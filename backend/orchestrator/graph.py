from __future__ import annotations

from functools import lru_cache
import time
from typing import TypedDict
import uuid

from langgraph.graph import END, START, StateGraph

from core.models import AnalyzeResponse, FinalJudgement, ForensicLogEntry, SieveOutcome
from core.document_parser import extract_invoice_text
from sieves.benford import analyze_benford
from sieves.checksum import analyze_checksum
from sieves.metadata import analyze_metadata
from sieves.vision import analyze_vision


class FraudMeshState(TypedDict):
    request_id: str
    invoice_bytes: bytes
    filename: str
    content_type: str
    extracted_text: str
    metadata: dict[str, str]
    gstins: list[str]
    line_item_amounts: list[float]
    forensic_log: list[ForensicLogEntry]
    final_judgement: FinalJudgement


def _stamp_forensic_entry(
    entry: ForensicLogEntry,
    *,
    request_id: str,
    started_at: float,
) -> ForensicLogEntry:
    duration_ms = max(0, int((time.perf_counter() - started_at) * 1000))
    return entry.model_copy(
        update={
            "correlation_id": request_id,
            "duration_ms": duration_ms,
        }
    )


def _parse_document_node(state: FraudMeshState) -> FraudMeshState:
    extracted_text = extract_invoice_text(
        state["invoice_bytes"], state["filename"], state["content_type"]
    )
    return {**state, "extracted_text": extracted_text}


def _metadata_node(state: FraudMeshState) -> FraudMeshState:
    started_at = time.perf_counter()
    entry, metadata = analyze_metadata(
        state["invoice_bytes"],
        filename=state["filename"],
        content_type=state["content_type"],
    )
    entry = _stamp_forensic_entry(entry, request_id=state["request_id"], started_at=started_at)
    return {
        **state,
        "metadata": metadata,
        "forensic_log": [*state["forensic_log"], entry],
    }


def _checksum_node(state: FraudMeshState) -> FraudMeshState:
    started_at = time.perf_counter()
    entry, gstins = analyze_checksum(state["extracted_text"])
    entry = _stamp_forensic_entry(entry, request_id=state["request_id"], started_at=started_at)
    return {
        **state,
        "gstins": gstins,
        "forensic_log": [*state["forensic_log"], entry],
    }


def _benford_node(state: FraudMeshState) -> FraudMeshState:
    started_at = time.perf_counter()
    entry, line_item_amounts = analyze_benford(state["extracted_text"])
    entry = _stamp_forensic_entry(entry, request_id=state["request_id"], started_at=started_at)
    return {
        **state,
        "line_item_amounts": line_item_amounts,
        "forensic_log": [*state["forensic_log"], entry],
    }


def _vision_node(state: FraudMeshState) -> FraudMeshState:
    started_at = time.perf_counter()
    entry = analyze_vision(
        state["invoice_bytes"],
        filename=state["filename"],
        content_type=state["content_type"],
    )
    entry = _stamp_forensic_entry(entry, request_id=state["request_id"], started_at=started_at)
    return {**state, "forensic_log": [*state["forensic_log"], entry]}


def _judgement_node(state: FraudMeshState) -> FraudMeshState:
    severe_findings = sum(
        1
        for item in state["forensic_log"]
        if item.result in {SieveOutcome.ANOMALY, SieveOutcome.FAILED}
    )
    errors = sum(1 for item in state["forensic_log"] if item.result == SieveOutcome.ERROR)

    if severe_findings >= 2:
        judgement = FinalJudgement.FRAUD_DETECTED
    elif severe_findings == 1 or errors > 0:
        judgement = FinalJudgement.SUSPICIOUS
    else:
        judgement = FinalJudgement.VALIDATED

    return {**state, "final_judgement": judgement}


@lru_cache(maxsize=1)
def build_graph():
    workflow = StateGraph(FraudMeshState)

    workflow.add_node("parse_document", _parse_document_node)
    workflow.add_node("metadata", _metadata_node)
    workflow.add_node("checksum", _checksum_node)
    workflow.add_node("benford", _benford_node)
    workflow.add_node("vision", _vision_node)
    workflow.add_node("finalize", _judgement_node)

    workflow.add_edge(START, "parse_document")
    workflow.add_edge("parse_document", "metadata")
    workflow.add_edge("metadata", "checksum")
    workflow.add_edge("checksum", "benford")
    workflow.add_edge("benford", "vision")
    workflow.add_edge("vision", "finalize")
    workflow.add_edge("finalize", END)

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
        "metadata": {},
        "gstins": [],
        "line_item_amounts": [],
        "forensic_log": [],
        "final_judgement": FinalJudgement.SUSPICIOUS,
    }

    final_state = build_graph().invoke(initial_state)
    return AnalyzeResponse(
        status="Completed",
        final_judgement=final_state["final_judgement"],
        forensic_log=final_state["forensic_log"],
    )
