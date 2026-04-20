from __future__ import annotations

import re

from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


GSTIN_PATTERN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b")
GSTIN_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_CHAR_INDEX = {char: index for index, char in enumerate(GSTIN_CHARSET)}


def _normalize_gstin(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()


def validate_gstin(gstin: str) -> bool:
    normalized = _normalize_gstin(gstin)
    if len(normalized) != 15:
        return False
    if not GSTIN_PATTERN.fullmatch(normalized):
        return False
    if any(char not in GSTIN_CHAR_INDEX for char in normalized):
        return False

    payload = normalized[:14]
    expected_check_digit = normalized[14]
    if not expected_check_digit.isdigit():
        return False

    # Deterministic modulo-10 checksum across alphanumeric payload characters.
    factor = 2
    total = 0
    for char in reversed(payload):
        codepoint = GSTIN_CHAR_INDEX[char]
        addend = factor * codepoint
        factor = 1 if factor == 2 else 2
        addend = (addend // 10) + (addend % 10)
        total += addend

    checksum_value = (10 - (total % 10)) % 10
    return str(checksum_value) == expected_check_digit


def gstin_checksum(gstin: str) -> bool:
    return validate_gstin(gstin)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _extract_gstin_candidates_from_text(extracted_text: str) -> list[str]:
    matches = GSTIN_PATTERN.findall(extracted_text.upper())
    return sorted(set(matches))


def evaluate_checksum(gstins: list[str]) -> SieveResult:
    if not gstins:
        return SieveResult(
            status=SieveStatus.WARNING,
            message="No GSTIN values were found for checksum validation.",
        )

    invalid_gstins = [gstin for gstin in gstins if not validate_gstin(gstin)]
    if invalid_gstins:
        return SieveResult(
            status=SieveStatus.FAIL,
            message=(
                f"GSTIN checksum validation failed for: {', '.join(invalid_gstins)}."
            ),
        )

    return SieveResult(
        status=SieveStatus.PASS,
        message=f"All GSTIN values passed checksum validation: {', '.join(gstins)}.",
    )


def run_checksum_sieve(extracted_text: str) -> SieveResult:
    gstins = _extract_gstin_candidates_from_text(extracted_text)
    return evaluate_checksum(gstins)


def analyze_checksum(extracted_text: str) -> tuple[ForensicLogEntry, list[str]]:
    gstins = _extract_gstin_candidates_from_text(extracted_text)
    sieve_result = evaluate_checksum(gstins)
    return (
        ForensicLogEntry(
            sieve="Checksum",
            result=_status_to_outcome(sieve_result.status),
            details=sieve_result.message,
        ),
        gstins,
    )
