"""
LLM Core Module

Provides LLM-powered analysis for leaf disease detection using a single
OpenRouter model as the primary approach, with ensemble functions available
for fallback or multi-model scenarios.
"""

from functools import lru_cache

from .utils import LeafAnalysisUtils
from .ensemble import (
    ensemble_invoke_text,
    ensemble_invoke_vision,
    get_single_model,
    get_vision_model,
)


@lru_cache(maxsize=1)
def get_leaf_analysis() -> LeafAnalysisUtils:
    """Return cached analysis service instance."""
    return LeafAnalysisUtils()


__all__ = [
    "LeafAnalysisUtils",
    "get_leaf_analysis",
    "get_single_model",
    "get_vision_model",
    "ensemble_invoke_text",
    "ensemble_invoke_vision",
]
