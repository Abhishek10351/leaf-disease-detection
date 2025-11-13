from typing import Dict, Any
from .gemini_model import gemini_vision_model
from langchain_core.messages import HumanMessage


def analyze_leaf_image(image_base64: str, additional_context: str = "") -> Dict[str, Any]:
    """
    Analyze a leaf image for disease detection using Gemini Vision.
    
    Args:
        image_base64: Base64 encoded image data
        additional_context: Optional additional context about the plant
    
    Returns:
        Dict containing analysis results
        
    Raises:
        Exception: If analysis fails
    """
    # Create the analysis prompt
    analysis_prompt = f"""
    You are an expert plant pathologist and agricultural specialist. Analyze this leaf image and provide a comprehensive diagnosis.

    Please provide your analysis in the following structured format:

    **Plant Identification:**
    - Likely plant species or family

    **Health Assessment:**
    - Overall health status (Healthy/Mild Issues/Moderate Disease/Severe Disease)
    - Confidence level (1-10)

    **Disease/Issue Detection:**
    - Primary concerns identified
    - Secondary issues (if any)
    - Affected areas of the leaf

    **Diagnosis:**
    - Most likely disease/condition
    - Alternative possibilities
    - Severity level

    **Treatment Recommendations:**
    - Immediate actions to take
    - Treatment options (organic/chemical)
    - Application methods and frequency

    **Prevention Measures:**
    - Environmental factors to control
    - Best practices for plant care
    - Monitoring recommendations

    **Prognosis:**
    - Expected recovery time
    - Likelihood of spread to other plants
    - Long-term plant health outlook

    Additional context: {additional_context}

    Please be specific, practical, and provide actionable advice. If you're uncertain about any aspect, mention the uncertainty and suggest consulting a local agricultural extension office.
    """

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

    # Get analysis from Gemini (let exceptions propagate)
    response = gemini_vision_model.invoke([message])
    
    return {
        "analysis": response.content,
        "model_used": "gemini-2.0",
        "confidence": "AI-generated analysis"
    }


def analyze_leaf_symptoms(symptoms_description: str, plant_type: str = "") -> Dict[str, Any]:
    """
    Analyze leaf symptoms based on text description only.
    
    Args:
        symptoms_description: Detailed description of symptoms
        plant_type: Type of plant (optional)
    
    Returns:
        Dict containing analysis results
        
    Raises:
        Exception: If analysis fails
    """
    plant_context = f"Plant type: {plant_type}\n" if plant_type else ""
    
    analysis_prompt = f"""
    You are an expert plant pathologist. Based on the described symptoms, provide a comprehensive analysis.

    {plant_context}Symptoms described: {symptoms_description}

    Please provide your analysis in the following format:

    **Symptom Analysis:**
    - Key symptoms identified
    - Symptom severity assessment

    **Possible Diagnoses:**
    - Most likely conditions (ranked by probability)
    - Distinguishing characteristics

    **Recommended Actions:**
    - Immediate steps to take
    - Diagnostic tests to perform
    - Treatment options

    **Additional Information Needed:**
    - What to observe or test
    - Environmental factors to consider

    **Prevention and Care:**
    - Preventive measures
    - Ongoing monitoring advice

    Please be specific and practical in your recommendations.
    """

    # Get analysis from Gemini (let exceptions propagate)
    response = gemini_vision_model.invoke(analysis_prompt)
    
    return {
        "analysis": response.content,
        "model_used": "gemini-2.0-flash"
    }


def get_plant_care_tips(plant_type: str) -> Dict[str, Any]:
    """
    Get general care tips for a specific plant type.
    
    Args:
        plant_type: Type of plant
    
    Returns:
        Dict containing care tips
        
    Raises:
        Exception: If getting care tips fails
    """
    care_prompt = f"""
    Provide comprehensive care guidelines for {plant_type}. Include:

    **Basic Care Requirements:**
    - Light requirements
    - Watering needs
    - Soil preferences
    - Temperature and humidity

    **Growth and Maintenance:**
    - Fertilization schedule
    - Pruning guidelines
    - Repotting needs (if applicable)

    **Common Problems:**
    - Typical diseases and pests
    - Early warning signs
    - Prevention strategies

    **Seasonal Care:**
    - Spring/Summer care
    - Fall/Winter adjustments

    **Troubleshooting:**
    - Common issues and solutions
    - When to seek professional help

    Make the advice practical and suitable for home gardeners.
    """

    # Get care tips from Gemini (let exceptions propagate)
    response = gemini_vision_model.invoke(care_prompt)
    
    return {
        "care_tips": response.content,
        "plant_type": plant_type,
        "model_used": "gemini-2.0-flash"
    }