from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ImageUploadResponse(BaseModel):
    """Image upload response"""
    image_id: str
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime = Field(default_factory=datetime.now)


class ImageAnalysisRequest(BaseModel):
    """Image analysis request"""
    image_id: str


class SymptomsAnalysisRequest(BaseModel):
    """Symptoms analysis request"""
    symptoms_description: str
    plant_type: Optional[str] = None


class PlantCareRequest(BaseModel):
    """Plant care request"""
    plant_type: str


# LLM Response Models
class ImageAnalysisLLMResponse(BaseModel):
    """Expert plant pathologist analysis of leaf images."""
    plant_identification: str = Field(
        ..., 
        description="Plant species/family with key identifying features"
    )
    health_status: str = Field(
        ..., 
        description="Health status: must be one of Healthy, Mild, Moderate, or Severe"
    )
    confidence: str = Field(
        ..., 
        description="Confidence level: must be one of High, Medium, or Low"
    )
    primary_issue: str = Field(
        ..., 
        description="Main problem identified with brief description"
    )
    quick_summary: str = Field(
        ..., 
        description="2-3 sentence summary explaining the condition and its impact"
    )
    immediate_action: str = Field(
        ..., 
        description="What to do in the next 24-48 hours: 3-4 actionable steps with specific details like application rates and timing"
    )
    treatment: str = Field(
        ..., 
        description="Comprehensive treatment plan with specific methods, timing, and application details (4-6 detailed points)"
    )
    prevention: str = Field(
        ..., 
        description="Prevention strategies including environmental controls, care practices, and monitoring tips (3-4 points)"
    )
    detailed_analysis: str = Field(
        ..., 
        description="Complete technical analysis in markdown format with pathology details, symptom progression, differential diagnosis, and scientific reasoning. Well-organized with clear sections for home gardeners."
    )


class SymptomsAnalysisLLMResponse(BaseModel):
    """Expert plant pathologist analysis based on symptom descriptions."""
    likely_condition: str = Field(
        ..., 
        description="Most probable disease/issue with brief description"
    )
    severity: str = Field(
        ..., 
        description="Severity level: must be one of Healthy, Mild, Moderate, or Severe"
    )
    confidence: str = Field(
        ..., 
        description="Confidence level: must be one of High, Medium, or Low"
    )
    quick_summary: str = Field(
        ..., 
        description="2-3 sentence explanation covering the condition, its causes, and potential impact"
    )
    immediate_action: str = Field(
        ..., 
        description="Detailed immediate steps to take within 24-48 hours (3-4 specific actions with application rates and timing)"
    )
    treatment_steps: str = Field(
        ..., 
        description="Comprehensive treatment plan with methods, timing, and application details (4-6 detailed steps)"
    )
    what_to_watch: str = Field(
        ..., 
        description="Key symptoms and progression indicators to monitor, including timeframes (3-4 monitoring points with visual indicators)"
    )
    detailed_analysis: str = Field(
        ..., 
        description="Complete technical analysis in markdown format including differential diagnosis, pathophysiology, environmental factors, and long-term management. Accessible to serious gardeners."
    )


class EssentialCare(BaseModel):
    """Essential care requirements for plants."""
    light: str = Field(
        ..., 
        description="Detailed light requirements with specific conditions, duration, and positioning tips"
    )
    water: str = Field(
        ..., 
        description="Comprehensive watering guidelines including frequency, amount, seasonal changes, and soil moisture indicators"
    )
    soil: str = Field(
        ..., 
        description="Specific soil requirements including pH, drainage, nutrients, and recommended mixes or amendments"
    )


class PlantCareLLMResponse(BaseModel):
    """Comprehensive care guidelines for specific plant types."""
    care_difficulty: str = Field(
        ..., 
        description="Care difficulty level: must be one of Easy, Moderate, or Difficult"
    )
    quick_overview: str = Field(
        ..., 
        description="2-3 sentence overview covering the plant's nature, basic needs, and what makes it special"
    )
    essential_care: EssentialCare = Field(
        ..., 
        description="Essential care requirements covering light, water, and soil needs"
    )
    key_tips: List[str] = Field(
        ..., 
        description="5 key care tips with specific techniques, timing, measurements, indicators, troubleshooting guidance, and seasonal considerations"
    )
    common_problems: List[str] = Field(
        ..., 
        description="3 common problems with detailed descriptions, causes, and step-by-step solutions"
    )
    detailed_guide: str = Field(
        ..., 
        description="Comprehensive care guide in markdown format with advanced techniques, seasonal care, propagation, fertilization schedules, pruning guidelines, and troubleshooting. Include specific measurements, timing, visual cues, and professional tips while remaining accessible to dedicated home gardeners."
    )

