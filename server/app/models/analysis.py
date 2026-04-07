from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class ImageUploadResponse(BaseModel):
    """Image upload response"""
    image_id: str
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime = Field(default_factory=datetime.now)


class RequestLocation(BaseModel):
    """Optional location coordinates for climate-aware analysis."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class ImageAnalysisRequest(BaseModel):
    """Image analysis request"""
    image_id: str
    language: Literal["en", "hi", "as", "brx"] = "en"
    location: Optional[RequestLocation] = None


class SymptomsAnalysisRequest(BaseModel):
    """Symptoms analysis request"""
    symptoms_description: str
    plant_type: Optional[str] = None
    language: Literal["en", "hi", "as", "brx"] = "en"
    location: Optional[RequestLocation] = None


class PlantCareRequest(BaseModel):
    """Plant care request"""
    plant_type: str
    language: Literal["en", "hi", "as", "brx"] = "en"
    location: Optional[RequestLocation] = None


# LLM Response Models
class ImageAnalysisLLMResponse(BaseModel):
    """Expert plant pathologist analysis of leaf images."""
    plant_identification: str = Field(
        ..., 
        description="Plant name in simple words with 1 short identifying clue"
    )
    health_status: Literal["Healthy", "Mild", "Moderate", "Severe"] = Field(
        ..., 
        description="Health status: must be one of Healthy, Mild, Moderate, or Severe"
    )
    confidence: Literal["High", "Medium", "Low"] = Field(
        ..., 
        description="Confidence level: must be one of High, Medium, or Low"
    )
    primary_issue: str = Field(
        ..., 
        description="Main issue in simple words, one short line"
    )
    quick_summary: str = Field(
        ..., 
        description="Short 2-3 sentence summary in plain language for non-technical users"
    )
    immediate_action: str = Field(
        ..., 
        description="Immediate next steps for 24-48 hours as clean bullet points, easy to follow"
    )
    treatment: str = Field(
        ..., 
        description="Treatment plan as short actionable bullet points with simple timing guidance"
    )
    prevention: str = Field(
        ..., 
        description="Simple prevention checklist in concise bullet points"
    )
    detailed_analysis: str = Field(
        ..., 
        description="Structured markdown report with clear headings, but still readable by normal users"
    )


class SymptomsAnalysisLLMResponse(BaseModel):
    """Expert plant pathologist analysis based on symptom descriptions."""
    likely_condition: str = Field(
        ..., 
        description="Most likely condition in simple words"
    )
    severity: Literal["Healthy", "Mild", "Moderate", "Severe"] = Field(
        ..., 
        description="Severity level: must be one of Healthy, Mild, Moderate, or Severe"
    )
    confidence: Literal["High", "Medium", "Low"] = Field(
        ..., 
        description="Confidence level: must be one of High, Medium, or Low"
    )
    quick_summary: str = Field(
        ..., 
        description="Short plain-language summary of likely condition and risk"
    )
    immediate_action: str = Field(
        ..., 
        description="Immediate actions in clean short bullet points"
    )
    treatment_steps: str = Field(
        ..., 
        description="Treatment steps in simple bullet format with practical timing"
    )
    what_to_watch: str = Field(
        ..., 
        description="Simple monitoring checklist with short time windows"
    )
    detailed_analysis: str = Field(
        ..., 
        description="Markdown analysis with clear sections and readable language"
    )


class EssentialCare(BaseModel):
    """Essential care requirements for plants."""
    light: str = Field(
        ..., 
        description="Simple light advice with clear duration or placement hint"
    )
    water: str = Field(
        ..., 
        description="Practical watering guidance in plain language"
    )
    soil: str = Field(
        ..., 
        description="Easy-to-understand soil advice with key do/don't points"
    )


class PlantCareLLMResponse(BaseModel):
    """Comprehensive care guidelines for specific plant types."""
    care_difficulty: Literal["Easy", "Moderate", "Difficult"] = Field(
        ..., 
        description="Care difficulty level: must be one of Easy, Moderate, or Difficult"
    )
    quick_overview: str = Field(
        ..., 
        description="Short plain-language overview for beginners"
    )
    essential_care: EssentialCare = Field(
        ..., 
        description="Essential care requirements covering light, water, and soil needs"
    )
    key_tips: List[str] = Field(
        ..., 
        description="Exactly 5 concise and practical care tips in simple wording"
    )
    common_problems: List[str] = Field(
        ..., 
        description="Exactly 3 common problems with short and clear fixes"
    )
    detailed_guide: str = Field(
        ..., 
        description="Markdown care guide with clear sections and non-technical language"
    )

