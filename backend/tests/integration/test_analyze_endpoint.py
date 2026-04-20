from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from core.models import VisionAnalysis
from main import app
from orchestrator.graph import build_graph
from sieves.arithmetic import InvoiceData, InvoiceLineItem
from sieves.checksum import validate_gstin


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "invoice_sample.pdf"


def _valid_gstin() -> str:
    payload = "27ABCDE1234F1Z"
    for digit in "0123456789":
        candidate = payload + digit
        if validate_gstin(candidate):
            return candidate
    raise AssertionError("Unable to derive a valid GSTIN for tests.")


def _benford_like_values() -> list[float]:
    counts = {
        1: 301,
        2: 176,
        3: 125,
        4: 97,
        5: 79,
        6: 67,
        7: 58,
        8: 51,
        9: 46,
    }
    values: list[float] = []
    for digit, count in counts.items():
        for idx in range(count):
            values.append(float(f"{digit}{idx + 100}"))
    return values


def test_analyze_endpoint_with_pdf_fixture(monkeypatch) -> None:
    assert FIXTURE_PATH.exists(), f"Missing test fixture: {FIXTURE_PATH}"

    monkeypatch.setattr(
        "sieves.checksum._extract_gstin_candidates_from_text",
        lambda _text: [_valid_gstin()],
    )
    monkeypatch.setattr(
        "sieves.benford._extract_numbers_from_text",
        lambda _text: _benford_like_values(),
    )
    monkeypatch.setattr(
        "sieves.arithmetic._extract_invoice_data_from_text",
        lambda _text: InvoiceData(
            line_items=[
                InvoiceLineItem(quantity=2.0, price=100.0, tax=36.0, line_total=236.0),
                InvoiceLineItem(quantity=1.0, price=200.0, tax=36.0, line_total=236.0),
            ],
            subtotal=400.0,
            tax_total=72.0,
            grand_total=472.0,
        ),
    )
    monkeypatch.setattr(
        "sieves.vision._call_vision_model",
        lambda _data_url, **_kwargs: VisionAnalysis(
            tampering_detected=False,
            risk_level="LOW",
            summary="No visual tampering indicators found.",
            findings=[],
        ),
    )
    monkeypatch.setattr(
        "sieves.registry._call_registry_model",
        lambda **_kwargs: {
            "matched": True,
            "confidence": 0.8,
            "rationale": "Vendor and GST profile are consistent.",
            "region_consistency": True,
        },
    )

    # Ensure the test runs with patched nodes and not cached compiled graph closures.
    build_graph.cache_clear()

    with FIXTURE_PATH.open("rb") as fixture_file:
        payload = fixture_file.read()

    client = TestClient(app)
    response = client.post(
        "/api/v1/analyze",
        files={"invoice": ("invoice_sample.pdf", payload, "application/pdf")},
    )

    assert response.status_code == 200
    request_id = response.headers.get("X-Request-ID")
    assert request_id

    body = response.json()
    assert body["status"] == "Completed"
    assert body["final_judgement"] == "VALIDATED"

    forensic_log = body["forensic_log"]
    assert len(forensic_log) == 6
    assert [entry["sieve"] for entry in forensic_log] == [
        "Cryptographic",
        "Checksum",
        "Arithmetic",
        "Statistical",
        "Spatial",
        "OSINT",
    ]
    assert all(entry["result"] in {"PASS", "WARNING"} for entry in forensic_log)
    assert all(entry.get("correlation_id") == request_id for entry in forensic_log)
    assert all(isinstance(entry.get("duration_ms"), int) for entry in forensic_log)
    assert all(entry.get("duration_ms", -1) >= 0 for entry in forensic_log)


def test_analyze_endpoint_degrades_when_model_calls_fail(monkeypatch) -> None:
    assert FIXTURE_PATH.exists(), f"Missing test fixture: {FIXTURE_PATH}"

    monkeypatch.setattr(
        "sieves.checksum._extract_gstin_candidates_from_text",
        lambda _text: [],
    )
    monkeypatch.setattr(
        "sieves.benford._extract_numbers_from_text",
        lambda _text: [],
    )
    monkeypatch.setattr(
        "sieves.arithmetic._extract_invoice_data_from_text",
        lambda _text: None,
    )
    monkeypatch.setattr(
        "sieves.vision._call_vision_model",
        lambda _data_url, **_kwargs: (_ for _ in ()).throw(RuntimeError("simulated vision model outage")),
    )
    monkeypatch.setattr(
        "sieves.registry._call_registry_model",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("simulated registry model outage")),
    )

    build_graph.cache_clear()

    with FIXTURE_PATH.open("rb") as fixture_file:
        payload = fixture_file.read()

    client = TestClient(app)
    response = client.post(
        "/api/v1/analyze",
        files={"invoice": ("invoice_sample.pdf", payload, "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "Completed"
    assert body["final_judgement"] == "SUSPICIOUS"
    assert len(body["forensic_log"]) == 6
    assert any(entry["result"] == "FAILED" for entry in body["forensic_log"])


def test_analyze_endpoint_returns_standard_error_payload_for_empty_invoice() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/analyze",
        files={"invoice": ("empty.pdf", b"", "application/pdf")},
    )

    assert response.status_code == 400
    body = response.json()
    detail = body["detail"]
    assert detail["code"] == "EMPTY_INVOICE"
    assert detail["message"] == "Uploaded invoice is empty."
    assert isinstance(detail["request_id"], str) and detail["request_id"]
