from __future__ import annotations

import re

from core.config import settings
from core.fastrouter_client import call_json_with_fallback
from core.models import ForensicLogEntry, SieveOutcome


GSTIN_PATTERN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b")
GSTIN_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_CHAR_INDEX = {char: index for index, char in enumerate(GSTIN_CHARSET)}


def _normalize_gstin(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()


def gstin_checksum(gstin: str) -> bool:
    normalized = _normalize_gstin(gstin)
    if len(normalized) != 15:
        return False
    if any(char not in GSTIN_CHAR_INDEX for char in normalized):
        return False

    payload = normalized[:14]
    expected_check_char = normalized[14]

    factor = 2
    total = 0
    for char in reversed(payload):
        codepoint = GSTIN_CHAR_INDEX[char]
        addend = factor * codepoint
        factor = 1 if factor == 2 else 2
        addend = (addend // 36) + (addend % 36)
        total += addend

    checksum_value = (36 - (total % 36)) % 36
    return GSTIN_CHARSET[checksum_value] == expected_check_char


def _extract_gstin_candidates_from_text(extracted_text: str) -> list[str]:
    matches = GSTIN_PATTERN.findall(extracted_text.upper())
    return sorted(set(matches))


def _extract_gstin_candidates_via_llm(extracted_text: str) -> list[str]:
    if not extracted_text.strip():
        return []

    prompt = (
        "Extract GSTIN values from this invoice text. Return only JSON with key 'gstins' as "
        "an array of strings. If none exist, return {'gstins': []}."
    )

    payload, _used_model = call_json_with_fallback(
        models=settings.extraction_models,
        messages=[
            {
                "role": "system",
                "content": "You are a strict data extraction engine. Return valid JSON only.",
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nInvoice text:\n{extracted_text[:15000]}",
            },
        ],
    )

    gstins = payload.get("gstins", [])
    if not isinstance(gstins, list):
        return []
    normalized = [_normalize_gstin(str(item)) for item in gstins if str(item).strip()]
    return sorted(set(item for item in normalized if GSTIN_PATTERN.fullmatch(item)))


def analyze_checksum(extracted_text: str) -> tuple[ForensicLogEntry, list[str]]:
    regex_gstins = _extract_gstin_candidates_from_text(extracted_text)

    llm_gstins: list[str] = []
    llm_error: str | None = None
    try:
        llm_gstins = _extract_gstin_candidates_via_llm(extracted_text)
    except Exception as exc:
        llm_error = str(exc)

    all_gstins = sorted(set([*regex_gstins, *llm_gstins]))
    if not all_gstins:
        details = "No GSTIN candidates were found in invoice text."
        if llm_error:
            details = f"{details} LLM extraction degraded: {llm_error[:220]}"
        return (
            ForensicLogEntry(
                sieve="Checksum",
                result=SieveOutcome.WARNING,
                details=details,
            ),
            [],
        )

    invalid_gstins = [gstin for gstin in all_gstins if not gstin_checksum(gstin)]

    if invalid_gstins:
        details = (
            f"GSTIN checksum failed for: {', '.join(invalid_gstins)}. "
            f"Validated candidates: {', '.join(all_gstins)}."
        )
        result = SieveOutcome.FAILED
    else:
        details = f"All extracted GSTIN values passed checksum validation: {', '.join(all_gstins)}."
        result = SieveOutcome.PASS

    if llm_error:
        details = f"{details} LLM extraction fallback warning: {llm_error[:180]}"

    return ForensicLogEntry(sieve="Checksum", result=result, details=details), all_gstins
