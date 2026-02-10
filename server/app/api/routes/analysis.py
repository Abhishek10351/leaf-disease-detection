import logging
from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.responses import FileResponse
from typing import Optional
from datetime import datetime
from bson import ObjectId
import base64
from pathlib import Path
import aiofiles

logger = logging.getLogger(__name__)

from app.models.analysis import (
    ImageUploadResponse,
    ImageAnalysisRequest,
    SymptomsAnalysisRequest,
    PlantCareRequest,
    ImageAnalysisLLMResponse,
    SymptomsAnalysisLLMResponse,
    PlantCareLLMResponse,
)
from ...llm_core.utils import (
    analyze_leaf_image,
    analyze_leaf_symptoms,
    get_plant_care_tips,
)

router = APIRouter(prefix="/analysis", tags=["leaf-analysis"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_image(
    req: Request,
    file: UploadFile = File(...)
):
    """Upload an image and get an ID for later analysis"""
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="File size too large (max 10MB)")
    
    # Generate unique image ID and file path
    image_id = str(ObjectId())
    file_extension = Path(file.filename).suffix.lower() if file.filename else '.jpg'
    file_path = UPLOAD_DIR / f"{image_id}{file_extension}"
    
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    try:
        # Save file to disk
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Store metadata in database
        image_metadata = {
            "_id": image_id,
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type,
            "file_path": str(file_path),
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
    request: ImageAnalysisRequest
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

    # Read image file from disk
    file_path = Path(image_doc["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found on disk")

    try:
        # Read and encode image to base64
        async with aiofiles.open(file_path, 'rb') as f:
            file_content = await f.read()
        image_base64 = base64.b64encode(file_content).decode('utf-8')

        # Perform analysis
        result = analyze_leaf_image(image_base64=image_base64)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Analysis failed: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
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
                "filename": image_doc["filename"]
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now()
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        # Log error but don't fail the request if history save fails
        logger.warning(f"Failed to save analysis history: {str(e)}")

    return result


@router.post("/symptoms", response_model=SymptomsAnalysisLLMResponse)
async def analyze_symptoms(
    req: Request,
    request: SymptomsAnalysisRequest
):
    """Analyze plant symptoms based on description"""
    # Perform symptoms analysis
    try:
        result = analyze_leaf_symptoms(
            symptoms_description=request.symptoms_description,
            plant_type=request.plant_type or ""
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Analysis failed: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    # Save to history
    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "symptoms",
            "user_id": user_id,
            "request_data": {
                "symptoms_description": request.symptoms_description,
                "plant_type": request.plant_type
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now()
        }
        await req.app.mongodb["analysis_history"].insert_one(history_data)
    except Exception as e:
        # Log error but don't fail the request if history save fails
        logger.warning(f"Failed to save symptoms analysis history: {str(e)}")

    return result


@router.post("/care-tips", response_model=PlantCareLLMResponse)
async def get_care_tips(
    req: Request,
    request: PlantCareRequest
):
    """Get care tips for a specific plant type"""
    # Get care tips
    try:
        result = get_plant_care_tips(plant_type=request.plant_type)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to get care tips: {str(e)}")

    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
        user_id = req.state.user.email
    
    # Save to history
    try:
        history_data = {
            "_id": str(ObjectId()),
            "analysis_type": "care",
            "user_id": user_id,
            "request_data": {
                "plant_type": request.plant_type
            },
            "response_data": result.model_dump(),
            "timestamp": datetime.now()
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
    skip: int = 0
):
    """Get list of uploaded images"""
    # Get user_id if logged in
    user_id = None
    if hasattr(req.state, 'user') and req.state.user:
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
                "limit": limit
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
                "uploaded_at": img["uploaded_at"]
            })
        
        return {
            "images": formatted_images,
            "total": len(formatted_images),
            "skip": skip,
            "limit": limit
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
            formatted_item = {
                "id": item["_id"],
                "analysis_type": item["analysis_type"],
                "timestamp": item["timestamp"],
                "request_data": item["request_data"]
            }
            
            # Add analysis preview if available
            analysis_text = item["response_data"].get("analysis") or item["response_data"].get("care_tips", "")
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
