from typing import Optional
from .gemini_model import gemini_vision_model
from app.models.analysis import ImageAnalysisLLMResponse, SymptomsAnalysisLLMResponse, PlantCareLLMResponse
from langchain_core.messages import HumanMessage


def analyze_leaf_image(image_base64: str) -> ImageAnalysisLLMResponse:
    """
    Analyze a leaf image for disease detection using Gemini Vision.
    
    Args:
        image_base64: Base64 encoded image data
    
    Returns:
        ImageAnalysisLLMResponse object
        
    Raises:
        Exception: If analysis fails
    """
    # Create structured output model
    structured_model = gemini_vision_model.with_structured_output(ImageAnalysisLLMResponse)
    
    # Create the analysis prompt
    analysis_prompt = "You are an expert plant pathologist. Analyze this leaf image and provide a comprehensive diagnosis."

    # Create message with image
    message = HumanMessage(
        content=[
            {"type": "text", "text": analysis_prompt},
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            }
        ]
    )

    # Get structured analysis from Gemini
    analysis_data = structured_model.invoke([message])
    
    return analysis_data


def analyze_leaf_symptoms(symptoms_description: str, plant_type: str = "") -> SymptomsAnalysisLLMResponse:
    """
    Analyze leaf symptoms based on text description only.
    
    Args:
        symptoms_description: Detailed description of symptoms
        plant_type: Type of plant (optional)
    
    Returns:
        SymptomsAnalysisLLMResponse object
        
    Raises:
        Exception: If analysis fails
    """
    # Create structured output model
    structured_model = gemini_vision_model.with_structured_output(SymptomsAnalysisLLMResponse)
    
    plant_context = f"Plant type: {plant_type}\n" if plant_type else ""
    
    analysis_prompt = f"You are an expert plant pathologist. Analyze these symptoms and provide a comprehensive diagnosis.\n\n{plant_context}Symptoms: {symptoms_description}"

    # Get structured analysis from Gemini
    analysis_data = structured_model.invoke(analysis_prompt)
    
    return analysis_data


def get_plant_care_tips(plant_type: str) -> PlantCareLLMResponse:
    """
    Get general care tips for a specific plant type.
    
    Args:
        plant_type: Type of plant
    
    Returns:
        PlantCareLLMResponse object
        
    Raises:
        Exception: If getting care tips fails
    """
    # Create structured output model
    structured_model = gemini_vision_model.with_structured_output(PlantCareLLMResponse)
    
    care_prompt = f"Provide comprehensive care guidelines for {plant_type}."

    # Get structured care tips from Gemini
    care_data = structured_model.invoke(care_prompt)
    
    return care_data