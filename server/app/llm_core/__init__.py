"""
LLM Core Module

Provides LLM-powered analysis for leaf disease detection using an ensemble of
three OpenRouter models (parallel inference) synthesized by a single aggregator:
  - google/gemma-3-12b-it:free
  - nvidia/nemotron-nano-12b-v2-vl:free
  - qwen/qwen3.5-35b-a3b
All structured outputs are produced by the synthesizer via LangChain.
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
