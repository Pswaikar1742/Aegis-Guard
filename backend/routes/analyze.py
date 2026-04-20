from __future__ import annotations

import uuid

from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status

from core.models import AnalyzeResponse, ErrorResponse
from orchestrator.graph import run_invoice_analysis


router = APIRouter(tags=["analysis"])


def _error_response(
    *,
    code: str,
    message: str,
    request_id: str,
    details: str | None = None,
) -> dict[str, str]:
    return ErrorResponse(
        code=code,
        message=message,
        request_id=request_id,
        details=details,
    ).model_dump(exclude_none=True)


@router.post("/api/v1/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_invoice(response: Response, invoice: UploadFile = File(...)) -> AnalyzeResponse:
    request_id = str(uuid.uuid4())
    response.headers["X-Request-ID"] = request_id

    payload = await invoice.read()

    if not payload:
        raise HTTPException(
            status_code=400,
            detail=_error_response(
                code="EMPTY_INVOICE",
                message="Uploaded invoice is empty.",
                request_id=request_id,
            ),
        )

    if len(payload) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=_error_response(
                code="INVOICE_TOO_LARGE",
                message="Invoice file is too large. Maximum allowed size is 15MB.",
                request_id=request_id,
            ),
        )

    filename = invoice.filename or "invoice.bin"
    content_type = invoice.content_type or "application/octet-stream"

    try:
        return run_invoice_analysis(
            payload,
            filename=filename,
            content_type=content_type,
            request_id=request_id,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=_error_response(
                code="ANALYSIS_PIPELINE_ERROR",
                message="Analysis pipeline failed.",
                request_id=request_id,
                details=str(exc),
            ),
        ) from exc
