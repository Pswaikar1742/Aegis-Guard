from __future__ import annotations

import io

from PyPDF2 import PdfReader
from pydantic import BaseModel, ConfigDict, Field

from core.document_parser import is_pdf_document
from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


FLAGGED_CREATOR_TERMS = ("canva", "photoshop", "ilovepdf", "word")


class MetadataSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    creator: str
    producer: str
    flagged_terms: list[str] = Field(default_factory=list)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _evaluate_metadata(snapshot: MetadataSnapshot) -> SieveResult:
    if snapshot.flagged_terms:
        return SieveResult(
            status=SieveStatus.FAIL,
            message=(
                f"Suspicious metadata detected: creator='{snapshot.creator}', "
                f"producer='{snapshot.producer}', flagged={', '.join(snapshot.flagged_terms)}."
            ),
        )

    return SieveResult(
        status=SieveStatus.PASS,
        message=(
            f"Metadata is clean: creator='{snapshot.creator}', producer='{snapshot.producer}'."
        ),
    )


def analyze_metadata(
    invoice_bytes: bytes,
    *,
    filename: str,
    content_type: str,
) -> tuple[ForensicLogEntry, dict[str, str]]:
    if not is_pdf_document(invoice_bytes, filename, content_type):
        result = SieveResult(
            status=SieveStatus.WARNING,
            message="Metadata check skipped because the uploaded file is not a PDF.",
        )
        return (
            ForensicLogEntry(
                sieve="Cryptographic",
                result=_status_to_outcome(result.status),
                details=result.message,
            ),
            {"creator": "unknown", "producer": "unknown"},
        )

    try:
        reader = PdfReader(io.BytesIO(invoice_bytes))
        metadata = reader.metadata or {}
    except Exception as exc:
        result = SieveResult(
            status=SieveStatus.WARNING,
            message=f"Metadata parsing failed: {exc}",
        )
        return (
            ForensicLogEntry(
                sieve="Cryptographic",
                result=_status_to_outcome(result.status),
                details=result.message,
            ),
            {"creator": "unknown", "producer": "unknown"},
        )

    creator = str(metadata.get("/Creator", "")).strip() or "unknown"
    producer = str(metadata.get("/Producer", "")).strip() or "unknown"
    searchable_blob = f"{creator} {producer}".lower()

    flagged_terms = sorted(
        {term for term in FLAGGED_CREATOR_TERMS if term in searchable_blob}
    )
    snapshot = MetadataSnapshot(
        creator=creator,
        producer=producer,
        flagged_terms=flagged_terms,
    )
    sieve_result = _evaluate_metadata(snapshot)

    return (
        ForensicLogEntry(
            sieve="Cryptographic",
            result=_status_to_outcome(sieve_result.status),
            details=sieve_result.message,
        ),
        {"creator": creator, "producer": producer},
    )


def run_metadata_sieve(
    invoice_bytes: bytes,
    *,
    filename: str,
    content_type: str,
) -> SieveResult:
    entry, _metadata = analyze_metadata(
        invoice_bytes,
        filename=filename,
        content_type=content_type,
    )
    if entry.result == SieveOutcome.PASS:
        status = SieveStatus.PASS
    elif entry.result in {SieveOutcome.FAILED, SieveOutcome.ANOMALY}:
        status = SieveStatus.FAIL
    else:
        status = SieveStatus.WARNING

    return SieveResult(status=status, message=entry.details)
