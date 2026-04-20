from __future__ import annotations

import json
import re
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
        timeout=45.0,
    )


def call_json_with_fallback(
    *,
    models: Sequence[str],
    messages: list[dict[str, Any]],
    temperature: float = 0.0,
    max_tokens: int = 1200,
) -> tuple[dict[str, Any], str]:
    if not models:
        raise ValueError("At least one model must be configured for FastRouter calls.")

    client = _get_client()
    failures: list[str] = []

    for model in models:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
        except Exception:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except Exception as exc:
                failures.append(f"{model}: {exc}")
                continue

        try:
            content = completion.choices[0].message.content if completion.choices else ""
            payload = _parse_json_object(content or "")
        except Exception as exc:
            failures.append(f"{model}: invalid JSON response ({exc})")
            continue

        return payload, model

    raise RuntimeError("All FastRouter model calls failed. " + " | ".join(failures))
