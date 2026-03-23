from typing import Type, TypeVar

from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from app.models.analysis import (
    ImageAnalysisLLMResponse,
    PlantCareLLMResponse,
    SymptomsAnalysisLLMResponse,
)
from .ensemble import get_single_model, get_vision_model

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
        model,
        schema: Type[StructuredModel],
        primary_prompt: str,
        fallback_prompt: str,
    ) -> StructuredModel:
        """Run structured text invocation and retry once with tighter output bounds."""
        structured_model = model.with_structured_output(schema)
        try:
            response = structured_model.invoke(primary_prompt)
            if response is None:
                raise RuntimeError("Model returned None response")
            return response
        except Exception as exc:
            if not self._is_truncation_or_parse_error(exc):
                raise

        response = structured_model.invoke(fallback_prompt)
        if response is None:
            raise RuntimeError("Model returned None response after retry")
        return response

    def _invoke_structured_vision_with_retry(
        self,
        model,
        schema: Type[StructuredModel],
        image_base64: str,
        primary_prompt: str,
        fallback_prompt: str,
    ) -> StructuredModel:
        """Run structured vision invocation and retry once with tighter output bounds."""
        structured_model = model.with_structured_output(schema)

        def _build_message(prompt_text: str) -> list[HumanMessage]:
            return [
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ]
                )
            ]

        try:
            response = structured_model.invoke(_build_message(primary_prompt))
            if response is None:
                raise RuntimeError("Model returned None response")
            return response
        except Exception as exc:
            if not self._is_truncation_or_parse_error(exc):
                raise

        response = structured_model.invoke(_build_message(fallback_prompt))
        if response is None:
            raise RuntimeError("Model returned None response after retry")
        return response

    def analyze_leaf_image(self, image_base64: str) -> ImageAnalysisLLMResponse:
        """Analyze leaf image directly with vision model."""
        prompt = (
            "You are an expert plant pathologist. Analyze this leaf image and provide a comprehensive diagnosis. "
            "Include: plant identification, severity, confidence, one primary issue, immediate actions, treatment plan, prevention strategy, and detailed markdown analysis with differential diagnosis."
        )
        fallback_prompt = (
            "You are an expert plant pathologist. Analyze this leaf image and return a valid structured response. "
            "Keep each field complete but concise so the full response fits safely within output limits. "
            "Word limits: quick_summary 60-90 words, immediate_action 90-140 words, treatment 120-180 words, "
            "prevention 80-130 words, detailed_analysis 220-320 words in markdown with headings: Likely Diagnosis, "
            "Why This Matches, Differential Diagnosis, Treatment Plan, Monitoring and Escalation."
        )
        model = get_vision_model()
        return self._invoke_structured_vision_with_retry(
            model=model,
            schema=ImageAnalysisLLMResponse,
            image_base64=image_base64,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )

    def analyze_leaf_symptoms(
        self, symptoms_description: str, plant_type: str = ""
    ) -> SymptomsAnalysisLLMResponse:
        """Analyze leaf symptoms directly with qwen model."""
        plant_context = f"Plant type: {plant_type}\n" if plant_type else ""
        prompt = (
            "You are an expert plant pathologist. "
            "Analyze these symptoms and provide a comprehensive diagnosis.\n\n"
            f"{plant_context}Symptoms: {symptoms_description}\n\n"
            "Provide: likely_condition, severity, confidence, quick_summary (2-3 sentences), "
            "immediate_action (3-4 steps), treatment_steps (4-6 steps with timing), "
            "what_to_watch (with time windows), and detailed_analysis (markdown with Likely Cause, Supporting Symptoms, Differential Diagnosis, Treatment Roadmap, Escalation Signs)."
        )
        fallback_prompt = (
            "You are an expert plant pathologist. Analyze these symptoms and return a valid structured response.\n\n"
            f"{plant_context}Symptoms: {symptoms_description}\n\n"
            "Keep outputs detailed but concise to avoid truncation. "
            "Word limits: quick_summary 60-90 words, immediate_action 90-140 words, treatment_steps 120-180 words, "
            "what_to_watch 80-130 words, detailed_analysis 220-320 words in markdown with sections: Likely Cause, "
            "Supporting Symptoms, Differential Diagnosis, Treatment Roadmap, Escalation Signs."
        )
        model = get_single_model()
        return self._invoke_structured_text_with_retry(
            model=model,
            schema=SymptomsAnalysisLLMResponse,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )

    def get_plant_care_tips(self, plant_type: str) -> PlantCareLLMResponse:
        """Get plant care tips directly with qwen model."""
        prompt = (
            f"Provide comprehensive care guidelines for {plant_type}.\n\n"
            "Include: care_difficulty (Easy/Moderate/Difficult), quick_overview (2-3 sentences), "
            "essential_care (light, water, soil), key_tips (exactly 5 bullets), "
            "common_problems (exactly 3 bullets), and detailed_guide (markdown with Environment Setup, Routine Care, Seasonal Adjustments, Troubleshooting)."
        )
        fallback_prompt = (
            f"Provide comprehensive care guidelines for {plant_type} and return a valid structured response.\n\n"
            "Keep content detailed but concise to avoid truncation. "
            "Word limits: quick_overview 60-90 words; essential_care.light 60-90 words; essential_care.water 60-90 words; "
            "essential_care.soil 60-90 words; each key_tip 20-35 words; each common_problem 30-50 words; "
            "detailed_guide 220-320 words in markdown with Environment Setup, Routine Care, Seasonal Adjustments, Troubleshooting."
        )
        model = get_single_model()
        return self._invoke_structured_text_with_retry(
            model=model,
            schema=PlantCareLLMResponse,
            primary_prompt=prompt,
            fallback_prompt=fallback_prompt,
        )