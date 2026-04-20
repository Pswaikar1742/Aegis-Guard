from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


LINE_ITEM_PATTERN = re.compile(
    r"(?im)^\s*[^\n]{0,120}?\b(\d+(?:\.\d+)?)\s*(?:x|\*|×)\s*"
    r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:\+\s*([0-9][0-9,]*(?:\.\d+)?))?\s*"
    r"(?:=|:)?\s*([0-9][0-9,]*(?:\.\d+)?)\b"
)
SUBTOTAL_PATTERN = re.compile(
    r"(?im)\bsub[\s-]*total\b\s*[:\-]?\s*(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)
TAX_TOTAL_PATTERN = re.compile(
    r"(?im)\b(?:total\s+tax|tax\s+total|gst\s+total)\b\s*[:\-]?\s*"
    r"(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)
GRAND_TOTAL_PATTERN = re.compile(
    r"(?im)\b(?:grand\s+total|total\s+due|amount\s+payable|invoice\s+total)\b\s*[:\-]?\s*"
    r"(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)


class InvoiceLineItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    quantity: float = Field(gt=0)
    price: float = Field(ge=0)
    tax: float = Field(default=0.0, ge=0)
    line_total: float = Field(ge=0)


class InvoiceData(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    line_items: list[InvoiceLineItem] = Field(min_length=1)
    subtotal: float = Field(ge=0)
    tax_total: float = Field(ge=0)
    grand_total: float = Field(ge=0)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    normalized = re.sub(r"[^0-9.\-]", "", str(value).replace(",", "").strip())
    if not normalized or normalized in {".", "-", "-."}:
        return None

    try:
        return float(normalized)
    except ValueError:
        return None


def _within_rupee_variance(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= 1.0


def verify_invoice_math(data: InvoiceData) -> SieveResult:
    mismatches: list[str] = []

    recomputed_subtotal = 0.0
    recomputed_tax_total = 0.0

    for index, item in enumerate(data.line_items, start=1):
        expected_base = round(item.quantity * item.price, 2)
        expected_line_total = round(expected_base + item.tax, 2)

        recomputed_subtotal += expected_base
        recomputed_tax_total += item.tax

        if not _within_rupee_variance(item.line_total, expected_line_total):
            mismatches.append(
                (
                    f"line {index}: expected qty*price+tax={expected_line_total:.2f}, "
                    f"found line_total={item.line_total:.2f}"
                )
            )

    recomputed_subtotal = round(recomputed_subtotal, 2)
    recomputed_tax_total = round(recomputed_tax_total, 2)
    recomputed_grand_total = round(recomputed_subtotal + recomputed_tax_total, 2)

    if not _within_rupee_variance(data.subtotal, recomputed_subtotal):
        mismatches.append(
            (
                f"subtotal mismatch: expected {recomputed_subtotal:.2f}, "
                f"found {data.subtotal:.2f}"
            )
        )

    if not _within_rupee_variance(data.tax_total, recomputed_tax_total):
        mismatches.append(
            (
                f"tax_total mismatch: expected {recomputed_tax_total:.2f}, "
                f"found {data.tax_total:.2f}"
            )
        )

    if not _within_rupee_variance(data.grand_total, recomputed_grand_total):
        mismatches.append(
            (
                f"grand_total mismatch: expected {recomputed_grand_total:.2f}, "
                f"found {data.grand_total:.2f}"
            )
        )

    if mismatches:
        return SieveResult(
            status=SieveStatus.FAIL,
            message=(
                f"Arithmetic verification failed with {len(mismatches)} mismatch(es): "
                f"{' | '.join(mismatches[:5])}."
            ),
        )

    return SieveResult(
        status=SieveStatus.PASS,
        message=(
            f"Arithmetic verification passed for {len(data.line_items)} line item(s); "
            f"subtotal, tax_total, and grand_total are within INR 1 variance."
        ),
    )


def _extract_invoice_data_from_text(extracted_text: str) -> InvoiceData | None:
    line_items: list[InvoiceLineItem] = []
    for quantity_raw, price_raw, tax_raw, line_total_raw in LINE_ITEM_PATTERN.findall(extracted_text):
        quantity = _to_float(quantity_raw)
        price = _to_float(price_raw)
        tax = _to_float(tax_raw) if tax_raw else 0.0
        line_total = _to_float(line_total_raw)

        if quantity is None or price is None or line_total is None:
            continue
        if quantity <= 0 or price < 0 or line_total < 0:
            continue

        line_items.append(
            InvoiceLineItem(
                quantity=quantity,
                price=price,
                tax=0.0 if tax is None else max(tax, 0.0),
                line_total=line_total,
            )
        )

    if not line_items:
        return None

    subtotal_match = SUBTOTAL_PATTERN.findall(extracted_text)
    tax_total_match = TAX_TOTAL_PATTERN.findall(extracted_text)
    grand_total_match = GRAND_TOTAL_PATTERN.findall(extracted_text)

    if not subtotal_match or not tax_total_match or not grand_total_match:
        return None

    subtotal = _to_float(subtotal_match[-1])
    tax_total = _to_float(tax_total_match[-1])
    grand_total = _to_float(grand_total_match[-1])
    if subtotal is None or tax_total is None or grand_total is None:
        return None

    return InvoiceData(
        line_items=line_items,
        subtotal=subtotal,
        tax_total=tax_total,
        grand_total=grand_total,
    )


def analyze_arithmetic(extracted_text: str) -> tuple[ForensicLogEntry, dict[str, int]]:
    data = _extract_invoice_data_from_text(extracted_text)
    if data is None:
        result = SieveResult(
            status=SieveStatus.WARNING,
            message=(
                "Arithmetic verification skipped because invoice line-item or total fields "
                "could not be deterministically extracted."
            ),
        )
        return (
            ForensicLogEntry(
                sieve="Arithmetic",
                result=_status_to_outcome(result.status),
                details=result.message,
            ),
            {"checks_performed": 0, "anomaly_count": 0, "line_item_count": 0},
        )

    result = verify_invoice_math(data)
    anomaly_count = 0 if result.status != SieveStatus.FAIL else max(1, result.message.count("mismatch"))
    checks_performed = len(data.line_items) + 3

    return (
        ForensicLogEntry(
            sieve="Arithmetic",
            result=_status_to_outcome(result.status),
            details=result.message,
        ),
        {
            "checks_performed": checks_performed,
            "anomaly_count": anomaly_count,
            "line_item_count": len(data.line_items),
        },
    )


def run_arithmetic_sieve(extracted_text: str) -> SieveResult:
    entry, _summary = analyze_arithmetic(extracted_text)
    if entry.result == SieveOutcome.PASS:
        status = SieveStatus.PASS
    elif entry.result in {SieveOutcome.FAILED, SieveOutcome.ANOMALY}:
        status = SieveStatus.FAIL
    else:
        status = SieveStatus.WARNING
    return SieveResult(status=status, message=entry.details)
