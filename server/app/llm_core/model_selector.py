"""
Centralized model selection for text and vision tasks.

This keeps provider selection in one place and avoids scattered fallback logic.
"""

from .openrouter_model import get_openrouter_text_model, get_openrouter_vision_model


def get_text_model():
    """Return OpenRouter text model."""
    return get_openrouter_text_model()


def get_vision_model():
    """Return OpenRouter vision model."""
    return get_openrouter_vision_model()
