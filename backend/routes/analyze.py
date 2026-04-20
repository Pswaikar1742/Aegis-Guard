from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from core.models import AnalyzeResponse
from orchestrator.graph import run_invoice_analysis


router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_invoice(invoice: UploadFile = File(...)) -> AnalyzeResponse:
    payload = await invoice.read()

    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded invoice is empty.")

    if len(payload) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Invoice file is too large. Maximum allowed size is 15MB.",
        )

    filename = invoice.filename or "invoice.bin"
    content_type = invoice.content_type or "application/octet-stream"

    try:
        return run_invoice_analysis(payload, filename=filename, content_type=content_type)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis pipeline failed: {exc}",
        ) from exc
