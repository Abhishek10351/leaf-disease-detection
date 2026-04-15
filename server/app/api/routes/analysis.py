import asyncio
import base64
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import aiofiles
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

from app.models.analysis import (
    ImageUploadResponse,
    ImageAnalysisRequest,
    ImageAnalysisTranslationRequest,
    SymptomsAnalysisRequest,
    PlantCareRequest,
    ImageAnalysisLLMResponse,
    SymptomsAnalysisLLMResponse,
    PlantCareLLMResponse,
)
from app.core.config import settings
from app.llm_core import get_leaf_analysis
from app.utils.image_hashing import compute_phash_hex, phash_hamming_distance
from app.utils.weather import build_location_weather_context_for_coordinates


def _get_leaf_analysis():
    """Return cached analysis service instance."""
    return get_leaf_analysis()


def _contains_weather_reference(text: Optional[str]) -> bool:
    if not text:
        return False
    normalized = text.lower()
    keywords = ["weather", "rain", "rainfall", "humidity", "forecast", "precipitation", "climate"]
    return any(keyword in normalized for keyword in keywords)


def _build_weather_note(weather_context: str) -> str:
    first_sentence = weather_context.split(".")[0].strip()
    if not first_sentence:
        return (
            "Weather note: Local weather conditions should guide spray timing "
            "and disease-risk prioritization."
        )
    return f"Weather note: {first_sentence}."


def _normalize_markdown(raw: Optional[str]) -> str:
    """Normalize imperfect markdown returned by models for stable rendering."""
    if not raw:
        return ""

    text = raw.replace("\r\n", "\n")

    # Ensure heading markers are followed by a space.
    text = re.sub(r"(^|\n)(\s{0,3}#{1,6})([^\s#])", r"\1\2 \3", text)
    # Start headings on a new line if they appear inline.
    text = re.sub(r"(\S)\s+(#{1,6}\s)", r"\1\n\n\2", text)
    # Normalize numbered lists from `1)` to `1.`.
    text = re.sub(r"(^|\n)(\s*)(\d+)\)\s+", r"\1\2\3. ", text)
    # Split inline list items into proper lines.
    text = re.sub(r"(\S)\s+(\d+[\.)]\s+)", r"\1\n\2", text)
    text = re.sub(r"(\S)\s+([*-]\s+)", r"\1\n\2", text)
    # Collapse excessive spacing.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _sanitize_image_result(result: ImageAnalysisLLMResponse) -> ImageAnalysisLLMResponse:
    result.immediate_action = _normalize_markdown(result.immediate_action)
    result.treatment = _normalize_markdown(result.treatment)
    result.prevention = _normalize_markdown(result.prevention)
    result.detailed_analysis = _normalize_markdown(result.detailed_analysis)
    return result


def _sanitize_symptoms_result(result: SymptomsAnalysisLLMResponse) -> SymptomsAnalysisLLMResponse:
    result.immediate_action = _normalize_markdown(result.immediate_action)
    result.treatment_steps = _normalize_markdown(result.treatment_steps)
    result.what_to_watch = _normalize_markdown(result.what_to_watch)
    result.detailed_analysis = _normalize_markdown(result.detailed_analysis)
    return result


def _sanitize_care_result(result: PlantCareLLMResponse) -> PlantCareLLMResponse:
    result.quick_overview = _normalize_markdown(result.quick_overview)
    result.essential_care.light = _normalize_markdown(result.essential_care.light)
    result.essential_care.water = _normalize_markdown(result.essential_care.water)
    result.essential_care.soil = _normalize_markdown(result.essential_care.soil)
    result.key_tips = [_normalize_markdown(item) for item in result.key_tips]
    result.common_problems = [_normalize_markdown(item) for item in result.common_problems]
    result.detailed_guide = _normalize_markdown(result.detailed_guide)
    return result


