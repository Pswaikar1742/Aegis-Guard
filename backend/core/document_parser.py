from __future__ import annotations

import io

from PyPDF2 import PdfReader


def is_pdf_document(invoice_bytes: bytes, filename: str, content_type: str) -> bool:
    if invoice_bytes.startswith(b"%PDF"):
        return True
    lowered_type = (content_type or "").lower()
    if "pdf" in lowered_type:
        return True
    return filename.lower().endswith(".pdf")


def extract_text_from_pdf(invoice_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(invoice_bytes))
    page_text: list[str] = []
    for page in reader.pages:
        content = page.extract_text() or ""
        if content.strip():
            page_text.append(content)
    return "\n".join(page_text)


def extract_invoice_text(invoice_bytes: bytes, filename: str, content_type: str) -> str:
    if not is_pdf_document(invoice_bytes, filename, content_type):
        return ""
    try:
        return extract_text_from_pdf(invoice_bytes)
    except Exception:
        return ""
