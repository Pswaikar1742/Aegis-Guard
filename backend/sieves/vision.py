from __future__ import annotations

import base64
import io
from typing import Any

import pypdfium2 as pdfium

from core.config import settings
from core.document_parser import is_pdf_document
from core.fastrouter_client import call_json_with_fallback
from core.models import ForensicLogEntry, SieveOutcome, VisionAnalysis


def _to_data_url(image_bytes: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def _render_first_pdf_page_as_png(pdf_bytes: bytes) -> bytes:
    document = pdfium.PdfDocument(pdf_bytes)
    if len(document) == 0:
        raise ValueError("PDF has no pages.")

    page = document[0]
    pil_image = page.render(scale=2.0).to_pil()
    output = io.BytesIO()
    pil_image.save(output, format="PNG")
    return output.getvalue()


def _prepare_visual_payload(
    invoice_bytes: bytes,
    filename: str,
    content_type: str,
) -> tuple[str, str]:
    if is_pdf_document(invoice_bytes, filename, content_type):
        png_bytes = _render_first_pdf_page_as_png(invoice_bytes)
        return _to_data_url(png_bytes, "image/png"), "image/png"

    lowered_type = (content_type or "").lower()
    if lowered_type.startswith("image/"):
        return _to_data_url(invoice_bytes, lowered_type), lowered_type

    lowered_name = filename.lower()
    if lowered_name.endswith(".png"):
        return _to_data_url(invoice_bytes, "image/png"), "image/png"
    if lowered_name.endswith(".jpg") or lowered_name.endswith(".jpeg"):
        return _to_data_url(invoice_bytes, "image/jpeg"), "image/jpeg"
    if lowered_name.endswith(".webp"):
        return _to_data_url(invoice_bytes, "image/webp"), "image/webp"

    raise ValueError("Vision sieve supports PDF, PNG, JPG, JPEG, and WEBP invoices.")


def _call_vision_model(data_url: str) -> VisionAnalysis:
    payload, _used_model = call_json_with_fallback(
        models=settings.vision_models,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a forensic document analyst. Return strict JSON with keys: "
                    "tampering_detected (bool), risk_level (LOW|MEDIUM|HIGH), summary (string), "
                    "findings (array of strings)."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Inspect this invoice image for signs of tampering: mismatched fonts, "
                            "compression artifacts near totals/signatures, alignment anomalies, "
                            "or edited text blocks."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                ],
            },
        ],
    )

    normalized: dict[str, Any] = {
        "tampering_detected": bool(payload.get("tampering_detected", False)),
        "risk_level": str(payload.get("risk_level", "LOW")).upper(),
        "summary": str(payload.get("summary", "No visual anomalies reported.")),
        "findings": payload.get("findings", []),
    }
    if not isinstance(normalized["findings"], list):
        normalized["findings"] = []

    return VisionAnalysis.model_validate(normalized)


def analyze_vision(
    invoice_bytes: bytes,
    *,
    filename: str,
    content_type: str,
) -> ForensicLogEntry:
    try:
        data_url, _mime_type = _prepare_visual_payload(invoice_bytes, filename, content_type)
        analysis = _call_vision_model(data_url)
    except Exception as exc:
        return ForensicLogEntry(
            sieve="Spatial",
            result=SieveOutcome.ERROR,
            details=f"Vision sieve failed: {exc}",
        )

    severe_risk = analysis.risk_level in {"HIGH", "CRITICAL"}
    flagged = analysis.tampering_detected or severe_risk
    result = SieveOutcome.ANOMALY if flagged else SieveOutcome.PASS

    findings = ", ".join(analysis.findings[:5]) if analysis.findings else "No discrete findings"
    details = (
        f"Risk={analysis.risk_level}. {analysis.summary}. Findings: {findings}."
    )

    return ForensicLogEntry(sieve="Spatial", result=result, details=details)