router = APIRouter(prefix="/analysis", tags=["leaf-analysis"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _extract_coordinates(request_with_location) -> tuple[Optional[float], Optional[float]]:
    location = getattr(request_with_location, "location", None)
    if not location:
        return None, None
    return location.latitude, location.longitude



def _location_scope_from_coordinates(latitude: Optional[float], longitude: Optional[float]) -> str:
    """Create coarse location scope so pHash cache reuse remains region-aware."""
    if latitude is None or longitude is None:
        return "fallback"
    return f"{round(latitude, 1)}:{round(longitude, 1)}"


async def _find_cached_image_analysis(
    req: Request,
    image_phash: str,
    language: str,
    location_scope: str,
) -> tuple[Optional[dict[str, Any]], Optional[int]]:
    """Find nearest cached image analysis using pHash Hamming distance."""
    cache_query = {
        "analysis_type": "image",
        "request_data.language": language,
        "request_data.location_scope": location_scope,
        "request_data.image_phash": {"$exists": True},
        "response_data": {"$exists": True},
    }
    projection = {
        "request_data.image_phash": 1,
        "response_data": 1,
    }
    cursor = (
        req.app.mongodb["analysis_history"]
        .find(cache_query, projection)
        .sort("timestamp", -1)
        .limit(settings.PHASH_CACHE_MAX_CANDIDATES)
    )
    docs = await cursor.to_list(length=settings.PHASH_CACHE_MAX_CANDIDATES)

    best_doc: Optional[dict[str, Any]] = None
    best_distance: Optional[int] = None
    for doc in docs:
        candidate_hash = doc.get("request_data", {}).get("image_phash")
        distance = phash_hamming_distance(image_phash, candidate_hash)
        if distance is None:
            continue
        if best_distance is None or distance < best_distance:
            best_doc = doc
            best_distance = distance

    if best_doc is None or best_distance is None:
        return None, None
    if best_distance > settings.PHASH_HAMMING_DISTANCE_THRESHOLD:
        return None, None

    return best_doc, best_distance

@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_image(
    req: Request,
    file: UploadFile = File(...),
):
    """Upload an image and get an ID for later analysis"""
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="File size too large (max 10MB)")

    try:
        image_phash = compute_phash_hex(file_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unsupported image payload: {str(e)}")
    
    # Generate unique image ID and file path
    image_id = str(ObjectId())
    file_extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    file_path = UPLOAD_DIR / f"{image_id}{file_extension}"

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    try:
        # Save file to disk
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_content)

        # Store metadata in database
        image_metadata = {
            "_id": image_id,
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type,
            "file_path": str(file_path),
            "phash": image_phash,
            "user_id": user_id,
            "uploaded_at": datetime.now()
        }

        await req.app.mongodb["uploaded_images"].insert_one(image_metadata)

    except Exception as e:
        # Clean up file if database save fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

    return ImageUploadResponse(
        image_id=image_id,
        filename=file.filename,
        file_size=len(file_content),
        content_type=file.content_type
    )


@router.post("/analyze", response_model=ImageAnalysisLLMResponse)
async def analyze_uploaded_image(
    req: Request,
    request: ImageAnalysisRequest,
):
    """Analyze a previously uploaded image using its ID"""
    # Get uploaded image metadata from database
    try:
        image_doc = await req.app.mongodb["uploaded_images"].find_one({
            "_id": request.image_id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if not image_doc:
        raise HTTPException(status_code=404, detail="Image not found")

    latitude, longitude = _extract_coordinates(request)
    location_scope = _location_scope_from_coordinates(latitude, longitude)
    weather_context = await asyncio.to_thread(
        build_location_weather_context_for_coordinates,
        latitude,
        longitude,
    )

    # Read image file from disk
    file_path = Path(image_doc["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found on disk")

    image_phash = image_doc.get("phash")

    try:
        # Read and encode image to base64
        async with aiofiles.open(file_path, "rb") as f:
            file_content = await f.read()

        if not image_phash:
            image_phash = compute_phash_hex(file_content)
            await req.app.mongodb["uploaded_images"].update_one(
                {"_id": request.image_id},
                {"$set": {"phash": image_phash}},
            )

        if image_phash:
            cached_doc, cache_distance = await _find_cached_image_analysis(
                req=req,
                image_phash=image_phash,
                language=request.language,
                location_scope=location_scope,
            )
            if cached_doc:
                cached_response = cached_doc.get("response_data") or {}
                result = ImageAnalysisLLMResponse.model_validate(cached_response)
                result = _sanitize_image_result(result)

                user_id = None
                if hasattr(req.state, "user") and req.state.user:
                    user_id = req.state.user.email

                try:
                    await req.app.mongodb["analysis_history"].insert_one(
                        {
                            "_id": str(ObjectId()),
                            "analysis_type": "image",
                            "image_id": request.image_id,
                            "user_id": user_id,
                            "request_data": {
                                "image_id": request.image_id,
                                "filename": image_doc["filename"],
                                "language": request.language,
                                "location": request.location.model_dump() if request.location else None,
                                "location_scope": location_scope,
                                "image_phash": image_phash,
                                "cache_hit": True,
                                "cache_distance": int(cache_distance) if cache_distance is not None else None,
                            },
                            "response_data": result.model_dump(),
                            "cache_source_history_id": str(cached_doc.get("_id")),
                            "timestamp": datetime.now(),
                        }
                    )
                except Exception as history_error:
                    logger.warning("Failed to save cache-hit history: %s", history_error)

                logger.info(
                    "pHash cache hit for image_id=%s distance=%s language=%s scope=%s",
                    request.image_id,
                    cache_distance,
                    request.language,
                    location_scope,
                )
                return result

        image_base64 = base64.b64encode(file_content).decode("utf-8")

        # Perform analysis
        result = _get_leaf_analysis().analyze_leaf_image(
            image_base64=image_base64,
            language=request.language,
            location_context=weather_context.weather_summary if weather_context else None,
        )

        if weather_context and weather_context.weather_summary:
            weather_note = _build_weather_note(weather_context.weather_summary)
            if not _contains_weather_reference(result.quick_summary):
                result.quick_summary = f"{result.quick_summary} {weather_note}".strip()
            if not _contains_weather_reference(result.immediate_action):
                result.immediate_action = f"{result.immediate_action}\n\n{weather_note}".strip()

        result = _sanitize_image_result(result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Analysis failed: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    # Save analysis to history
    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "image",
            "image_id": request.image_id,
            "user_id": user_id,
            "request_data": {
                "image_id": request.image_id,
                "filename": image_doc["filename"],
                "language": request.language,
                "location": request.location.model_dump() if request.location else None,
                "location_scope": location_scope,
                "image_phash": image_phash,
                "cache_hit": False,
                "weather_context": weather_context.weather_summary if weather_context else None,
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now(),
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        # Log error but don't fail the request if history save fails
        logger.warning(f"Failed to save analysis history: {str(e)}")

    return result


@router.post("/translate-image", response_model=ImageAnalysisLLMResponse)
async def translate_image_analysis(
    req: Request,
    request: ImageAnalysisTranslationRequest,
):
    """Translate an already generated image analysis response using final verifier model only."""
    try:
        result = _get_leaf_analysis().translate_image_analysis(
            response=request.response,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        result = _sanitize_image_result(result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Translation failed: {str(e)}")

    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "image_translation",
            "user_id": user_id,
            "request_data": {
                "source_language": request.source_language,
                "target_language": request.target_language,
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now(),
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        logger.warning(f"Failed to save image translation history: {str(e)}")

    return result


@router.post("/symptoms", response_model=SymptomsAnalysisLLMResponse)
async def analyze_symptoms(
    req: Request,
    request: SymptomsAnalysisRequest,
):
    """Analyze plant symptoms based on description"""
    latitude, longitude = _extract_coordinates(request)
    weather_context = await asyncio.to_thread(
        build_location_weather_context_for_coordinates,
        latitude,
        longitude,
    )

    # Perform symptoms analysis
    try:
        result = _get_leaf_analysis().analyze_leaf_symptoms(
            symptoms_description=request.symptoms_description,
            plant_type=request.plant_type or "",
            language=request.language,
            location_context=weather_context.weather_summary if weather_context else None,
        )
        result = _sanitize_symptoms_result(result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Analysis failed: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    # Save to history
    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "symptoms",
            "user_id": user_id,
            "request_data": {
                "symptoms_description": request.symptoms_description,
                "plant_type": request.plant_type,
                "language": request.language,
                "location": request.location.model_dump() if request.location else None,
                "weather_context": weather_context.weather_summary if weather_context else None,
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now(),
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        # Log error but don't fail the request if history save fails
        logger.warning(f"Failed to save symptoms analysis history: {str(e)}")

    return result


@router.post("/care-tips", response_model=PlantCareLLMResponse)
async def get_care_tips(
    req: Request,
    request: PlantCareRequest,
):
    """Get care tips for a specific plant type"""
    latitude, longitude = _extract_coordinates(request)
    weather_context = await asyncio.to_thread(
        build_location_weather_context_for_coordinates,
        latitude,
        longitude,
    )

    # Get care tips
    try:
        result = _get_leaf_analysis().get_plant_care_tips(
            plant_type=request.plant_type,
            language=request.language,
            location_context=weather_context.weather_summary if weather_context else None,
        )
        result = _sanitize_care_result(result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to get care tips: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    # Save to history
    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "care",
            "user_id": user_id,
            "request_data": {
                "plant_type": request.plant_type,
                "language": request.language,
                "location": request.location.model_dump() if request.location else None,
                "weather_context": weather_context.weather_summary if weather_context else None,
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now(),
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        # Log error but don't fail the request if history save fails
        logger.warning(f"Failed to save care tips history: {str(e)}")

    return result


@router.get("/images")
async def get_uploaded_images(
    req: Request,
    limit: int = 20,
    skip: int = 0,
):
    """Get list of uploaded images"""
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, "user") and req.state.user:
        user_id = req.state.user.email

    try:
        # Build query filter - show only user's images if logged in, blank if not
        query_filter = {}
        if user_id:
            query_filter["user_id"] = user_id
        else:
            # Return empty list if not logged in
            return {
                "images": [],
                "total": 0,
                "skip": skip,
                "limit": limit,
            }

        # Get images metadata from database
        images_cursor = req.app.mongodb["uploaded_images"].find(
            query_filter
        ).sort("uploaded_at", -1).skip(skip).limit(limit)

        images_list = await images_cursor.to_list(length=limit)
        
        # Format response
        formatted_images = []
        for img in images_list:
            formatted_images.append({
                "image_id": img["_id"],
                "filename": img["filename"],
                "file_size": img["file_size"],
                "content_type": img["content_type"],
                "uploaded_at": img["uploaded_at"],
            })

        return {
            "images": formatted_images,
            "total": len(formatted_images),
            "skip": skip,
            "limit": limit,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching images: {str(e)}")


@router.get("/images/{image_id}")
async def get_image_info(
    req: Request,
    image_id: str
):
    """Get information about a specific uploaded image"""
    try:
        # Get image metadata from database
        image_doc = await req.app.mongodb["uploaded_images"].find_one({
            "_id": image_id
        })
        
        if not image_doc:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return {
            "image_id": image_doc["_id"],
            "filename": image_doc["filename"],
            "file_size": image_doc["file_size"],
            "content_type": image_doc["content_type"],
            "uploaded_at": image_doc["uploaded_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image info: {str(e)}")


@router.get("/images/{image_id}/view")
async def view_image(
    req: Request,
    image_id: str
):
    """View/download the actual image file"""
    try:
        # Get image metadata from database
        image_doc = await req.app.mongodb["uploaded_images"].find_one({
            "_id": image_id
        })
        
        if not image_doc:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Handle both old records (with image_data) and new records (with file_path)
        if "file_path" in image_doc:
            # New storage system - file on disk
            file_path = Path(image_doc["file_path"])
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="Image file not found on disk")
            
            # Return the file with proper headers
            return FileResponse(
                path=str(file_path),
                media_type=image_doc["content_type"],
                filename=image_doc["filename"],
                headers={
                    "Content-Disposition": f"inline; filename=\"{image_doc['filename']}\"",
                    "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
                }
            )
        
        elif "image_data" in image_doc:
            # Old storage system - base64 in database
            # Create a temporary file and serve it
            import tempfile
            import base64
            
            try:
                image_data = base64.b64decode(image_doc["image_data"])
                
                # Create temporary file
                file_extension = Path(image_doc["filename"]).suffix.lower() if image_doc["filename"] else '.jpg'
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(image_data)
                    tmp_file_path = tmp_file.name
                
                # Return the temporary file
                return FileResponse(
                    path=tmp_file_path,
                    media_type=image_doc["content_type"],
                    filename=image_doc["filename"],
                    headers={
                        "Content-Disposition": f"inline; filename=\"{image_doc['filename']}\"",
                        "Cache-Control": "public, max-age=3600"
                    }
                )
                
            except Exception as decode_error:
                raise HTTPException(status_code=500, detail=f"Error decoding image data: {str(decode_error)}")
        
        else:
            raise HTTPException(status_code=404, detail="Image data not found (no file_path or image_data)")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")


@router.delete("/images/{image_id}")
async def delete_uploaded_image(
    req: Request,
    image_id: str
):
    """Delete an uploaded image"""
    try:
        # Get image metadata first to know the file path
        image_doc = await req.app.mongodb["uploaded_images"].find_one({
            "_id": image_id
        })
        
        if not image_doc:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Delete file from disk
        file_path = Path(image_doc["file_path"])
        if file_path.exists():
            file_path.unlink()
        
        # Delete image metadata from database
        await req.app.mongodb["uploaded_images"].delete_one({
            "_id": image_id
        })
        
        # Also delete related analysis history
        await req.app.mongodb["analysis_history"].delete_many({
            "image_id": image_id
        })
        
        return {"message": "Image and related analyses deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")


@router.get("/history")
async def get_analysis_history(
    req: Request,
    limit: int = 20,
    skip: int = 0,
    analysis_type: Optional[str] = None
):
    """Get analysis history"""
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    try:
        # Build query filter - show only user's history if logged in, blank if not
        query_filter = {}
        if user_id:
            query_filter["user_id"] = user_id
        else:
            # Return empty history if not logged in
            return {
                "history": [],
                "total": 0,
                "skip": skip,
                "limit": limit
            }
        
        if analysis_type:
            query_filter["analysis_type"] = analysis_type
        
        # Get history from database
        history_cursor = req.app.mongodb["analysis_history"].find(
            query_filter
        ).sort("timestamp", -1).skip(skip).limit(limit)
        
        history_list = await history_cursor.to_list(length=limit)
        
        # Format response
        formatted_history = []
        for item in history_list:
            response_data = item.get("response_data", {})
            formatted_item = {
                "id": item["_id"],
                "analysis_type": item["analysis_type"],
                "timestamp": item["timestamp"],
                "request_data": item.get("request_data", {}),
                "response_data": response_data,
            }
            
            # Build preview from the actual response fields for each analysis type.
            analysis_text = (
                response_data.get("quick_summary")
                or response_data.get("quick_overview")
                or response_data.get("primary_issue")
                or response_data.get("likely_condition")
                or response_data.get("detailed_analysis")
                or response_data.get("detailed_guide")
                or ""
            )
            if analysis_text:
                # Get first 200 characters as preview
                formatted_item["preview"] = analysis_text[:200] + ("..." if len(analysis_text) > 200 else "")
            
            formatted_history.append(formatted_item)
        
        return {
            "history": formatted_history,
            "total": len(formatted_history),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.get("/history/{analysis_id}")
async def get_analysis_detail(
    req: Request,
    analysis_id: str
):
    """Get detailed analysis result by ID"""
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    try:
        # Build query - ensure user can only access their own history
        query_filter = {"_id": analysis_id}
        if user_id:
            query_filter["user_id"] = user_id
        else:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Get analysis from database
        analysis = await req.app.mongodb["analysis_history"].find_one(query_filter)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            "id": analysis["_id"],
            "analysis_type": analysis["analysis_type"],
            "timestamp": analysis["timestamp"],
            "request_data": analysis["request_data"],
            "response_data": analysis["response_data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analysis detail: {str(e)}")


@router.delete("/history/{analysis_id}")
async def delete_analysis(
    req: Request,
    analysis_id: str
):
    """Delete an analysis from history"""
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    try:
        # Build query - ensure user can only delete their own history
        query_filter = {"_id": analysis_id}
        if user_id:
            query_filter["user_id"] = user_id
        else:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Delete analysis
        result = await req.app.mongodb["analysis_history"].delete_one(query_filter)
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting analysis: {str(e)}")
