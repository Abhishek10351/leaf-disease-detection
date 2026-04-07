"""Single-model factory for leaf disease detection."""

from functools import lru_cache

from app.core.config import settings

_BASE_URL = "https://openrouter.ai/api/v1"
_HEADERS = {
    "HTTP-Referer": "https://leaf-disease-detection",
    "X-Title": "Leaf Disease Detection",
}

# Single active model for lower latency.
ACTIVE_MODEL_ID = "qwen/qwen3.5-9b"
ACTIVE_MODEL_ID = "nemotron-nano-12b-v2-vl:free"



def _make_model(model_id: str, max_tokens: int):
    """Construct a ChatOpenAI instance for the given model."""
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model_id,
        base_url=_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        temperature=0.1,
        default_headers=_HEADERS,
        max_tokens=max_tokens,
    )


@lru_cache(maxsize=1)
def get_single_model():
    """Return the single model used for text analysis."""
    return _make_model(
        ACTIVE_MODEL_ID,
        settings.OPENROUTER_TEXT_MAX_TOKENS,
    )


@lru_cache(maxsize=1)
def get_vision_model():
    """Return the single model used for vision analysis."""
    return _make_model(
        ACTIVE_MODEL_ID,
        settings.OPENROUTER_VISION_MAX_TOKENS,
    )


def ensemble_invoke_text(prompt: str) -> list[str]:
    """Compatibility helper that returns one response from the single active model."""
    result = get_single_model().invoke(prompt)
    content = result.content if hasattr(result, "content") else str(result)
    return [content] if content and content.strip() else []


def ensemble_invoke_vision(messages: list) -> list[str]:
    """Compatibility helper that returns one response from the single active model."""
    result = get_vision_model().invoke(messages)
    content = result.content if hasattr(result, "content") else str(result)
    return [content] if content and content.strip() else []
