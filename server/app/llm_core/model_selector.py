"""
Centralized model access — thin wrappers kept for backward compatibility.

Full analysis now goes through the ensemble pipeline in ensemble.py.
These helpers return the synthesizer model for any code that still needs
a single ChatOpenAI instance.
"""

from .ensemble import get_synthesizer


def get_text_model():
    """Return the synthesizer model (used as fallback single-model access)."""
    return get_synthesizer()


def get_vision_model():
    """Return the synthesizer model (used as fallback single-model access)."""
    return get_synthesizer()
