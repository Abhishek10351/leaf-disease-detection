"""
RAG API routes for knowledge base management and RAG-enhanced analysis.

Endpoints:
- POST /rag/seed-kb - Seed knowledge base with diseases, treatments, care guides
- GET /rag/kb-stats - Get knowledge base statistics
- POST /rag/search - Search knowledge base
- POST /rag/analyze-with-rag - Perform RAG-enhanced disease analysis
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.rag_core import RAGService, get_rag_service, KNOWLEDGE_BASE_SEED
from app.core.security import get_current_user
from app.models import User

router = APIRouter(prefix="/rag", tags=["RAG"])


# ============================================================================
# Request/Response Models
# ============================================================================

class SearchRequest(BaseModel):
    """Request model for knowledge base search"""
    query: str = Field(..., min_length=3, max_length=500, description="Search query text")
    include_diseases: bool = Field(default=True, description="Include disease documents")
    include_treatments: bool = Field(default=True, description="Include treatment documents")
    include_care: bool = Field(default=True, description="Include care guide documents")
    filter_plant: Optional[str] = Field(default=None, description="Filter by plant type")
    limit: int = Field(default=5, ge=1, le=20, description="Max results to return")
    min_similarity: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity score")


class SearchResult(BaseModel):
    """Search result item"""
    id: str
    content: str
    metadata: Dict[str, Any]
    similarity_score: float


class SearchResponse(BaseModel):
    """Response model for search"""
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float


class DiseaseAnalysisRequest(BaseModel):
    """Request model for RAG-enhanced disease analysis"""
    disease_name: str = Field(..., min_length=2, max_length=100, description="Disease name or symptoms")
    plant_type: Optional[str] = Field(default=None, description="Plant being analyzed")
    severity: Optional[str] = Field(default=None, description="Disease severity (mild/moderate/severe)")
    symptoms: Optional[str] = Field(default=None, max_length=500, description="Observed symptoms")
    use_rag: bool = Field(default=True, description="Enable RAG context retrieval")


class DiseaseAnalysisResponse(BaseModel):
    """Response model for disease analysis"""
    query: str
    analysis: str
    rag_enhanced: bool
    referenced_cases: int
    retrieval_count: int
    retrieved_documents: List[SearchResult]
    confidence: Optional[float] = None
    analysis_time_ms: float


class KBStatsResponse(BaseModel):
    """Knowledge base statistics"""
    disease_count: int
    treatment_count: int
    care_guide_count: int
    case_history_count: int
    total_vectors: int
    collections: List[str]


class SeedKBRequest(BaseModel):
    """Request to seed knowledge base"""
    use_default_seeds: bool = Field(default=True, description="Load default disease/treatment/care data")
    additional_diseases: Optional[List[Dict[str, Any]]] = Field(default=None, description="Additional diseases to add")
    additional_treatments: Optional[List[Dict[str, Any]]] = Field(default=None, description="Additional treatments")
    additional_care: Optional[List[Dict[str, Any]]] = Field(default=None, description="Additional care guides")


# ============================================================================
# Helper Functions
# ============================================================================

def format_retrieved_results(results: List[Any]) -> List[SearchResult]:
    """Convert retrieval results to API response format"""
    return [
        SearchResult(
            id=r.id,
            content=r.content,
            metadata=r.metadata,
            similarity_score=r.similarity_score
        )
        for r in results
    ]


# ============================================================================
# Routes
# ============================================================================

@router.post("/seed-kb", response_model=Dict[str, Any], summary="Seed Knowledge Base")
async def seed_knowledge_base(
    request: SeedKBRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Seed the knowledge base with diseases, treatments, and care guides.
    
    **Options:**
    - `use_default_seeds`: Load built-in disease/treatment/care data (recommended for first run)
    - `additional_diseases`: Add custom disease entries
    - `additional_treatments`: Add custom treatment entries
    - `additional_care`: Add custom care guide entries
    
    **Response:** Count of added documents by category
    """
    try:
        counts = {}
        
        if request.use_default_seeds:
            counts = await rag_service.seed_knowledge_base(KNOWLEDGE_BASE_SEED)
            logger.info(f"Seeded KB with defaults: {counts}")
        
        # Add additional data if provided
        if request.additional_diseases:
            for disease in request.additional_diseases:
                await rag_service.add_disease(disease)
            counts["diseases"] = counts.get("diseases", 0) + len(request.additional_diseases)
        
        if request.additional_treatments:
            for treatment in request.additional_treatments:
                await rag_service.add_treatment(treatment)
            counts["treatments"] = counts.get("treatments", 0) + len(request.additional_treatments)
        
        if request.additional_care:
            for care in request.additional_care:
                await rag_service.add_care_guide(care)
            counts["care_guides"] = counts.get("care_guides", 0) + len(request.additional_care)
        
        return {
            "status": "success",
            "message": "Knowledge base seeded successfully",
            "counts": counts
        }
    
    except Exception as e:
        print(f"Error seeding KB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to seed knowledge base: {str(e)}")


