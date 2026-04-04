"""OpenRouter helpers — embeddings only.

Text and vision inference are handled by the ensemble pipeline in ensemble.py.
"""

from functools import lru_cache

from app.core.config import settings


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_HEADERS = {
    "HTTP-Referer": "https://leaf-disease-detection",
    "X-Title": "Leaf Disease Detection",
}



@lru_cache(maxsize=1)
def get_openrouter_embedding_model():
    """Return configured OpenRouter embedding model."""
    if not settings.OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")

    from langchain_openai import OpenAIEmbeddings

    embedding_model = getattr(settings, "OPENROUTER_EMBEDDING_MODEL", "text-embedding-3-small")

    return OpenAIEmbeddings(
        model=embedding_model,
        base_url=OPENROUTER_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        default_headers=OPENROUTER_DEFAULT_HEADERS,
    )
