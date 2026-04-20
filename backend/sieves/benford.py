from __future__ import annotations

import math
import re

from core.config import settings
from core.fastrouter_client import call_json_with_fallback
from core.models import ForensicLogEntry, SieveOutcome


NUMBER_PATTERN = re.compile(r"\b(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\b")


def _leading_digit(value: float) -> int | None:
    absolute = abs(value)
    if absolute == 0:
        return None
    while absolute < 1:
        absolute *= 10
    while absolute >= 10:
        absolute /= 10
    digit = int(absolute)
    if 1 <= digit <= 9:
        return digit
    return None


def _extract_numbers_from_text(extracted_text: str) -> list[float]:
    values: list[float] = []
    for token in NUMBER_PATTERN.findall(extracted_text):
        normalized = token.replace(",", "")
        try:
            value = float(normalized)
        except ValueError:
            continue
        if value > 0:
            values.append(value)
    return values


def _extract_numbers_via_llm(extracted_text: str) -> list[float]:
    if not extracted_text.strip():
        return []

    payload, _used_model = call_json_with_fallback(
        models=settings.extraction_models,
        messages=[
            {
                "role": "system",
                "content": "You extract numeric line-item values from invoices and return strict JSON.",
            },
            {
                "role": "user",
                "content": (
                    "Return JSON as {'line_item_amounts': [number]} containing only monetary line item "
                    "amounts from this invoice text. Exclude dates, phone numbers, IDs, and tax rates.\n\n"
                    f"Invoice text:\n{extracted_text[:16000]}"
                ),
            },
        ],
    )

    amounts = payload.get("line_item_amounts", [])
    if not isinstance(amounts, list):
        return []

    parsed: list[float] = []
    for item in amounts:
        try:
            value = float(item)
        except (TypeError, ValueError):
            continue
        if value > 0:
            parsed.append(value)
    return parsed


def _mad_against_benford(values: list[float]) -> tuple[float, int]:
    counts = {digit: 0 for digit in range(1, 10)}
    usable = 0
    for value in values:
        digit = _leading_digit(value)
        if digit is None:
            continue
        counts[digit] += 1
        usable += 1

    if usable == 0:
        return 1.0, 0

    observed = {digit: counts[digit] / usable for digit in range(1, 10)}
    expected = {digit: math.log10(1 + (1 / digit)) for digit in range(1, 10)}
    mad = sum(abs(observed[digit] - expected[digit]) for digit in range(1, 10)) / 9
    return mad, usable


def analyze_benford(extracted_text: str) -> tuple[ForensicLogEntry, list[float]]:
    regex_values = _extract_numbers_from_text(extracted_text)

    llm_values: list[float] = []
    llm_error: str | None = None
    try:
        llm_values = _extract_numbers_via_llm(extracted_text)
    except Exception as exc:
        llm_error = str(exc)

    values = sorted(set([*regex_values, *llm_values]))

    if len(values) < settings.benford_min_sample_size:
        details = (
            f"Benford analysis needs at least {settings.benford_min_sample_size} positive values; "
            f"found {len(values)}."
        )
        if llm_error:
            details = f"{details} LLM extraction degraded: {llm_error[:220]}"
        return (
            ForensicLogEntry(
                sieve="Statistical",
                result=SieveOutcome.WARNING,
                details=details,
            ),
            values,
        )

    mad, usable = _mad_against_benford(values)

    if mad > 0.015:
        result = SieveOutcome.ANOMALY
        conformity = "non-conforming"
    else:
        result = SieveOutcome.PASS
        conformity = "conforming"

    details = (
        f"Benford MAD={mad:.5f} on {usable} values, classified as {conformity} "
        "(threshold 0.01500)."
    )
    if llm_error:
        details = f"{details} LLM extraction fallback warning: {llm_error[:180]}"

    return ForensicLogEntry(sieve="Statistical", result=result, details=details), values
