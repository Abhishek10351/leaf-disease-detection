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
    You are an expert plant pathologist. Analyze this leaf image and provide a diagnosis in JSON format.

    Return your response as a valid JSON object with this exact structure:
    {{
        "plant_identification": "Plant species/family with key identifying features",
        "health_status": "Healthy/Mild/Moderate/Severe",
        "confidence": "High/Medium/Low",
        "primary_issue": "Main problem identified with brief description",
        "quick_summary": "2-3 sentence summary explaining the condition and its impact",
        "immediate_action": "What to do in the next 24-48 hours (3-4 actionable steps)",
        "treatment": "Comprehensive treatment plan with specific methods, timing, and application details (4-6 detailed points)",
        "prevention": "Prevention strategies including environmental controls, care practices, and monitoring tips (3-4 points)",
        "detailed_analysis": "Complete technical analysis in markdown format with pathology details, symptom progression, differential diagnosis, and scientific reasoning"
    }}

    Additional context: {additional_context}

    Make the content informative but accessible to home gardeners. Include specific details like application rates, timing, and visual cues to look for. The detailed_analysis should be comprehensive but well-organized with clear sections.
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
    
    try:
        # Try to parse JSON response
        import json
        response_text = response.content.strip()
        
        # Clean up response if it has markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        analysis_data = json.loads(response_text)
        
        return {
            "analysis": analysis_data.get("detailed_analysis", response.content),
            "model_used": "gemini-2.0-flash-exp",
            "confidence": analysis_data.get("confidence", "AI-generated"),
            "summary": analysis_data.get("quick_summary", "Analysis completed"),
            "severity": analysis_data.get("health_status", "Unknown"),
            "plant_identification": analysis_data.get("plant_identification", ""),
            "primary_issue": analysis_data.get("primary_issue", ""),
            "immediate_action": analysis_data.get("immediate_action", ""),
            "treatment": analysis_data.get("treatment", ""),
            "prevention": analysis_data.get("prevention", "")
        }
    except (json.JSONDecodeError, KeyError) as e:
        # Fallback to original processing if JSON parsing fails
        content = response.content
        severity = "Unknown"
        summary = ""
        
        # Try to extract severity from content
        if "Severe" in content:
            severity = "Severe"
        elif "Moderate" in content:
            severity = "Moderate"  
        elif "Mild" in content:
            severity = "Mild"
        elif "Healthy" in content:
            severity = "Healthy"
        
        # Extract first meaningful line as summary
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                summary = line.strip()[:150] + "..." if len(line.strip()) > 150 else line.strip()
                break
        
        return {
            "analysis": content,
            "model_used": "gemini-2.0-flash-exp",
            "confidence": "AI-generated analysis",
            "summary": summary,
            "severity": severity
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
    You are an expert plant pathologist. Analyze these symptoms and provide a diagnosis in JSON format.

    {plant_context}Symptoms: {symptoms_description}

    Return your response as a valid JSON object with this exact structure:
    {{
        "likely_condition": "Most probable disease/issue with brief description",
        "severity": "Healthy/Mild/Moderate/Severe", 
        "confidence": "High/Medium/Low",
        "quick_summary": "2-3 sentence explanation covering the condition, its causes, and potential impact",
        "immediate_action": "Detailed immediate steps to take within 24-48 hours (3-4 specific actions)",
        "treatment_steps": "Comprehensive treatment plan with methods, timing, and application details (4-6 detailed steps)",
        "what_to_watch": "Key symptoms and progression indicators to monitor, including timeframes (3-4 monitoring points)",
        "detailed_analysis": "Complete technical analysis in markdown format including differential diagnosis, pathophysiology, environmental factors, and long-term management"
    }}

    Provide practical, actionable advice with specific details like application rates, timing, and visual indicators. Make it informative enough for serious gardeners while remaining accessible.
    """

    # Get analysis from Gemini (let exceptions propagate)
    response = gemini_vision_model.invoke(analysis_prompt)
    
    try:
        # Try to parse JSON response
        import json
        response_text = response.content.strip()
        
        # Clean up response if it has markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        analysis_data = json.loads(response_text)
        
        return {
            "analysis": analysis_data.get("detailed_analysis", response.content),
            "model_used": "gemini-2.0-flash",
            "summary": analysis_data.get("quick_summary", "Analysis completed"),
            "severity": analysis_data.get("severity", "Unknown"),
            "likely_condition": analysis_data.get("likely_condition", ""),
            "confidence": analysis_data.get("confidence", "Medium"),
            "immediate_action": analysis_data.get("immediate_action", ""),
            "treatment_steps": analysis_data.get("treatment_steps", ""),
            "what_to_watch": analysis_data.get("what_to_watch", "")
        }
    except (json.JSONDecodeError, KeyError) as e:
        # Fallback to original processing if JSON parsing fails
        content = response.content
        summary = ""
        
        # Extract first meaningful sentence as summary
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                summary = line.strip()[:150] + "..." if len(line.strip()) > 150 else line.strip()
                break
        
        return {
            "analysis": content,
            "model_used": "gemini-2.0-flash",
            "summary": summary
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
    Provide comprehensive care guidelines for {plant_type} in JSON format.

    Return your response as a valid JSON object with this exact structure:
    {{
        "care_difficulty": "Easy/Moderate/Difficult",
        "quick_overview": "2-3 sentence overview covering the plant's nature, basic needs, and what makes it special",
        "essential_care": {{
            "light": "Detailed light requirements with specific conditions, duration, and positioning tips",
            "water": "Comprehensive watering guidelines including frequency, amount, seasonal changes, and soil moisture indicators",
            "soil": "Specific soil requirements including pH, drainage, nutrients, and recommended mixes or amendments"
        }},
        "key_tips": [
            "Detailed tip 1 with specific techniques or timing",
            "Detailed tip 2 with measurements or indicators", 
            "Detailed tip 3 with troubleshooting guidance",
            "Detailed tip 4 with seasonal considerations",
            "Detailed tip 5 with growth optimization"
        ],
        "common_problems": [
            "Problem 1: detailed description, causes, and step-by-step solution",
            "Problem 2: detailed description, causes, and step-by-step solution",
            "Problem 3: detailed description, causes, and step-by-step solution"
        ],
        "detailed_guide": "Comprehensive care guide in markdown format with advanced techniques, seasonal care, propagation, fertilization schedules, pruning guidelines, and troubleshooting"
    }}

    Provide detailed, actionable information that goes beyond basics. Include specific measurements, timing, visual cues, and professional tips while remaining accessible to dedicated home gardeners.
    """

    # Get care tips from Gemini (let exceptions propagate)
    response = gemini_vision_model.invoke(care_prompt)
    
    try:
        # Try to parse JSON response
        import json
        response_text = response.content.strip()
        
        # Clean up response if it has markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        care_data = json.loads(response_text)
        
        return {
            "care_tips": care_data.get("detailed_guide", response.content),
            "plant_type": plant_type,
            "model_used": "gemini-2.0-flash",
            "care_difficulty": care_data.get("care_difficulty", "Moderate"),
            "quick_overview": care_data.get("quick_overview", ""),
            "essential_care": care_data.get("essential_care", {}),
            "key_tips": care_data.get("key_tips", []),
            "common_problems": care_data.get("common_problems", [])
        }
    except (json.JSONDecodeError, KeyError) as e:
        # Fallback to original processing if JSON parsing fails
        content = response.content
        care_difficulty = "Moderate"
        
        if any(word in content.lower() for word in ["easy", "beginner", "low maintenance", "simple"]):
            care_difficulty = "Easy"
        elif any(word in content.lower() for word in ["difficult", "advanced", "challenging", "expert"]):
            care_difficulty = "Difficult"
        
        return {
            "care_tips": content,
            "plant_type": plant_type,
            "model_used": "gemini-2.0-flash",
            "care_difficulty": care_difficulty
        }