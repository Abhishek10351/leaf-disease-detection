from .ensemble import ensemble_invoke_text, ensemble_invoke_vision, synthesize_structured
from app.models.analysis import ImageAnalysisLLMResponse, SymptomsAnalysisLLMResponse, PlantCareLLMResponse
from langchain_core.messages import HumanMessage


class LeafAnalysisUtils:
    """Leaf analysis using an ensemble of three LLMs synthesized into one response."""

    def analyze_leaf_image(self, image_base64: str) -> ImageAnalysisLLMResponse:
        """
        Analyze a leaf image via ensemble vision models then a single synthesizer.

        Each of the three ensemble models independently examines the image;
        their plain-text outputs are fed to the synthesizer which produces a
        single structured ImageAnalysisLLMResponse.
        """
        prompt = "You are an expert plant pathologist. Analyze this leaf image and provide a comprehensive diagnosis."
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                },
            ]
        )
        responses = ensemble_invoke_vision([message])
        synthesis_context = (
            "You are an expert plant pathologist. "
            "Using the following ensemble analyses of a leaf image, "
            "produce a single unified, comprehensive diagnosis."
        )
        return synthesize_structured(responses, synthesis_context, ImageAnalysisLLMResponse)

    def analyze_leaf_symptoms(
        self, symptoms_description: str, plant_type: str = ""
    ) -> SymptomsAnalysisLLMResponse:
        """
        Analyze leaf symptoms via ensemble text models then a single synthesizer.
        """
        plant_context = f"Plant type: {plant_type}\n" if plant_type else ""
        prompt = (
            "You are an expert plant pathologist. "
            "Analyze these symptoms and provide a comprehensive diagnosis.\n\n"
            f"{plant_context}Symptoms: {symptoms_description}"
        )
        responses = ensemble_invoke_text(prompt)
        synthesis_context = (
            "You are an expert plant pathologist synthesizing analyses for the following case:\n"
            f"{plant_context}Symptoms: {symptoms_description}\n"
            "Produce a single unified, accurate diagnosis."
        )
        return synthesize_structured(responses, synthesis_context, SymptomsAnalysisLLMResponse)

    def get_plant_care_tips(self, plant_type: str) -> PlantCareLLMResponse:
        """
        Get plant care tips via ensemble text models then a single synthesizer.
        """
        prompt = (
            f"Provide comprehensive care guidelines for {plant_type}. "
            "Keep the response concise but complete: "
            "quick_overview 2-3 sentences, key_tips exactly 5 short bullets, "
            "common_problems exactly 3 short bullets, and detailed_guide under 400 words."
        )
        responses = ensemble_invoke_text(prompt)
        synthesis_context = (
            f"Provide comprehensive but concise care guidelines for {plant_type}. "
            "Use the expert analyses below to produce the final structured output. "
            "quick_overview 2-3 sentences, key_tips exactly 5 short bullets, "
            "common_problems exactly 3 short bullets, detailed_guide under 400 words."
        )
        return synthesize_structured(responses, synthesis_context, PlantCareLLMResponse)