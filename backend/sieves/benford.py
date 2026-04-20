from __future__ import annotations

import re

import numpy as np

from core.config import settings
from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


NUMBER_PATTERN = re.compile(r"\b(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\b")


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


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


def _first_digits(values: list[float]) -> np.ndarray:
    if not values:
        return np.array([], dtype=np.int64)

    arr = np.asarray(values, dtype=np.float64)
    arr = np.abs(arr)
    arr = arr[arr > 0]
    if arr.size == 0:
        return np.array([], dtype=np.int64)

    scales = np.power(10.0, np.floor(np.log10(arr)))
    normalized = arr / scales
    digits = np.floor(normalized).astype(np.int64)
    digits = digits[(digits >= 1) & (digits <= 9)]
    return digits


def calculate_variance_score(values: list[float]) -> float:
    digits = _first_digits(values)
    if digits.size == 0:
        return 1.0

    counts = np.bincount(digits, minlength=10)[1:10].astype(np.float64)
    observed = counts / counts.sum()
    expected = np.log10(1.0 + (1.0 / np.arange(1, 10, dtype=np.float64)))
    return float(np.mean(np.square(observed - expected)))


def evaluate_benford(values: list[float]) -> SieveResult:
    if len(values) < settings.benford_min_sample_size:
        return SieveResult(
            status=SieveStatus.WARNING,
            message=(
                f"Benford check needs at least {settings.benford_min_sample_size} positive values; "
                f"found {len(values)}."
            ),
        )

    variance_score = calculate_variance_score(values)
    status = SieveStatus.PASS if variance_score <= 0.0002 else SieveStatus.FAIL
    classification = "conforming" if status == SieveStatus.PASS else "non-conforming"
    return SieveResult(
        status=status,
        message=(
            f"Benford variance score={variance_score:.6f} on {len(values)} values "
            f"({classification}, threshold 0.000200)."
        ),
    )


def run_benford_sieve(extracted_text: str) -> SieveResult:
    values = sorted(set(_extract_numbers_from_text(extracted_text)))
    return evaluate_benford(values)


def analyze_benford(extracted_text: str) -> tuple[ForensicLogEntry, list[float]]:
    values = sorted(set(_extract_numbers_from_text(extracted_text)))
    sieve_result = evaluate_benford(values)
    return (
        ForensicLogEntry(
            sieve="Statistical",
            result=_status_to_outcome(sieve_result.status),
            details=sieve_result.message,
        ),
        values,
    )
