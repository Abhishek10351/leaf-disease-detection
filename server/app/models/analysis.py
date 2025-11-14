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
    analysis_type: str = Field(..., description="Type of analysis performed")
    summary: Optional[str] = Field(default=None, description="Brief summary of findings")
    severity: Optional[str] = Field(default=None, description="Issue severity level")
    # New structured fields for better UX
    plant_identification: Optional[str] = Field(default=None, description="Plant species/family")
    primary_issue: Optional[str] = Field(default=None, description="Main problem identified")
    immediate_action: Optional[str] = Field(default=None, description="What to do right now")
    treatment: Optional[str] = Field(default=None, description="Treatment recommendations")
    prevention: Optional[str] = Field(default=None, description="Prevention measures")
    likely_condition: Optional[str] = Field(default=None, description="Most likely condition")
    treatment_steps: Optional[str] = Field(default=None, description="Treatment steps")
    what_to_watch: Optional[str] = Field(default=None, description="What to monitor")


class CareResponse(BaseModel):
    """Response model for successful care tips"""
    care_tips: str = Field(..., description="Care tips")
    plant_type: str = Field(..., description="Plant type")
    model_used: str = Field(..., description="AI model used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    care_difficulty: Optional[str] = Field(default=None, description="Care difficulty level")
    seasonal_care: Optional[str] = Field(default=None, description="Seasonal care notes")
    # New structured fields for better UX
    quick_overview: Optional[str] = Field(default=None, description="Brief overview of care needs")
    essential_care: Optional[dict] = Field(default=None, description="Essential care requirements")
    key_tips: Optional[list] = Field(default=None, description="Key care tips")
    common_problems: Optional[list] = Field(default=None, description="Common problems and solutions")


