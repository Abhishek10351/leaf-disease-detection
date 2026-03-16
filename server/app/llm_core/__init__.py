"""
LLM Core Module

Provides LLM-powered analysis for leaf disease detection using:
- OpenRouter for image analysis (OPENROUTER_IMAGE_MODEL)
- OpenRouter for text analysis (OPENROUTER_TEXT_MODEL)
- Structured outputs via LangChain
"""

from functools import lru_cache

from .utils import LeafAnalysisUtils
from .model_selector import get_text_model, get_vision_model


@lru_cache(maxsize=1)
def get_leaf_analysis() -> LeafAnalysisUtils:
    """Return cached analysis service instance."""
    return LeafAnalysisUtils()


__all__ = [
    "LeafAnalysisUtils",
    "get_leaf_analysis",
    "get_text_model",
    "get_vision_model",
]
