from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ImageUploadResponse(BaseModel):
    """Response model for successful image upload"""
    image_id: str = Field(..., description="Unique image identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="MIME type")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")


class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis using uploaded image ID"""
    image_id: str = Field(..., description="ID of uploaded image")


class SymptomsAnalysisRequest(BaseModel):
    """Request model for symptoms-only analysis"""
    symptoms_description: str = Field(..., description="Detailed description of plant symptoms")
    plant_type: Optional[str] = Field(default=None, description="Type of plant (optional)")


class PlantCareRequest(BaseModel):
    """Request model for plant care tips"""
    plant_type: str = Field(..., description="Type of plant")


class AnalysisResponse(BaseModel):
    """Response model for successful analysis results"""
    analysis: str = Field(..., description="Analysis results")
    model_used: str = Field(..., description="AI model used")
    confidence: Optional[str] = Field(default=None, description="Confidence level")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class CareResponse(BaseModel):
    """Response model for successful care tips"""
    care_tips: str = Field(..., description="Care tips")
    plant_type: str = Field(..., description="Plant type")
    model_used: str = Field(..., description="AI model used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


