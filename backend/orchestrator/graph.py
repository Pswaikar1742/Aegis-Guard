from __future__ import annotations

import re
from functools import lru_cache
from typing import Any, TypedDict
import uuid

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field

from core.config import settings
from core.document_parser import extract_invoice_text
from core.fastrouter_client import call_json_with_fallback
from core.models import AnalyzeResponse, FinalJudgement, ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus
from sieves.arithmetic import InvoiceData, InvoiceLineItem, run_arithmetic_sieve, verify_invoice_math
from sieves.benford import evaluate_benford, run_benford_sieve
from sieves.checksum import evaluate_checksum, run_checksum_sieve
from sieves.metadata import run_metadata_sieve
from sieves.registry import run_registry_sieve
from sieves.vision import analyze_vision


GSTIN_PATTERN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[0-9]\b")
NUMBER_PATTERN = re.compile(r"\b(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\b")


class ExtractedLineItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    quantity: float | None = None
    price: float | None = None
    tax: float | None = 0.0
    line_total: float | None = None


class ExtractedInvoiceData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vendor_name: str = ""
    gstin: str = ""
    line_items: list[ExtractedLineItem] = Field(default_factory=list)
    subtotal: float | None = None
    tax_total: float | None = None
    grand_total: float | None = None
    numbers: list[float] = Field(default_factory=list)


class FraudMeshState(TypedDict):
    request_id: str
    invoice_bytes: bytes
    filename: str
    content_type: str
    extracted_text: str
    extracted_data: ExtractedInvoiceData
    metadata_result: SieveResult
    checksum_result: SieveResult
    arithmetic_result: SieveResult
    benford_result: SieveResult
    vision_result: SieveResult
    registry_result: SieveResult
    forensic_log: list[ForensicLogEntry]
    final_judgement: FinalJudgement


def _warning_result(message: str) -> SieveResult:
    return SieveResult(status=SieveStatus.WARNING, message=message)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _entry_to_sieve_result(entry: ForensicLogEntry) -> SieveResult:
    if entry.result == SieveOutcome.PASS:
        status = SieveStatus.PASS
    elif entry.result in {SieveOutcome.ANOMALY, SieveOutcome.FAILED, SieveOutcome.ERROR}:
        status = SieveStatus.FAIL
    else:
        status = SieveStatus.WARNING
    return SieveResult(status=status, message=entry.details)


def _to_float(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed


def _extract_numbers_from_text(extracted_text: str) -> list[float]:
    values: list[float] = []
    for token in NUMBER_PATTERN.findall(extracted_text):
        number = _to_float(token.replace(",", ""))
        if number is None:
            continue
        if number > 0:
            values.append(number)
    return values


def _normalize_line_items(payload: dict[str, Any]) -> list[ExtractedLineItem]:
    raw_items = payload.get("line_items", [])
    if not isinstance(raw_items, list):
        return []

    items: list[ExtractedLineItem] = []
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            continue
        items.append(
            ExtractedLineItem(
                quantity=_to_float(raw_item.get("quantity")),
                price=_to_float(raw_item.get("price")),
                tax=_to_float(raw_item.get("tax")) or 0.0,
                line_total=_to_float(raw_item.get("line_total")),
            )
        )
    return items


def _normalize_extracted_data(payload: dict[str, Any], extracted_text: str) -> ExtractedInvoiceData:
    raw_gstin = str(payload.get("gstin", "")).strip().upper()
    if not raw_gstin:
        matches = GSTIN_PATTERN.findall(extracted_text.upper())
        raw_gstin = matches[0] if matches else ""

    raw_numbers = payload.get("numbers", [])
    numbers: list[float] = []
    if isinstance(raw_numbers, list):
        for value in raw_numbers:
            parsed = _to_float(value)
            if parsed is not None and parsed > 0:
                numbers.append(parsed)
    if not numbers:
        numbers = _extract_numbers_from_text(extracted_text)

    return ExtractedInvoiceData(
        vendor_name=str(payload.get("vendor_name", "")).strip(),
        gstin=raw_gstin,
        line_items=_normalize_line_items(payload),
        subtotal=_to_float(payload.get("subtotal")),
        tax_total=_to_float(payload.get("tax_total")),
        grand_total=_to_float(payload.get("grand_total")),
        numbers=numbers,
    )


def _extract_data_node(state: FraudMeshState) -> FraudMeshState:
    extracted_text = extract_invoice_text(
        state["invoice_bytes"],
        state["filename"],
        state["content_type"],
    )

    payload: dict[str, Any] = {}
    if extracted_text.strip():
        try:
            payload, _used_model = call_json_with_fallback(
                models=settings.extraction_models,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Extract structured invoice data and return strict JSON only with keys: "
                            "vendor_name (string), gstin (string), line_items (array of objects with "
                            "quantity, price, tax, line_total), subtotal (number|null), tax_total "
                            "(number|null), grand_total (number|null), numbers (array[number])."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Extract the invoice fields from the following text. "
                            "If a field is missing, return empty string, empty array, or null as appropriate.\n\n"
                            f"Invoice text:\n{extracted_text[:20000]}"
                        ),
                    },
                ],
                max_tokens=1600,
            )
        except Exception:
            payload = {}

    extracted_data = _normalize_extracted_data(payload, extracted_text)
    return {"extracted_text": extracted_text, "extracted_data": extracted_data}


