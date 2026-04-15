from typing import Optional, Type, TypeVar

from pydantic import BaseModel

from app.models.analysis import (
    ImageAnalysisLLMResponse,
    PlantCareLLMResponse,
    SymptomsAnalysisLLMResponse,
)
from .ensemble import ensemble_invoke_text, ensemble_invoke_vision, get_single_model

StructuredModel = TypeVar("StructuredModel", bound=BaseModel)


class LeafAnalysisUtils:
    """Leaf analysis using single model direct structured output."""

    @staticmethod
    def _is_truncation_or_parse_error(exc: Exception) -> bool:
        """Detect model truncation/parse failures that merit a constrained retry."""
        msg = str(exc).lower()
        markers = [
            "length limit",
            "could not parse response content",
            "output parser",
            "validation error",
            "none type",
            "nonetype",
        ]
        return any(marker in msg for marker in markers)

    def _invoke_structured_text_with_retry(
        self,
        schema: Type[StructuredModel],
        primary_prompt: str,
        fallback_prompt: str,
    ) -> StructuredModel:
        """Run structured text invocation and retry once with tighter output bounds."""
        try:
            response = ensemble_invoke_text(primary_prompt, schema=schema)
            if response is None:
                raise RuntimeError("Ensemble returned None response")
            return response
        except Exception as exc:
            if not self._is_truncation_or_parse_error(exc):
                raise

        response = ensemble_invoke_text(fallback_prompt, schema=schema)
        if response is None:
            raise RuntimeError("Ensemble returned None response after retry")
        return response

    def _invoke_structured_vision_with_retry(
        self,
        schema: Type[StructuredModel],
        image_base64: str,
        primary_prompt: str,
        fallback_prompt: str,
    ) -> StructuredModel:
        """Run structured vision invocation and retry once with tighter output bounds."""
        try:
            response = ensemble_invoke_vision(
                image_base64=image_base64,
                prompt=primary_prompt,
                schema=schema,
            )
            if response is None:
                raise RuntimeError("Ensemble returned None response")
            return response
        except Exception as exc:
            if not self._is_truncation_or_parse_error(exc):
                raise

        response = ensemble_invoke_vision(
            image_base64=image_base64,
            prompt=fallback_prompt,
            schema=schema,
        )
        if response is None:
            raise RuntimeError("Ensemble returned None response after retry")
        return response

    @staticmethod
    def _language_instruction(language: str) -> str:
        """Return language-specific output instruction for narrative fields."""
        if language == "hi":
            return (
                "Language requirement: Write all narrative/explanatory fields in Hindi (Devanagari). "
                "Use simple daily Hindi words that common farmers can understand; avoid overly literary or highly technical vocabulary. "
                "Keep constrained enum fields exactly in English as required by schema "
                "(health_status: Healthy/Mild/Moderate/Severe; confidence: High/Medium/Low; "
                "care_difficulty: Easy/Moderate/Difficult)."
            )
        if language == "as":
            return (
                "Language requirement: Write all narrative/explanatory fields in Assamese (Axomiya, Assamese script). "
                "Use simple daily Assamese words that common farmers can understand; avoid overly literary or highly technical vocabulary. "
                "Keep constrained enum fields exactly in English as required by schema "
                "(health_status: Healthy/Mild/Moderate/Severe; confidence: High/Medium/Low; "
                "care_difficulty: Easy/Moderate/Difficult)."
            )
        if language == "brx":
            return (
                "Language requirement: Write all narrative/explanatory fields in Bodo language EXCLUSIVELY in Devanagari script generally used in BODO language. "
                "Do NOT use Latin characters or any other script for Bodo narrative fields. "
                "Use simple daily Bodo words that common farmers can understand; avoid overly literary or highly technical vocabulary. "
                "Keep constrained enum fields exactly in English as required by schema "
                "(health_status: Healthy/Mild/Moderate/Severe; confidence: High/Medium/Low; "
                "care_difficulty: Easy/Moderate/Difficult)."
            )
        return (
            "Language requirement: Write all response content in English. "
            "Use very simple everyday English that common farmers can understand; avoid advanced or technical jargon."
        )

    @staticmethod
    def _simplicity_instruction() -> str:
        """Force plain-language, easy-to-understand communication style."""
        return (
            "Simplicity requirement: Use short, clear sentences and common everyday words. "
            "Explain any unavoidable technical term in plain language immediately. "
            "Keep tone practical, direct, and easy for non-experts to follow."
        )

    @staticmethod
    def _formatting_instruction() -> str:
        """Keep outputs visually clean and easy to scan in the UI."""
        return (
            "Formatting requirement: Keep output clean and scannable. "
            "Use short markdown bullet points with '-' for steps and actions. "
            "Avoid repeating the same advice in different sections. "
            "Do not add long introductions or unnecessary filler text."
        )

    @staticmethod
    def _location_instruction(location_context: Optional[str]) -> str:
        """Return location-aware agricultural guidance when climate data is available."""
        if not location_context:
            return ""

        return (
            "Location and climate requirement: Use the following local weather and location context to tailor the diagnosis and advice. "
            "Prioritize diseases and management decisions that fit the user's climate, especially humidity-driven fungal pressure. "
            "If forecast conditions include rain or sustained humidity, avoid recommending contact sprays immediately before rainfall and prefer timing-aware extension guidance. "
            "If the climate suggests a humid subtropical or tropical pattern, bias the differential toward fungal diseases common in local crops such as rice, tea, banana, citrus, tomato, and leafy vegetables. "
            "Mandatory output rule: Keep quick_summary leaf-first (first sentence must describe observed leaf symptoms/details), and include weather impact in the next sentence. "
            "Also mention weather impact in immediate_action (or treatment_steps for symptom analysis). "
            "Use concrete weather words such as humidity, rain, precipitation, forecast, or climate. "
            f"Local context: {location_context}"
        )

    def analyze_leaf_image(
        self,
        image_base64: str,
        language: str = "en",
        location_context: Optional[str] = None,
    ) -> ImageAnalysisLLMResponse:
        """Analyze leaf image directly with vision model."""
        language_instruction = self._language_instruction(language)
        simplicity_instruction = self._simplicity_instruction()
        formatting_instruction = self._formatting_instruction()
        location_instruction = self._location_instruction(location_context)
        prompt_parts = [
            "You are an expert plant pathologist. Analyze this leaf image and provide a comprehensive diagnosis.",
            "Include: plant identification, severity, confidence, one primary issue, immediate actions, treatment plan, prevention strategy, and detailed markdown analysis with differential diagnosis.",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        fallback_parts = [
            "You are an expert plant pathologist. Analyze this leaf image and return a valid structured response.",
            "Keep each field complete but concise so the full response fits safely within output limits.",
            "Word limits: quick_summary 40-70 words, immediate_action 70-110 words, treatment 90-140 words, prevention 60-100 words, detailed_analysis 160-240 words in markdown with headings: Likely Diagnosis, Why This Matches, Differential Diagnosis, Treatment Plan, Monitoring and Escalation.",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        if location_instruction:
            prompt_parts.append(location_instruction)
            fallback_parts.append(location_instruction)

        prompt = "\n\n".join(prompt_parts)
        fallback_prompt = "\n\n".join(fallback_parts)
        return self._invoke_structured_vision_with_retry(
            schema=ImageAnalysisLLMResponse,
            image_base64=image_base64,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )

    def analyze_leaf_symptoms(
        self,
        symptoms_description: str,
        plant_type: str = "",
        language: str = "en",
        location_context: Optional[str] = None,
    ) -> SymptomsAnalysisLLMResponse:
        """Analyze leaf symptoms directly with qwen model."""
        language_instruction = self._language_instruction(language)
        simplicity_instruction = self._simplicity_instruction()
        formatting_instruction = self._formatting_instruction()
        location_instruction = self._location_instruction(location_context)
        plant_context = f"Plant type: {plant_type}\n" if plant_type else ""
        prompt_parts = [
            "You are an expert plant pathologist. Analyze these symptoms and provide a comprehensive diagnosis.",
            f"{plant_context}Symptoms: {symptoms_description}",
            "Provide: likely_condition, severity, confidence, quick_summary (2-3 sentences), immediate_action (3-4 steps), treatment_steps (4-6 steps with timing), what_to_watch (with time windows), and detailed_analysis (markdown with Likely Cause, Supporting Symptoms, Differential Diagnosis, Treatment Roadmap, Escalation Signs).",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        fallback_parts = [
            "You are an expert plant pathologist. Analyze these symptoms and return a valid structured response.",
            f"{plant_context}Symptoms: {symptoms_description}",
            "Keep outputs detailed but concise to avoid truncation.",
            "Word limits: quick_summary 40-70 words, immediate_action 70-110 words, treatment_steps 90-140 words, what_to_watch 60-100 words, detailed_analysis 160-240 words in markdown with sections: Likely Cause, Supporting Symptoms, Differential Diagnosis, Treatment Roadmap, Escalation Signs.",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        if location_instruction:
            prompt_parts.append(location_instruction)
            fallback_parts.append(location_instruction)

        prompt = "\n\n".join(prompt_parts)
        fallback_prompt = "\n\n".join(fallback_parts)
        return self._invoke_structured_text_with_retry(
            schema=SymptomsAnalysisLLMResponse,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )

    def get_plant_care_tips(
        self,
        plant_type: str,
        language: str = "en",
        location_context: Optional[str] = None,
    ) -> PlantCareLLMResponse:
        """Get plant care tips directly with qwen model."""
        language_instruction = self._language_instruction(language)
        simplicity_instruction = self._simplicity_instruction()
        formatting_instruction = self._formatting_instruction()
        location_instruction = self._location_instruction(location_context)
        prompt_parts = [
            f"Provide comprehensive care guidelines for {plant_type}.",
            "Include: care_difficulty (Easy/Moderate/Difficult), quick_overview (2-3 sentences), essential_care (light, water, soil), key_tips (exactly 5 bullets), common_problems (exactly 3 bullets), and detailed_guide (markdown with Environment Setup, Routine Care, Seasonal Adjustments, Troubleshooting).",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        fallback_parts = [
            f"Provide comprehensive care guidelines for {plant_type} and return a valid structured response.",
            "Keep content detailed but concise to avoid truncation.",
            "Word limits: quick_overview 40-70 words; essential_care.light 40-70 words; essential_care.water 40-70 words; essential_care.soil 40-70 words; each key_tip 12-24 words; each common_problem 18-36 words; detailed_guide 160-240 words in markdown with Environment Setup, Routine Care, Seasonal Adjustments, Troubleshooting.",
            language_instruction,
            simplicity_instruction,
            formatting_instruction,
        ]
        if location_instruction:
            prompt_parts.append(location_instruction)
            fallback_parts.append(location_instruction)

        prompt = "\n\n".join(prompt_parts)
        fallback_prompt = "\n\n".join(fallback_parts)
        return self._invoke_structured_text_with_retry(
            schema=PlantCareLLMResponse,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )

    def translate_image_analysis(
        self,
        response: ImageAnalysisLLMResponse,
        source_language: str,
        target_language: str,
    ) -> ImageAnalysisLLMResponse:
        """Translate an existing image analysis response using the final verifier model only."""
        if source_language == target_language:
            return response

        language_instruction = self._language_instruction(target_language)
        simplicity_instruction = self._simplicity_instruction()
        formatting_instruction = self._formatting_instruction()

        prompt = (
            "You are a translation and quality verifier for plant analysis responses. "
            "Translate only narrative fields to the target language while preserving meaning and practical steps. "
            "Do not change enum fields: health_status, confidence. "
            "Do not add or remove key recommendations.\n\n"
            f"Source language: {source_language}\n"
            f"Target language: {target_language}\n"
            f"{language_instruction}\n"
            f"{simplicity_instruction}\n"
            f"{formatting_instruction}\n\n"
            f"Input JSON:\n{response.model_dump_json(indent=2)}"
        )

        model = get_single_model().with_structured_output(ImageAnalysisLLMResponse)
        translated = model.invoke(prompt)
        if translated is None:
            raise RuntimeError("Translation model returned None response")
        return translated