"""
Ensemble LLM runner.

Invokes the three ensemble models in parallel (text or vision), collects their
plain-text responses, then feeds them through a single synthesizer model to
produce one structured output.

Ensemble members:
  1. google/gemma-3-12b-it:free
  2. nvidia/nemotron-nano-12b-v2-vl:free
  3. qwen/qwen3.5-35b-a3b

Synthesizer: settings.OPENROUTER_SYNTHESIZER_MODEL (default: qwen/qwen3.5-35b-a3b)
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import Type, TypeVar

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")

_BASE_URL = "https://openrouter.ai/api/v1"
_HEADERS = {
    "HTTP-Referer": "https://leaf-disease-detection",
    "X-Title": "Leaf Disease Detection",
}

# All three ensemble members — every model here is vision-capable
ENSEMBLE_MODEL_IDS: list[str] = [
    "google/gemma-3-12b-it:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "qwen/qwen3.5-35b-a3b",
]


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
def _ensemble_text_models() -> tuple:
    """Cached tuple of ChatOpenAI instances for text-only ensemble."""
    return tuple(
        _make_model(mid, settings.OPENROUTER_TEXT_MAX_TOKENS)
        for mid in ENSEMBLE_MODEL_IDS
    )


@lru_cache(maxsize=1)
def _ensemble_vision_models() -> tuple:
    """Cached tuple of ChatOpenAI instances for vision ensemble."""
    return tuple(
        _make_model(mid, settings.OPENROUTER_VISION_MAX_TOKENS)
        for mid in ENSEMBLE_MODEL_IDS
    )


@lru_cache(maxsize=1)
def get_synthesizer():
    """Return the single synthesizer model that aggregates ensemble outputs."""
    return _make_model(
        settings.OPENROUTER_SYNTHESIZER_MODEL,
        settings.OPENROUTER_TEXT_MAX_TOKENS,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _invoke_one(model, prompt, model_label: str) -> str:
    """Call one model; return empty string on failure so others still proceed."""
    try:
        result = model.invoke(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as exc:
        logger.warning("Ensemble model '%s' failed: %s", model_label, exc)
        return ""


def _run_parallel(models: tuple, prompt) -> list[str]:
    """Submit all models in parallel; return only non-empty responses in original order."""
    labels = ENSEMBLE_MODEL_IDS[: len(models)]
    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {
            pool.submit(_invoke_one, m, prompt, labels[i]): i
            for i, m in enumerate(models)
        }
        ordered: list[str] = [""] * len(models)
        for fut in as_completed(futures):
            ordered[futures[fut]] = fut.result()
    return [r for r in ordered if r.strip()]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ensemble_invoke_text(prompt: str) -> list[str]:
    """
    Run all ensemble models with a text prompt in parallel.

    Returns:
        List of non-empty response strings (preserving original model order).
    """
    return _run_parallel(_ensemble_text_models(), prompt)


def ensemble_invoke_vision(messages: list) -> list[str]:
    """
    Run all ensemble models with a vision message list in parallel.

    Returns:
        List of non-empty response strings (preserving original model order).
    """
    return _run_parallel(_ensemble_vision_models(), messages)


def synthesize_structured(
    responses: list[str],
    synthesis_context: str,
    schema: Type[T],
) -> T:
    """
    Feed ensemble responses into the synthesizer to produce structured output.

    Args:
        responses: Plain-text outputs collected from the ensemble models.
        synthesis_context: Instructions / original query for the synthesizer.
        schema: Pydantic model class defining the desired output structure.

    Returns:
        An instance of `schema` populated by the synthesizer.

    Raises:
        RuntimeError: If every ensemble model failed to respond.
    """
    if not responses:
        raise RuntimeError(
            "All ensemble models failed to respond — cannot synthesize output."
        )

    joined = "\n\n".join(
        f"--- Expert Analysis {i + 1} ---\n{r}" for i, r in enumerate(responses)
    )
    full_prompt = (
        f"{synthesis_context}\n\n"
        f"{len(responses)} expert AI model(s) have analyzed the input. "
        "Synthesize their findings into one accurate, comprehensive response:\n\n"
        f"{joined}"
    )

    return get_synthesizer().with_structured_output(schema).invoke(full_prompt)
