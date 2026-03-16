"""
OpenRouter vision model initialisation.

OpenRouter exposes an OpenAI-compatible endpoint so we use ChatOpenAI
with a custom base_url.  The default image model is configurable via
OPENROUTER_IMAGE_MODEL in .env (defaults to google/gemini-2.0-flash).
"""

from functools import lru_cache

from app.core.config import settings


@lru_cache(maxsize=1)
def get_openrouter_vision_model():
    """Return OpenRouter vision model, or None when key is missing."""
    if not settings.OPENROUTER_API_KEY:
        return None

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.OPENROUTER_IMAGE_MODEL,
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
        temperature=0.1,
        default_headers={
            "HTTP-Referer": "https://leaf-disease-detection",
            "X-Title": "Leaf Disease Detection",
        },
        max_tokens=1000,
    )