def _sieve_metadata_node(state: FraudMeshState) -> FraudMeshState:
    result = run_metadata_sieve(
        state["invoice_bytes"],
        filename=state["filename"],
        content_type=state["content_type"],
    )
    return {"metadata_result": result}


def _sieve_checksum_node(state: FraudMeshState) -> FraudMeshState:
    gstin = state["extracted_data"].gstin
    if gstin:
        result = evaluate_checksum([gstin])
    else:
        result = run_checksum_sieve(state["extracted_text"])
    return {"checksum_result": result}


def _to_invoice_data(extracted: ExtractedInvoiceData) -> InvoiceData | None:
    if extracted.subtotal is None or extracted.tax_total is None or extracted.grand_total is None:
        return None
    if not extracted.line_items:
        return None

    line_items: list[InvoiceLineItem] = []
    for item in extracted.line_items:
        if item.quantity is None or item.price is None or item.line_total is None:
            return None
        line_items.append(
            InvoiceLineItem(
                quantity=item.quantity,
                price=item.price,
                tax=0.0 if item.tax is None else item.tax,
                line_total=item.line_total,
            )
        )

    return InvoiceData(
        line_items=line_items,
        subtotal=extracted.subtotal,
        tax_total=extracted.tax_total,
        grand_total=extracted.grand_total,
    )


def _sieve_arithmetic_node(state: FraudMeshState) -> FraudMeshState:
    invoice_data = _to_invoice_data(state["extracted_data"])
    if invoice_data is not None:
        result = verify_invoice_math(invoice_data)
    else:
        result = run_arithmetic_sieve(state["extracted_text"])
    return {"arithmetic_result": result}


def _sieve_benford_node(state: FraudMeshState) -> FraudMeshState:
    numbers = state["extracted_data"].numbers
    if numbers:
        result = evaluate_benford(numbers)
    else:
        result = run_benford_sieve(state["extracted_text"])
    return {"benford_result": result}


def _sieve_vision_node(state: FraudMeshState) -> FraudMeshState:
    entry = analyze_vision(
        state["invoice_bytes"],
        filename=state["filename"],
        content_type=state["content_type"],
        models=settings.vision_models,
    )
    result = _entry_to_sieve_result(entry)
    return {"vision_result": result}


def _sieve_registry_node(state: FraudMeshState) -> FraudMeshState:
    result = run_registry_sieve(
        vendor_name=state["extracted_data"].vendor_name,
        gstin=state["extracted_data"].gstin,
    )
    return {"registry_result": result}


