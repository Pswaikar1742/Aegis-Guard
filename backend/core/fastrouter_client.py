from __future__ import annotations

import json
import re
import time
from functools import lru_cache
from typing import Any, Sequence

from openai import OpenAI

from core.config import settings


JSON_OBJECT_PATTERN = re.compile(r"\{.*\}", re.DOTALL)


def _parse_json_object(raw_content: str) -> dict[str, Any]:
    text = (raw_content or "").strip()
    if not text:
        raise ValueError("Model returned an empty payload.")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = JSON_OBJECT_PATTERN.search(text)
        if not match:
            raise
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("Model response was JSON but not a JSON object.")
    return parsed


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    return OpenAI(
        api_key=settings.fastrouter_api_key,
        base_url=settings.fastrouter_base_url,
        timeout=settings.fastrouter_request_timeout_sec,
    )


def _request_completion(
    *,
    client: OpenAI,
    model: str,
    messages: list[dict[str, Any]],
    temperature: float,
    max_tokens: int,
    prefer_json_format: bool,
):
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if prefer_json_format:
        kwargs["response_format"] = {"type": "json_object"}
    return client.chat.completions.create(**kwargs)


def call_json_with_fallback(
    *,
    models: Sequence[str],
    messages: list[dict[str, Any]],
    temperature: float = 0.0,
    max_tokens: int = 1200,
    max_retries_per_model: int | None = None,
    retry_backoff_sec: float | None = None,
) -> tuple[dict[str, Any], str]:
    if not models:
        raise ValueError("At least one model must be configured for FastRouter calls.")

    retries = (
        settings.fastrouter_max_retries_per_model
        if max_retries_per_model is None
        else max_retries_per_model
    )
    backoff = (
        settings.fastrouter_retry_backoff_sec if retry_backoff_sec is None else retry_backoff_sec
    )
    if retries < 0:
        raise ValueError("max_retries_per_model cannot be negative.")

    client = _get_client()
    failures: list[str] = []

    for model in models:
        max_attempts = retries + 1
        for attempt in range(1, max_attempts + 1):
            completion = None
            try:
                completion = _request_completion(
                    client=client,
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    prefer_json_format=True,
                )
            except Exception:
                try:
                    completion = _request_completion(
                        client=client,
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        prefer_json_format=False,
                    )
                except Exception as exc:
                    failures.append(f"{model} attempt {attempt}/{max_attempts}: request failed ({exc})")
                    if attempt < max_attempts and backoff > 0:
                        time.sleep(backoff * (2 ** (attempt - 1)))
                    continue

            try:
                content = completion.choices[0].message.content if completion.choices else ""
                payload = _parse_json_object(content or "")
            except Exception as exc:
                failures.append(
                    f"{model} attempt {attempt}/{max_attempts}: invalid JSON response ({exc})"
                )
                if attempt < max_attempts and backoff > 0:
                    time.sleep(backoff * (2 ** (attempt - 1)))
                continue

            return payload, model

    raise RuntimeError("All FastRouter model calls failed. " + " | ".join(failures[:20]))
