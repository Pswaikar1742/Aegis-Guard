from __future__ import annotations

from sieves.arithmetic import InvoiceData, InvoiceLineItem, analyze_arithmetic, verify_invoice_math


def test_verify_invoice_math_passes_when_totals_are_consistent() -> None:
    data = InvoiceData(
        line_items=[
            InvoiceLineItem(quantity=2.0, price=100.0, tax=36.0, line_total=236.0),
            InvoiceLineItem(quantity=1.0, price=150.0, tax=27.0, line_total=177.0),
        ],
        subtotal=350.0,
        tax_total=63.0,
        grand_total=413.0,
    )

    result = verify_invoice_math(data)

    assert result.status.value == "PASS"
    assert "within INR 1 variance" in result.message


def test_verify_invoice_math_flags_fail_for_tampered_totals() -> None:
    data = InvoiceData(
        line_items=[
            InvoiceLineItem(quantity=2.0, price=100.0, tax=36.0, line_total=290.0),
        ],
        subtotal=290.0,
        tax_total=36.0,
        grand_total=500.0,
    )

    result = verify_invoice_math(data)

    assert result.status.value == "FAIL"
    assert "mismatch" in result.message


def test_analyze_arithmetic_warns_when_fields_are_missing() -> None:
    entry, summary = analyze_arithmetic("just random words without numbers")

    assert entry.result.value == "WARNING"
    assert summary["checks_performed"] == 0
    assert "skipped" in entry.details