def _aggregator_node(state: FraudMeshState) -> FraudMeshState:
    ordered_results = [
        ("Cryptographic", state["metadata_result"]),
        ("Checksum", state["checksum_result"]),
        ("Arithmetic", state["arithmetic_result"]),
        ("Statistical", state["benford_result"]),
        ("Spatial", state["vision_result"]),
        ("OSINT", state["registry_result"]),
    ]

    forensic_log = [
        ForensicLogEntry(
            sieve=name,
            result=_status_to_outcome(result.status),
            details=result.message,
            correlation_id=state["request_id"],
            duration_ms=0,
        )
        for name, result in ordered_results
    ]

    # Weight-based trust score (same formula as frontend)
    sieve_weights = {
        "Cryptographic": 15,
        "Checksum": 10,
        "Arithmetic": 20,
        "Statistical": 10,
        "Spatial": 20,
        "OSINT": 8,
    }

    outcome_risk = {
        SieveStatus.PASS: 0.0,
        SieveStatus.WARNING: 0.2,
        SieveStatus.FAIL: 1.0,
    }

    total_penalty = 0.0
    for name, result in ordered_results:
        weight = sieve_weights.get(name, 0)
        risk = outcome_risk.get(result.status, 0.65)
        total_penalty += weight * risk

    trust_score = max(0, round(100 - total_penalty))

    # Map trust score to verdict
    if trust_score >= 80:
        final_judgement = FinalJudgement.VALIDATED
    elif trust_score >= 60:
        final_judgement = FinalJudgement.SUSPICIOUS
    else:
        final_judgement = FinalJudgement.FRAUD_DETECTED

    return {"forensic_log": forensic_log, "final_judgement": final_judgement}


@lru_cache(maxsize=1)
def build_graph():
    workflow = StateGraph(FraudMeshState)

    workflow.add_node("extract_data", _extract_data_node)
    workflow.add_node("sieve_metadata", _sieve_metadata_node)
    workflow.add_node("sieve_checksum", _sieve_checksum_node)
    workflow.add_node("sieve_arithmetic", _sieve_arithmetic_node)
    workflow.add_node("sieve_benford", _sieve_benford_node)
    workflow.add_node("sieve_vision", _sieve_vision_node)
    workflow.add_node("sieve_registry", _sieve_registry_node)
    workflow.add_node("aggregator", _aggregator_node)

    workflow.add_edge(START, "extract_data")

    workflow.add_edge("extract_data", "sieve_metadata")
    workflow.add_edge("extract_data", "sieve_checksum")
    workflow.add_edge("extract_data", "sieve_arithmetic")
    workflow.add_edge("extract_data", "sieve_benford")
    workflow.add_edge("extract_data", "sieve_vision")
    workflow.add_edge("extract_data", "sieve_registry")

    workflow.add_edge("sieve_metadata", "aggregator")
    workflow.add_edge("sieve_checksum", "aggregator")
    workflow.add_edge("sieve_arithmetic", "aggregator")
    workflow.add_edge("sieve_benford", "aggregator")
    workflow.add_edge("sieve_vision", "aggregator")
    workflow.add_edge("sieve_registry", "aggregator")

    workflow.add_edge("aggregator", END)

    return workflow.compile()


def run_invoice_analysis(
    invoice_bytes: bytes,
    filename: str,
    content_type: str,
    request_id: str | None = None,
) -> AnalyzeResponse:
    initial_state: FraudMeshState = {
        "request_id": request_id or str(uuid.uuid4()),
        "invoice_bytes": invoice_bytes,
        "filename": filename,
        "content_type": content_type,
        "extracted_text": "",
        "extracted_data": ExtractedInvoiceData(),
        "metadata_result": _warning_result("Metadata sieve not executed."),
        "checksum_result": _warning_result("Checksum sieve not executed."),
        "arithmetic_result": _warning_result("Arithmetic sieve not executed."),
        "benford_result": _warning_result("Benford sieve not executed."),
        "vision_result": _warning_result("Vision sieve not executed."),
        "registry_result": _warning_result("Registry sieve not executed."),
        "forensic_log": [],
        "final_judgement": FinalJudgement.SUSPICIOUS,
    }

    final_state = build_graph().invoke(initial_state)
    return AnalyzeResponse(
        status="Completed",
        final_judgement=final_state["final_judgement"],
        forensic_log=final_state["forensic_log"],
    )
