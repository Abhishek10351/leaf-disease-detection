"""OpenRouter ensemble helpers for text and vision analysis.

Text analysis uses a lightweight primary model with a fallback model on failure.
Vision analysis can still compare multiple small models, then a final verifier
model cleans and validates the output.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Optional, Type, TypeVar

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.core.config import settings

StructuredModel = TypeVar("StructuredModel", bound=BaseModel)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_HEADERS = {
    "HTTP-Referer": "https://leaf-disease-detection",
    "X-Title": "Leaf Disease Detection",
}

# Keep model pools lightweight for testing.
TEXT_ENSEMBLE_MODEL_IDS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-4-26b-a4b-it",
]
VISION_ENSEMBLE_MODEL_IDS = [
    "google/gemma-4-26b-a4b-it",
    "nvidia/nemotron-nano-12b-v2-vl",
]
FINAL_VERIFIER_MODEL_ID = "qwen/qwen3-235b-a22b-2507"


def _require_api_key() -> str:
    if not settings.OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")
    return settings.OPENROUTER_API_KEY


def _build_chat_model(model_id: str, *, max_tokens: int) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_id,
        base_url=OPENROUTER_BASE_URL,
        api_key=_require_api_key(),
        temperature=0.1,
        default_headers=OPENROUTER_DEFAULT_HEADERS,
        max_tokens=max_tokens,
    )


@lru_cache(maxsize=1)
def _get_text_models() -> tuple[ChatOpenAI, ...]:
    return tuple(
        _build_chat_model(model_id, max_tokens=settings.OPENROUTER_TEXT_MAX_TOKENS)
        for model_id in TEXT_ENSEMBLE_MODEL_IDS
    )


@lru_cache(maxsize=1)
def _get_vision_models() -> tuple[ChatOpenAI, ...]:
    return tuple(
        _build_chat_model(model_id, max_tokens=settings.OPENROUTER_VISION_MAX_TOKENS)
        for model_id in VISION_ENSEMBLE_MODEL_IDS
    )


@lru_cache(maxsize=1)
def _get_final_verifier_model() -> ChatOpenAI:
    return _build_chat_model(
        FINAL_VERIFIER_MODEL_ID,
        max_tokens=settings.OPENROUTER_TEXT_MAX_TOKENS,
    )


def get_single_model() -> ChatOpenAI:
    """Return the final verifier model for compatibility with older code paths."""
    return _get_final_verifier_model()


def get_vision_model() -> ChatOpenAI:
    """Return the final verifier model for compatibility with older code paths."""
    return _get_final_verifier_model()


def _extract_response_text(response: Any) -> str:
    if response is None:
        return ""
    if hasattr(response, "content"):
        return str(response.content or "").strip()
    return str(response).strip()


def _invoke_one_text_model(model: ChatOpenAI, prompt: str, model_id: str) -> str:
    try:
        response = model.invoke(prompt)
        return _extract_response_text(response)
    except Exception as exc:
        print(f"⚠️  Text model '{model_id}' failed: {exc}")
        return ""


def _invoke_one_vision_model(
    model: ChatOpenAI,
    prompt: str,
    image_base64: str,
    model_id: str,
) -> str:
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                },
            ]
        )
    ]

    try:
        response = model.invoke(messages)
        return _extract_response_text(response)
    except Exception as exc:
        print(f"⚠️  Vision model '{model_id}' failed: {exc}")
        return ""


def _run_text_with_fallback(prompt: str) -> str:
    models = list(_get_text_models())
    for index, model in enumerate(models):
        response = _invoke_one_text_model(model, prompt, TEXT_ENSEMBLE_MODEL_IDS[index])
        if response:
            return response
    return ""


def _run_parallel_vision(prompt: str, image_base64: str) -> list[str]:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    models = list(_get_vision_models())
    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {
            pool.submit(
                _invoke_one_vision_model,
                model,
                prompt,
                image_base64,
                VISION_ENSEMBLE_MODEL_IDS[index],
            ): index
            for index, model in enumerate(models)
        }
        ordered = [""] * len(models)
        for future in as_completed(futures):
            ordered[futures[future]] = future.result()
    return [item for item in ordered if item.strip()]


def _build_merge_prompt(user_prompt: str, responses: list[str]) -> str:
    numbered_responses = "\n\n".join(
        f"Expert response {index + 1}:\n{response}"
        for index, response in enumerate(responses)
    )
    return (
        "You are the final verifier and merger model. "
        "Review the expert responses, remove duplicates, resolve contradictions, "
        "and keep only the most reliable answer. "
        "Use plain, clear language and keep the final answer concise.\n\n"
        f"Original task:\n{user_prompt}\n\n"
        f"Expert responses:\n{numbered_responses}"
    )


def _merge_with_final_model(
    user_prompt: str,
    responses: list[str],
    schema: Optional[Type[StructuredModel]] = None,
) -> Any:
    if not responses:
        raise RuntimeError("All ensemble models failed to respond.")

    merge_prompt = _build_merge_prompt(user_prompt, responses)
    verifier = _get_final_verifier_model()

    if schema is None:
        return verifier.invoke(merge_prompt)

    verifier_with_schema = verifier.with_structured_output(schema)
    return verifier_with_schema.invoke(merge_prompt)


def ensemble_invoke_text(
    prompt: str,
    schema: Optional[Type[StructuredModel]] = None,
) -> Any:
    """Run one lightweight text model, fallback if needed, then verify with the final model."""
    response = _run_text_with_fallback(prompt)
    if not response:
        raise RuntimeError("All text models failed to respond.")

    merge_prompt = _build_merge_prompt(prompt, [response])
    verifier = _get_final_verifier_model()
    if schema is None:
        return verifier.invoke(merge_prompt)

    verifier_with_schema = verifier.with_structured_output(schema)
    return verifier_with_schema.invoke(merge_prompt)


def ensemble_invoke_vision(
    image_base64: str,
    prompt: str,
    schema: Optional[Type[StructuredModel]] = None,
) -> Any:
    """Run vision models in parallel, then merge and verify with the final model."""
    responses = _run_parallel_vision(prompt, image_base64)
    return _merge_with_final_model(prompt, responses, schema=schema)
