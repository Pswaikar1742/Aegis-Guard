from __future__ import annotations

import io

from PyPDF2 import PdfReader

from core.config import settings
from core.document_parser import is_pdf_document
from core.models import ForensicLogEntry, SieveOutcome


def analyze_metadata(
    invoice_bytes: bytes,
    *,
    filename: str,
    content_type: str,
) -> tuple[ForensicLogEntry, dict[str, str]]:
    if not is_pdf_document(invoice_bytes, filename, content_type):
        return (
            ForensicLogEntry(
                sieve="Cryptographic",
                result=SieveOutcome.WARNING,
                details="Metadata analysis skipped because file is not a PDF.",
            ),
            {"creator": "unknown", "producer": "unknown"},
        )

    try:
        reader = PdfReader(io.BytesIO(invoice_bytes))
        metadata = reader.metadata or {}
    except Exception as exc:
        return (
            ForensicLogEntry(
                sieve="Cryptographic",
                result=SieveOutcome.ERROR,
                details=f"Unable to parse PDF metadata: {exc}",
            ),
            {"creator": "unknown", "producer": "unknown"},
        )

    creator = str(metadata.get("/Creator", "")).strip() or "unknown"
    producer = str(metadata.get("/Producer", "")).strip() or "unknown"
    searchable_blob = f"{creator} {producer}".lower()

    flagged_terms = [
        token for token in settings.suspicious_pdf_creators if token.lower() in searchable_blob
    ]

    if flagged_terms:
        details = (
            f"PDF metadata creator='{creator}', producer='{producer}'. "
            f"Flagged tools: {', '.join(sorted(set(flagged_terms)))}."
        )
        result = SieveOutcome.ANOMALY
    else:
        details = (
            f"PDF metadata creator='{creator}', producer='{producer}' did not match suspicious tools."
        )
        result = SieveOutcome.PASS

    return (
        ForensicLogEntry(sieve="Cryptographic", result=result, details=details),
        {"creator": creator, "producer": producer},
    )