@router.get("/kb-stats", response_model=KBStatsResponse, summary="Get KB Statistics")
async def get_kb_stats(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get statistics about the knowledge base.
    
    **Returns:**
    - Count of diseases, treatments, care guides, and cases
    - Total vectors stored
    - Available collections
    """
    try:
        stats = await rag_service.get_kb_stats()
        return KBStatsResponse(**stats)
    
    except Exception as e:
        print(f"Error fetching KB stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get KB stats: {str(e)}")


@router.post("/search", response_model=SearchResponse, summary="Search Knowledge Base")
async def search_knowledge_base(
    request: SearchRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Search the knowledge base using semantic search.
    
    **Query Types:**
    - Disease names: "powdery mildew", "early blight"
    - Symptoms: "white spots on leaves", "yellowing leaves"
    - Treatments: "fungicide spray", "organic control"
    - Care tips: "watering schedule", "soil preparation"
    
    **Filters:**
    - `filter_plant`: Search only for specific plants (rose, tomato, etc.)
    - Document type filters: include_diseases, include_treatments, include_care
    - `min_similarity`: Confidence threshold (0.3 = good, 0.7 = very confident)
    """
    try:
        import time
        start_time = time.time()
        
        results = await rag_service.search_knowledge_base(
            query=request.query,
            limit=request.limit,
            min_similarity=request.min_similarity,
            filter_plant=request.filter_plant,
            include_diseases=request.include_diseases,
            include_treatments=request.include_treatments,
            include_care=request.include_care
        )
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=request.query,
            results=format_retrieved_results(results),
            total_results=len(results),
            search_time_ms=elapsed_ms
        )
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")


@router.post(
    "/analyze-with-rag",
    response_model=DiseaseAnalysisResponse,
    summary="RAG-Enhanced Disease Analysis"
)
async def analyze_with_rag(
    request: DiseaseAnalysisRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Perform disease analysis with RAG context retrieval.
    
    This endpoint:
    1. Searches knowledge base for relevant diseases, treatments, and symptoms
    2. Validates retrieval quality (confidence-based branching)
    3. Calls Gemini with augmented context if confidence is high enough
    4. Returns analysis enriched with referenced documents and care recommendations
    
    **Request Fields:**
    - `disease_name`: Main disease or symptom description (required)
    - `plant_type`: Plant being analyzed (optional, helps filter results)
    - `severity`: Disease severity level (optional)
    - `symptoms`: Detailed symptom description (optional)
    - `use_rag`: Enable/disable RAG context (default: true)
    
    **Response includes:**
    - LLM analysis with RAG context
    - Retrieved documents used for enhancement
    - Confidence scores and counts
    """
    try:
        import time
        start_time = time.time()
        
        # Build analysis query
        analysis_query = request.disease_name
        if request.symptoms:
            analysis_query += f" - {request.symptoms}"
        
        # Execute RAG analysis
        result = await rag_service.analyze_with_rag(
            query=analysis_query,
            plant_type=request.plant_type,
            severity=request.severity,
            use_context=request.use_rag
        )
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Extract and format results
        analysis_text = result.get("analysis", "")
        rag_enhanced = result.get("rag_enhanced", False)
        referenced_count = result.get("referenced_cases", 0)
        confidence = result.get("confidence")
        retrieved_docs = result.get("retrieved_documents", [])
        
        return DiseaseAnalysisResponse(
            query=analysis_query,
            analysis=analysis_text,
            rag_enhanced=rag_enhanced,
            referenced_cases=referenced_count,
            retrieval_count=len(retrieved_docs),
            retrieved_documents=format_retrieved_results(retrieved_docs),
            confidence=confidence,
            analysis_time_ms=elapsed_ms
        )
    
    except Exception as e:
        print(f"RAG analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG analysis failed: {str(e)}"
        )


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health", summary="Health Check")
async def rag_health(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Check RAG system health and readiness.
    
    Returns status of:
    - Chroma vector database connection
    - Embedding generator availability
    - LangGraph workflow setup
    - Knowledge base status
    """
    try:
        stats = await rag_service.get_kb_stats()
        return {
            "status": "healthy",
            "rag_ready": stats.get("total_vectors", 0) > 0,
            "knowledge_base": stats
        }
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "rag_ready": False,
            "error": str(e)
        }
