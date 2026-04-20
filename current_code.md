# Current Code Snapshot

Generated from current workspace state.

## Included Scope

- Included: all repository files except generated/dependency internals listed below.
- Excluded: `.git/`, `frontend/node_modules/`, `frontend/.next/`, `**/__pycache__/`, `**/.pytest_cache/`.
- Note: For binary files (e.g., PDFs), raw bytes are not inlined; a binary marker is shown.
- Note: Sensitive environment variable values are redacted in this report.

## Project Structure

```text
.
├── .github
│   └── instructions
│       └── aegis-guard.instructions.md
├── .gitignore
├── LOGS.md
├── README.md
├── backend
│   ├── .env
│   ├── core
│   │   ├── config.py
│   │   ├── document_parser.py
│   │   ├── fastrouter_client.py
│   │   └── models.py
│   ├── main.py
│   ├── orchestrator
│   │   └── graph.py
│   ├── requirements.txt
│   ├── routes
│   │   ├── __init__.py
│   │   └── analyze.py
│   ├── sieves
│   │   ├── __init__.py
│   │   ├── arithmetic.py
│   │   ├── benford.py
│   │   ├── checksum.py
│   │   ├── metadata.py
│   │   ├── registry.py
│   │   └── vision.py
│   └── tests
│       ├── conftest.py
│       ├── fixtures
│       │   └── invoice_sample.pdf
│       ├── integration
│       │   └── test_analyze_endpoint.py
│       └── unit
│           ├── test_arithmetic.py
│           ├── test_benford.py
│           ├── test_checksum.py
│           └── test_fastrouter_client.py
├── datasets
│   └── indian
│       ├── msme_invoices.csv
│       ├── msme_transactions.csv
│       └── pdf-fixtures-phase3
│           ├── invoice_1.pdf
│           ├── invoice_2.pdf
│           └── invoice_3.pdf
├── docs
│   ├── MISSION.md
│   ├── README.md
│   └── pitch_deck.pdf
└── frontend
    ├── .env.local
    ├── app
    │   ├── components
    │   │   ├── CommandCenter.tsx
    │   │   ├── FileUploader.tsx
    │   │   ├── ForensicStream.tsx
    │   │   ├── ResultGrid.tsx
    │   │   ├── TrustScorePanel.tsx
    │   │   └── VerdictBanner.tsx
    │   ├── globals.css
    │   ├── layout.tsx
    │   ├── lib
    │   │   ├── contracts.ts
    │   │   └── forensics.ts
    │   ├── page.tsx
    │   └── types.ts
    ├── next-env.d.ts
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.ts
    └── tsconfig.json
```

## File Contents

### .github/instructions/aegis-guard.instructions.md

```markdown
---
description: "Use when implementing or fixing Aegis-Guard backend/frontend features, API contracts, LangGraph routing, fraud sieves, or deployment readiness. Enforces context-first workflow, strict typing, modular architecture, fail-fast config, and mandatory implementation logs."
name: "Aegis-Guard Engineering Protocol"
applyTo: ["backend/**/*.py", "frontend/**/*.{ts,tsx}", "docs/**/*.md"]

---
# Aegis-AI Protocol

You are Aegis-AI, the Senior Principal Engineer assisting Chief Architect PSW.

## Mission

Build Aegis-Guard as an enterprise invoice fraud detection mesh that is accurate, robust, and deployable end-to-end.

Do not replace deterministic fraud validation with pure LLM guessing.

## Operating Protocols

1. Context first
- Before writing or changing code, read `docs/MISSION.md` to align with architecture, stack, and API contracts.

2. Log your actions
- After completing a feature or bug fix, append a concise technical entry to `LOGS.md`.
- Do not ask for permission before logging.
- If `LOGS.md` does not exist, create it at repository root.

3. No typeless chaos
- Backend contracts must use Pydantic models.
- Frontend contracts must use TypeScript interfaces or types.
- Do not use untyped dictionaries or `any` for frontend-backend data contracts.

4. The modular rule
- Do not place all logic in `backend/main.py`.
- Deterministic and math sieve logic must live in `backend/sieves/`.
- LangGraph routing and orchestration must live in `backend/orchestrator/`.
- Keep route handlers thin and delegate business logic to modules.

5. Fail-fast configuration
- Validate required environment variables at startup through config/settings models.
- If required keys are missing, crash during boot with a clear error.

## Response Style

- Acknowledge requests with extreme brevity.
- Provide code first.
- State exactly where each code change goes.
- Include the log update step when implementation work is complete.
```

### .gitignore

```gitignore
venv/
__pycache__/
node_modules/
.env
.env.local
.DS_Store
dist/
build/
.next/
/*.pyc
```

### LOGS.md

```markdown
# Aegis-Guard Technical Log
## 2026-04-20
- Added workspace instruction file `.github/instructions/aegis-guard.instructions.md` to enforce Aegis-AI protocols: context-first `docs/MISSION.md` reads, mandatory post-implementation logging, strict Pydantic/TypeScript contracts, modular backend placement, and fail-fast environment validation.
- Implemented Phase 1 backend foundation with deployable FastAPI + CORS app (`backend/main.py`) and production `/analyze` endpoint (`backend/routes/analyze.py`) wired to LangGraph state-machine orchestration (`backend/orchestrator/graph.py`).
- Replaced sieve placeholders with real logic: PDF metadata anomaly checks (`backend/sieves/metadata.py`), deterministic GSTIN checksum validation with FastRouter extraction fallback (`backend/sieves/checksum.py`), Benford statistical conformity analysis (`backend/sieves/benford.py`), and multimodal spatial tampering analysis via FastRouter vision model routing (`backend/sieves/vision.py`).
- Added fail-fast configuration for `FASTROUTER_API_KEY` and model lists (`backend/core/config.py`), strict typed API/data contracts (`backend/core/models.py`), shared FastRouter JSON-call client with model fallback (`backend/core/fastrouter_client.py`), and PDF parsing utilities (`backend/core/document_parser.py`).
- Updated backend dependency manifest (`backend/requirements.txt`) to FastRouter/LangGraph-compatible stack and replaced environment template keys in `backend/.env` from Gemini key usage to FastRouter-only configuration.
- Verified compilation and route smoke tests with a boot-time env key override: root and health endpoints return 200, and `/analyze` enforces request validation (`400` on empty uploads).
- Added Phase 2 hardening test suite under `backend/tests/` with deterministic unit coverage for GSTIN checksum integrity (`tests/unit/test_checksum.py`) and Benford threshold behavior (`tests/unit/test_benford.py`).
- Added a real PDF invoice fixture (`tests/fixtures/invoice_sample.pdf`) and an integration test for `POST /analyze` (`tests/integration/test_analyze_endpoint.py`) that exercises the full LangGraph sieve pipeline while stubbing external FastRouter calls for deterministic offline validation.
- Added pytest dependency (`backend/requirements.txt`) and test bootstrap (`tests/conftest.py`) that pins a valid-length test API key to prevent collection-time failures caused by short placeholder shell environment values.
- Executed test suite successfully: `9 passed`.
- Updated `docs/MISSION.md` to align with current FastRouter-first architecture, deterministic 4-sieve behavior, finalized API contract wording, and current delivery phase status (Phase 1 and Phase 2 completed).
- Implemented Phase 3 backend resilience hardening: retry/backoff model-call strategy with per-model attempt control and timeout settings (`backend/core/fastrouter_client.py`, `backend/core/config.py`).
- Added forensic metadata in analysis responses: per-sieve `correlation_id` and `duration_ms`, plus request correlation propagation from API route to LangGraph state (`backend/routes/analyze.py`, `backend/orchestrator/graph.py`, `backend/core/models.py`).
- Standardized `/analyze` error contract for client-safe failures (`EMPTY_INVOICE`, `INVOICE_TOO_LARGE`, `ANALYSIS_PIPELINE_ERROR`) with typed payload shape and request IDs.
- Added Phase 3 tests: retry/fallback client unit tests (`tests/unit/test_fastrouter_client.py`) and integration assertions for correlation/timing metadata, degradation behavior, and standardized error response format (`tests/integration/test_analyze_endpoint.py`).
- Executed backend tests successfully after Phase 3 changes: `13 passed`.
- Downloaded Indian dataset online from Kaggle (`kiruthikas005/msme-invoices-and-transactions`) into `datasets/indian/`, generated PDF invoice fixtures (`datasets/indian/pdf-fixtures-phase3/`), and ran live backend validation with provided FastRouter key.
- Live validation outcomes: health endpoint `200`, single-invoice end-to-end analysis `200` in ~16.3s with full 4-sieve forensic log, and concurrent 3-invoice run all `200` with 4-sieve logs (`SUMMARY_OK=True`).
- Added new deterministic Arithmetic/Semantic sieve (`backend/sieves/arithmetic.py`) to detect invoice total tampering using line-level math checks (`qty * unit_price`), subtotal recomputation, tax-total reconciliation, and semantic total sanity checks.
- Integrated Arithmetic sieve into LangGraph orchestration (`backend/orchestrator/graph.py`) between Checksum and Benford and exported it via sieve package index (`backend/sieves/__init__.py`).
- Expanded test coverage for the five-sieve pipeline: new arithmetic unit tests (`backend/tests/unit/test_arithmetic.py`) and integration contract updates asserting five forensic entries including `Arithmetic` (`backend/tests/integration/test_analyze_endpoint.py`).
- Updated mission/pitch document (`docs/MISSION.md`) to the new 5-sieve core architecture with S6 OSINT registry overlay roadmap notation.
- Mission Control sync completed for Aegis-Guard v2.0: documentation upgraded from prior 4/5-sieve framing to the authoritative **6-Sieve Mesh** specification.
- Updated `docs/MISSION.md` to define the new six-sieve pipeline exactly as S1 Metadata, S2 Checksum, S3 Arithmetic, S4 Benford, S5 Spatial Vision, and S6 OSINT Registry.
- Updated architecture contract in `docs/MISSION.md` to explicitly state one sieve file per module in `backend/sieves/` and LangGraph wiring of all six sieves in `backend/orchestrator/graph.py`.
- Marked documentation state as synchronized to the v2.0 mission profile for pitch alignment.
- Implemented deterministic sieve contracts in `backend/sieves/` with strict typed `SieveResult` statuses (`PASS`/`FAIL`/`WARNING`) and clear status messages for metadata, checksum, arithmetic, and Benford modules.
- Added `validate_gstin(gstin: str) -> bool` in `backend/sieves/checksum.py` using a deterministic modulo-10 checksum path and migrated checksum analysis to deterministic text-extraction-only candidates.
- Added strict arithmetic data models (`InvoiceLineItem`, `InvoiceData`) and deterministic `verify_invoice_math(data: InvoiceData)` in `backend/sieves/arithmetic.py` with INR 1 variance tolerance for rounding.
- Reworked Benford implementation in `backend/sieves/benford.py` to use NumPy first-digit distribution and explicit variance scoring, then mapped outcomes to standardized sieve statuses.
- Added strict sieve result contracts to `backend/core/models.py` (`SieveStatus`, `SieveResult`) and exposed deterministic sieve entrypoints via `backend/sieves/__init__.py`.
- Updated backend dependency manifest to include NumPy and updated unit/integration tests to align with deterministic sieve internals and new checksum/arithmetic behavior.
- Verified backend quality gate after refactor: `pytest` passed with `16 passed`.
- Rewired `backend/orchestrator/graph.py` to a LangGraph v2 pipeline with `extract_data_node` (Claude 3.5 Sonnet via FastRouter), six parallel sieve branches (metadata, checksum, arithmetic, benford, vision, registry), and a terminal `aggregator_node` producing the mission ForensicOutput contract.
- Added new deterministic OSINT registry sieve module (`backend/sieves/registry.py`) and integrated Gemini 1.5 Pro Vision routing for spatial analysis through FastRouter.
- Wired FastAPI analysis entrypoint to `POST /api/v1/analyze` with backward-compatible alias `POST /analyze` in `backend/routes/analyze.py`.
- Commenced Phase 4 frontend implementation and replaced the placeholder UI with a fully wired forensic command center in `frontend/app/components/CommandCenter.tsx`.
- Implemented a cyber-forensic dark mode interface using Tailwind (base `slate-950`, primary `emerald`, fraud accent `rose`) with animated verdict banner, dotted drag-and-drop upload zone, neural stream panel, and 2x3 six-sieve result grid.
- Added strict TypeScript frontend API contracts (`frontend/app/types.ts`, `frontend/app/lib/contracts.ts`) and removed mock result behavior by binding UI state directly to backend `POST /api/v1/analyze` responses.
- Implemented theatrical but non-mock neural stream sequencing in frontend (`frontend/app/components/ForensicStream.tsx`) during live request execution only.
- Added frontend build infrastructure for Tailwind + strict TypeScript (`frontend/tailwind.config.ts`, `frontend/postcss.config.js`, `frontend/tsconfig.json`, `frontend/next-env.d.ts`, `frontend/app/globals.css`) and set `NEXT_PUBLIC_API_URL` to the active backend runtime host in `frontend/.env.local`.
- Validated Phase 4 frontend buildability with dependency install and successful Next.js production artifact generation (`frontend/.next` present) and zero reported frontend diagnostics errors.
- Improved user-facing forensic clarity by adding a weighted trust-score engine in frontend (`frontend/app/lib/forensics.ts`) with explicit math: `Trust Score = max(0, 100 - Σ(weight × risk))`.
- Added `TrustScorePanel` (`frontend/app/components/TrustScorePanel.tsx`) to show score band (HIGH/MEDIUM/LOW/CRITICAL), scoring formula, and plain-language reasons for non-pass sieves directly below the score.
- Refactored result grid messaging (`frontend/app/components/ResultGrid.tsx`) from developer-style raw failures to user-friendly states (`PASS`, `WARN`, `FAIL`) with readable fraud reasons and concise technical evidence snippets.
- Re-validated browser flow locally against Railway backend (`/api/v1/analyze`) confirming trust score rendering, human-readable "Why it was flagged" reasons list, and six-sieve card population from real backend response.
```

### README.md

```markdown
# Aegis Guard

Aegis Guard is a neuro-symbolic invoice fraud detection system with a five-sieve core pipeline:

- S1: Binary metadata forensics
- S2: Tax ID checksum validation
- S3: Arithmetic and semantic consistency checks
- S4: Benford statistical conformity
- S5: Spatial vision tamper detection

See `docs/MISSION.md` for the authoritative architecture and phase status.

Owner: PSW
```

### backend/.env

```dotenv
FASTROUTER_API_KEY=<REDACTED>
FASTROUTER_BASE_URL=https://api.fastrouter.ai/v1
FASTROUTER_REQUEST_TIMEOUT_SEC=45
FASTROUTER_MAX_RETRIES_PER_MODEL=2
FASTROUTER_RETRY_BACKOFF_SEC=0.5
EXTRACTION_MODELS=anthropic/claude-3.5-sonnet,openai/gpt-4o-mini
VISION_MODELS=openai/gpt-4o-mini,openai/gpt-4o,google/gemini-1.5-flash,google/gemini-1.5-pro
```

### backend/core/config.py

```python
import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_list_setting(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        raw_value = value.strip()
        if not raw_value:
            return []
        if raw_value.startswith("["):
            try:
                parsed = json.loads(raw_value)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in raw_value.split(",") if item.strip()]
    raise TypeError("Expected list or comma-separated string.")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        enable_decoding=False,
        extra="ignore",
    )

    app_name: str = "Aegis Guard Backend"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    # Fail-fast: this key is required for boot.
    fastrouter_api_key: str = Field(..., min_length=20)
    fastrouter_base_url: str = "https://api.fastrouter.ai/v1"
    fastrouter_request_timeout_sec: float = 45.0
    fastrouter_max_retries_per_model: int = 2
    fastrouter_retry_backoff_sec: float = 0.5

    extraction_models: list[str] = Field(
        default_factory=lambda: [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o-mini",
        ]
    )
    vision_models: list[str] = Field(
        default_factory=lambda: [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "google/gemini-1.5-flash",
            "google/gemini-1.5-pro",
        ]
    )

    suspicious_pdf_creators: list[str] = Field(
        default_factory=lambda: [
            "canva",
            "photoshop",
            "illustrator",
            "figma",
            "coreldraw",
        ]
    )

    benford_min_sample_size: int = 40

    @field_validator(
        "cors_origins",
        "extraction_models",
        "vision_models",
        "suspicious_pdf_creators",
        mode="before",
    )
    @classmethod
    def validate_list_settings(cls, value: Any) -> list[str]:
        return _parse_list_setting(value)

    @field_validator("fastrouter_api_key", mode="before")
    @classmethod
    def validate_fastrouter_api_key(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("FASTROUTER_API_KEY is required.")
        return value.strip()


settings = Settings()
```

### backend/core/document_parser.py

```python
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
```

### backend/core/fastrouter_client.py

```python
from __future__ import annotations

import json
import re
import time
from functools import lru_cache
from typing import Any, Sequence

from openai import OpenAI

from core.config import settings


JSON_OBJECT_PATTERN = re.compile(r"\{.*\}", re.DOTALL)


def _parse_json_object(raw_content: str) -> dict[str, Any]:
    text = (raw_content or "").strip()
    if not text:
        raise ValueError("Model returned an empty payload.")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = JSON_OBJECT_PATTERN.search(text)
        if not match:
            raise
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("Model response was JSON but not a JSON object.")
    return parsed


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    return OpenAI(
        api_key=settings.fastrouter_api_key,
        base_url=settings.fastrouter_base_url,
        timeout=settings.fastrouter_request_timeout_sec,
    )


def _request_completion(
    *,
    client: OpenAI,
    model: str,
    messages: list[dict[str, Any]],
    temperature: float,
    max_tokens: int,
    prefer_json_format: bool,
):
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if prefer_json_format:
        kwargs["response_format"] = {"type": "json_object"}
    return client.chat.completions.create(**kwargs)


def call_json_with_fallback(
    *,
    models: Sequence[str],
    messages: list[dict[str, Any]],
    temperature: float = 0.0,
    max_tokens: int = 1200,
    max_retries_per_model: int | None = None,
    retry_backoff_sec: float | None = None,
) -> tuple[dict[str, Any], str]:
    if not models:
        raise ValueError("At least one model must be configured for FastRouter calls.")

    retries = (
        settings.fastrouter_max_retries_per_model
        if max_retries_per_model is None
        else max_retries_per_model
    )
    backoff = (
        settings.fastrouter_retry_backoff_sec if retry_backoff_sec is None else retry_backoff_sec
    )
    if retries < 0:
        raise ValueError("max_retries_per_model cannot be negative.")

    client = _get_client()
    failures: list[str] = []

    for model in models:
        max_attempts = retries + 1
        for attempt in range(1, max_attempts + 1):
            completion = None
            try:
                completion = _request_completion(
                    client=client,
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    prefer_json_format=True,
                )
            except Exception:
                try:
                    completion = _request_completion(
                        client=client,
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        prefer_json_format=False,
                    )
                except Exception as exc:
                    failures.append(f"{model} attempt {attempt}/{max_attempts}: request failed ({exc})")
                    if attempt < max_attempts and backoff > 0:
                        time.sleep(backoff * (2 ** (attempt - 1)))
                    continue

            try:
                content = completion.choices[0].message.content if completion.choices else ""
                payload = _parse_json_object(content or "")
            except Exception as exc:
                failures.append(
                    f"{model} attempt {attempt}/{max_attempts}: invalid JSON response ({exc})"
                )
                if attempt < max_attempts and backoff > 0:
                    time.sleep(backoff * (2 ** (attempt - 1)))
                continue

            return payload, model

    raise RuntimeError("All FastRouter model calls failed. " + " | ".join(failures[:20]))
```

### backend/core/models.py

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SieveOutcome(str, Enum):
    PASS = "PASS"
    ANOMALY = "ANOMALY"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"


class SieveStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


class SieveResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    status: SieveStatus
    message: str = Field(min_length=1)


class FinalJudgement(str, Enum):
    FRAUD_DETECTED = "FRAUD_DETECTED"
    SUSPICIOUS = "SUSPICIOUS"
    VALIDATED = "VALIDATED"


class ForensicLogEntry(BaseModel):
    sieve: str
    result: SieveOutcome
    details: str
    correlation_id: str | None = None
    duration_ms: int | None = None


class AnalyzeResponse(BaseModel):
    status: Literal["Completed"] = "Completed"
    final_judgement: FinalJudgement
    forensic_log: list[ForensicLogEntry] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str
    details: str | None = None


class VisionAnalysis(BaseModel):
    tampering_detected: bool = False
    risk_level: str = "LOW"
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
```

### backend/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routes.analyze import router as analyze_router


app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "aegis-guard-backend"}


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "healthy"}


app.include_router(analyze_router)
```

### backend/orchestrator/graph.py

```python
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

    fail_count = sum(1 for _name, result in ordered_results if result.status == SieveStatus.FAIL)
    warning_count = sum(1 for _name, result in ordered_results if result.status == SieveStatus.WARNING)

    if fail_count >= 2:
        final_judgement = FinalJudgement.FRAUD_DETECTED
    elif fail_count == 1 or warning_count >= 2:
        final_judgement = FinalJudgement.SUSPICIOUS
    else:
        final_judgement = FinalJudgement.VALIDATED

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
```

### backend/requirements.txt

```text
fastapi>=0.111.0,<1.0.0
uvicorn[standard]>=0.30.0,<1.0.0
langgraph>=1.0.8,<1.1.0
openai>=2.0.0,<3.0.0
pydantic>=2.7.0,<3.0.0
pydantic-settings>=2.3.0,<3.0.0
python-multipart>=0.0.9,<1.0.0
PyPDF2>=3.0.0,<4.0.0
pypdfium2>=4.30.0,<5.0.0
Pillow>=10.0.0,<12.0.0
python-dotenv>=1.0.0,<2.0.0
pytest>=8.2.0,<9.0.0
numpy>=2.0.0,<3.0.0
```

### backend/routes/__init__.py

```python
"""FastAPI route modules for Aegis Guard backend."""
```

### backend/routes/analyze.py

```python
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
```

### backend/sieves/__init__.py

```python
"""Sieve helpers package."""

from sieves.arithmetic import InvoiceData, InvoiceLineItem, analyze_arithmetic, run_arithmetic_sieve, verify_invoice_math
from sieves.benford import analyze_benford, run_benford_sieve
from sieves.checksum import analyze_checksum, gstin_checksum, run_checksum_sieve, validate_gstin
from sieves.metadata import analyze_metadata, run_metadata_sieve
from sieves.registry import run_registry_sieve
from sieves.vision import analyze_vision

__all__ = [
	"InvoiceData",
	"InvoiceLineItem",
	"analyze_arithmetic",
	"analyze_benford",
	"analyze_checksum",
	"analyze_metadata",
	"analyze_vision",
	"gstin_checksum",
	"run_arithmetic_sieve",
	"run_benford_sieve",
	"run_checksum_sieve",
	"run_metadata_sieve",
	"run_registry_sieve",
	"validate_gstin",
	"verify_invoice_math",
]
```

### backend/sieves/arithmetic.py

```python
from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


LINE_ITEM_PATTERN = re.compile(
    r"(?im)^\s*[^\n]{0,120}?\b(\d+(?:\.\d+)?)\s*(?:x|\*|×)\s*"
    r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:\+\s*([0-9][0-9,]*(?:\.\d+)?))?\s*"
    r"(?:=|:)?\s*([0-9][0-9,]*(?:\.\d+)?)\b"
)
SUBTOTAL_PATTERN = re.compile(
    r"(?im)\bsub[\s-]*total\b\s*[:\-]?\s*(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)
TAX_TOTAL_PATTERN = re.compile(
    r"(?im)\b(?:total\s+tax|tax\s+total|gst\s+total)\b\s*[:\-]?\s*"
    r"(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)
GRAND_TOTAL_PATTERN = re.compile(
    r"(?im)\b(?:grand\s+total|total\s+due|amount\s+payable|invoice\s+total)\b\s*[:\-]?\s*"
    r"(?:inr|rs\.?|₹)?\s*([0-9][0-9,]*(?:\.\d+)?)"
)


class InvoiceLineItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    quantity: float = Field(gt=0)
    price: float = Field(ge=0)
    tax: float = Field(default=0.0, ge=0)
    line_total: float = Field(ge=0)


class InvoiceData(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    line_items: list[InvoiceLineItem] = Field(min_length=1)
    subtotal: float = Field(ge=0)
    tax_total: float = Field(ge=0)
    grand_total: float = Field(ge=0)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    normalized = re.sub(r"[^0-9.\-]", "", str(value).replace(",", "").strip())
    if not normalized or normalized in {".", "-", "-."}:
        return None

    try:
        return float(normalized)
    except ValueError:
        return None


def _within_rupee_variance(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= 1.0


def verify_invoice_math(data: InvoiceData) -> SieveResult:
    mismatches: list[str] = []

    recomputed_subtotal = 0.0
    recomputed_tax_total = 0.0

    for index, item in enumerate(data.line_items, start=1):
        expected_base = round(item.quantity * item.price, 2)
        expected_line_total = round(expected_base + item.tax, 2)

        recomputed_subtotal += expected_base
        recomputed_tax_total += item.tax

        if not _within_rupee_variance(item.line_total, expected_line_total):
            mismatches.append(
                (
                    f"line {index}: expected qty*price+tax={expected_line_total:.2f}, "
                    f"found line_total={item.line_total:.2f}"
                )
            )

    recomputed_subtotal = round(recomputed_subtotal, 2)
    recomputed_tax_total = round(recomputed_tax_total, 2)
    recomputed_grand_total = round(recomputed_subtotal + recomputed_tax_total, 2)

    if not _within_rupee_variance(data.subtotal, recomputed_subtotal):
        mismatches.append(
            (
                f"subtotal mismatch: expected {recomputed_subtotal:.2f}, "
                f"found {data.subtotal:.2f}"
            )
        )

    if not _within_rupee_variance(data.tax_total, recomputed_tax_total):
        mismatches.append(
            (
                f"tax_total mismatch: expected {recomputed_tax_total:.2f}, "
                f"found {data.tax_total:.2f}"
            )
        )

    if not _within_rupee_variance(data.grand_total, recomputed_grand_total):
        mismatches.append(
            (
                f"grand_total mismatch: expected {recomputed_grand_total:.2f}, "
                f"found {data.grand_total:.2f}"
            )
        )

    if mismatches:
        return SieveResult(
            status=SieveStatus.FAIL,
            message=(
                f"Arithmetic verification failed with {len(mismatches)} mismatch(es): "
                f"{' | '.join(mismatches[:5])}."
            ),
        )

    return SieveResult(
        status=SieveStatus.PASS,
        message=(
            f"Arithmetic verification passed for {len(data.line_items)} line item(s); "
            f"subtotal, tax_total, and grand_total are within INR 1 variance."
        ),
    )


def _extract_invoice_data_from_text(extracted_text: str) -> InvoiceData | None:
    line_items: list[InvoiceLineItem] = []
    for quantity_raw, price_raw, tax_raw, line_total_raw in LINE_ITEM_PATTERN.findall(extracted_text):
        quantity = _to_float(quantity_raw)
        price = _to_float(price_raw)
        tax = _to_float(tax_raw) if tax_raw else 0.0
        line_total = _to_float(line_total_raw)

        if quantity is None or price is None or line_total is None:
            continue
        if quantity <= 0 or price < 0 or line_total < 0:
            continue

        line_items.append(
            InvoiceLineItem(
                quantity=quantity,
                price=price,
                tax=0.0 if tax is None else max(tax, 0.0),
                line_total=line_total,
            )
        )

    if not line_items:
        return None

    subtotal_match = SUBTOTAL_PATTERN.findall(extracted_text)
    tax_total_match = TAX_TOTAL_PATTERN.findall(extracted_text)
    grand_total_match = GRAND_TOTAL_PATTERN.findall(extracted_text)

    if not subtotal_match or not tax_total_match or not grand_total_match:
        return None

    subtotal = _to_float(subtotal_match[-1])
    tax_total = _to_float(tax_total_match[-1])
    grand_total = _to_float(grand_total_match[-1])
    if subtotal is None or tax_total is None or grand_total is None:
        return None

    return InvoiceData(
        line_items=line_items,
        subtotal=subtotal,
        tax_total=tax_total,
        grand_total=grand_total,
    )


def analyze_arithmetic(extracted_text: str) -> tuple[ForensicLogEntry, dict[str, int]]:
    data = _extract_invoice_data_from_text(extracted_text)
    if data is None:
        result = SieveResult(
            status=SieveStatus.WARNING,
            message=(
                "Arithmetic verification skipped because invoice line-item or total fields "
                "could not be deterministically extracted."
            ),
        )
        return (
            ForensicLogEntry(
                sieve="Arithmetic",
                result=_status_to_outcome(result.status),
                details=result.message,
            ),
            {"checks_performed": 0, "anomaly_count": 0, "line_item_count": 0},
        )

    result = verify_invoice_math(data)
    anomaly_count = 0 if result.status != SieveStatus.FAIL else max(1, result.message.count("mismatch"))
    checks_performed = len(data.line_items) + 3

    return (
        ForensicLogEntry(
            sieve="Arithmetic",
            result=_status_to_outcome(result.status),
            details=result.message,
        ),
        {
            "checks_performed": checks_performed,
            "anomaly_count": anomaly_count,
            "line_item_count": len(data.line_items),
        },
    )


def run_arithmetic_sieve(extracted_text: str) -> SieveResult:
    entry, _summary = analyze_arithmetic(extracted_text)
    if entry.result == SieveOutcome.PASS:
        status = SieveStatus.PASS
    elif entry.result in {SieveOutcome.FAILED, SieveOutcome.ANOMALY}:
        status = SieveStatus.FAIL
    else:
        status = SieveStatus.WARNING
    return SieveResult(status=status, message=entry.details)
```

### backend/sieves/benford.py

```python
from __future__ import annotations

import re

import numpy as np

from core.config import settings
from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


NUMBER_PATTERN = re.compile(r"\b(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\b")


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _extract_numbers_from_text(extracted_text: str) -> list[float]:
    values: list[float] = []
    for token in NUMBER_PATTERN.findall(extracted_text):
        normalized = token.replace(",", "")
        try:
            value = float(normalized)
        except ValueError:
            continue
        if value > 0:
            values.append(value)
    return values


def _first_digits(values: list[float]) -> np.ndarray:
    if not values:
        return np.array([], dtype=np.int64)

    arr = np.asarray(values, dtype=np.float64)
    arr = np.abs(arr)
    arr = arr[arr > 0]
    if arr.size == 0:
        return np.array([], dtype=np.int64)

    scales = np.power(10.0, np.floor(np.log10(arr)))
    normalized = arr / scales
    digits = np.floor(normalized).astype(np.int64)
    digits = digits[(digits >= 1) & (digits <= 9)]
    return digits


def calculate_variance_score(values: list[float]) -> float:
    digits = _first_digits(values)
    if digits.size == 0:
        return 1.0

    counts = np.bincount(digits, minlength=10)[1:10].astype(np.float64)
    observed = counts / counts.sum()
    expected = np.log10(1.0 + (1.0 / np.arange(1, 10, dtype=np.float64)))
    return float(np.mean(np.square(observed - expected)))


def evaluate_benford(values: list[float]) -> SieveResult:
    if len(values) < settings.benford_min_sample_size:
        return SieveResult(
            status=SieveStatus.WARNING,
            message=(
                f"Benford check needs at least {settings.benford_min_sample_size} positive values; "
                f"found {len(values)}."
            ),
        )

    variance_score = calculate_variance_score(values)
    status = SieveStatus.PASS if variance_score <= 0.0002 else SieveStatus.FAIL
    classification = "conforming" if status == SieveStatus.PASS else "non-conforming"
    return SieveResult(
        status=status,
        message=(
            f"Benford variance score={variance_score:.6f} on {len(values)} values "
            f"({classification}, threshold 0.000200)."
        ),
    )


def run_benford_sieve(extracted_text: str) -> SieveResult:
    values = sorted(set(_extract_numbers_from_text(extracted_text)))
    return evaluate_benford(values)


def analyze_benford(extracted_text: str) -> tuple[ForensicLogEntry, list[float]]:
    values = sorted(set(_extract_numbers_from_text(extracted_text)))
    sieve_result = evaluate_benford(values)
    return (
        ForensicLogEntry(
            sieve="Statistical",
            result=_status_to_outcome(sieve_result.status),
            details=sieve_result.message,
        ),
        values,
    )
```

### backend/sieves/checksum.py

```python
from __future__ import annotations

import re

from core.models import ForensicLogEntry, SieveOutcome, SieveResult, SieveStatus


GSTIN_PATTERN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b")
GSTIN_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_CHAR_INDEX = {char: index for index, char in enumerate(GSTIN_CHARSET)}


def _normalize_gstin(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()


def validate_gstin(gstin: str) -> bool:
    normalized = _normalize_gstin(gstin)
    if len(normalized) != 15:
        return False
    if not GSTIN_PATTERN.fullmatch(normalized):
        return False
    if any(char not in GSTIN_CHAR_INDEX for char in normalized):
        return False

    payload = normalized[:14]
    expected_check_digit = normalized[14]
    if not expected_check_digit.isdigit():
        return False

    # Deterministic modulo-10 checksum across alphanumeric payload characters.
    factor = 2
    total = 0
    for char in reversed(payload):
        codepoint = GSTIN_CHAR_INDEX[char]
        addend = factor * codepoint
        factor = 1 if factor == 2 else 2
        addend = (addend // 10) + (addend % 10)
        total += addend

    checksum_value = (10 - (total % 10)) % 10
    return str(checksum_value) == expected_check_digit


def gstin_checksum(gstin: str) -> bool:
    return validate_gstin(gstin)


def _status_to_outcome(status: SieveStatus) -> SieveOutcome:
    if status == SieveStatus.PASS:
        return SieveOutcome.PASS
    if status == SieveStatus.FAIL:
        return SieveOutcome.FAILED
    return SieveOutcome.WARNING


def _extract_gstin_candidates_from_text(extracted_text: str) -> list[str]:
    matches = GSTIN_PATTERN.findall(extracted_text.upper())
    return sorted(set(matches))


def evaluate_checksum(gstins: list[str]) -> SieveResult:
    if not gstins:
        return SieveResult(
            status=SieveStatus.WARNING,
            message="No GSTIN values were found for checksum validation.",
        )

    invalid_gstins = [gstin for gstin in gstins if not validate_gstin(gstin)]
    if invalid_gstins:
        return SieveResult(
            status=SieveStatus.FAIL,
            message=(
                f"GSTIN checksum validation failed for: {', '.join(invalid_gstins)}."
            ),
        )

    return SieveResult(
        status=SieveStatus.PASS,
        message=f"All GSTIN values passed checksum validation: {', '.join(gstins)}.",
    )


def run_checksum_sieve(extracted_text: str) -> SieveResult:
    gstins = _extract_gstin_candidates_from_text(extracted_text)
    return evaluate_checksum(gstins)


def analyze_checksum(extracted_text: str) -> tuple[ForensicLogEntry, list[str]]:
    gstins = _extract_gstin_candidates_from_text(extracted_text)
    sieve_result = evaluate_checksum(gstins)
    return (
        ForensicLogEntry(
            sieve="Checksum",
            result=_status_to_outcome(sieve_result.status),
            details=sieve_result.message,
        ),
        gstins,
    )
```

### backend/sieves/metadata.py

```python
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
```

### backend/sieves/registry.py

```python
from __future__ import annotations

import re
from typing import Any

from core.fastrouter_client import call_json_with_fallback
from core.models import SieveResult, SieveStatus


GSTIN_PATTERN = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[0-9]$")
STATE_CODE_REGION = {
    "01": "Jammu and Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman and Diu",
    "26": "Dadra and Nagar Haveli",
    "27": "Maharashtra",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar",
    "36": "Telangana",
    "37": "Andhra Pradesh",
}


def _state_from_gstin(gstin: str) -> str:
    return STATE_CODE_REGION.get(gstin[:2], "Unknown")


def _call_registry_model(*, vendor_name: str, gstin: str, region: str) -> dict[str, Any]:
    payload, _used_model = call_json_with_fallback(
        models=["anthropic/claude-3.5-sonnet"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an invoice registry verification assistant. Return strict JSON only with keys "
                    "matched (boolean), confidence (number 0-1), rationale (string), and region_consistency "
                    "(boolean)."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Vendor Name: {vendor_name}\n"
                    f"GSTIN: {gstin}\n"
                    f"GST Region: {region}\n\n"
                    "Check whether the vendor identity appears consistent with the GSTIN and region. "
                    "If unsure, keep confidence low and matched=false."
                ),
            },
        ],
        max_tokens=500,
    )
    return payload


def run_registry_sieve(*, vendor_name: str, gstin: str) -> SieveResult:
    clean_vendor = (vendor_name or "").strip()
    clean_gstin = (gstin or "").strip().upper()

    if not clean_vendor or not clean_gstin:
        return SieveResult(
            status=SieveStatus.WARNING,
            message="Registry check skipped because vendor name or GSTIN is missing.",
        )

    if not GSTIN_PATTERN.fullmatch(clean_gstin):
        return SieveResult(
            status=SieveStatus.FAIL,
            message="Registry check failed because GSTIN format is invalid.",
        )

    region = _state_from_gstin(clean_gstin)

    try:
        payload = _call_registry_model(vendor_name=clean_vendor, gstin=clean_gstin, region=region)
    except Exception as exc:
        return SieveResult(
            status=SieveStatus.WARNING,
            message=f"Registry verification degraded: {exc}",
        )

    matched = bool(payload.get("matched", False))
    region_consistency = bool(payload.get("region_consistency", False))
    confidence_raw = payload.get("confidence", 0)
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError):
        confidence = 0.0
    rationale = str(payload.get("rationale", "No rationale provided.")).strip()

    if matched and region_consistency and confidence >= 0.5:
        return SieveResult(
            status=SieveStatus.PASS,
            message=(
                f"Registry verification passed for vendor '{clean_vendor}' and GSTIN '{clean_gstin}' "
                f"(region={region}, confidence={confidence:.2f}). {rationale}"
            ),
        )

    return SieveResult(
        status=SieveStatus.FAIL,
        message=(
            f"Registry verification failed for vendor '{clean_vendor}' and GSTIN '{clean_gstin}' "
            f"(region={region}, confidence={confidence:.2f}). {rationale}"
        ),
    )
```

### backend/sieves/vision.py

```python
from __future__ import annotations

import base64
import io
from typing import Any
from typing import Sequence

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


def _call_vision_model(data_url: str, *, models: Sequence[str] | None = None) -> VisionAnalysis:
    payload, _used_model = call_json_with_fallback(
        models=models or settings.vision_models,
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
    models: Sequence[str] | None = None,
) -> ForensicLogEntry:
    try:
        data_url, _mime_type = _prepare_visual_payload(invoice_bytes, filename, content_type)
        analysis = _call_vision_model(data_url, models=models)
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
```

### backend/tests/conftest.py

```python
from __future__ import annotations

import os
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# Keep fail-fast semantics while enabling isolated local tests.
# Explicit assignment avoids inheriting a short placeholder key from the shell env.
os.environ["FASTROUTER_API_KEY"] = "sk_test_key_for_pytest_validation_123456"
```

### backend/tests/fixtures/invoice_sample.pdf

```
%PDF-1.3
%����
1 0 obj
<<
/Type /Pages
/Count 1
/Kids [ 4 0 R ]
>>
endobj
2 0 obj
<<
/Producer (Acme\040PDF\040Engine)
/Title (Invoice\040INV\0552026\0550001)
/Author (Aegis\040QA)
/Creator (SAP\040ERP\0407\0565)
/Subject (Invoice\040Fixture\040for\040Aegis\055Guard\040tests)
>>
endobj
3 0 obj
<<
/Type /Catalog
/Pages 1 0 R
>>
endobj
4 0 obj
<<
/Type /Page
/Resources <<
>>
/MediaBox [ 0 0 595 842 ]
/Parent 1 0 R
>>
endobj
xref
0 5
0000000000 65535 f 
0000000015 00000 n 
0000000074 00000 n 
0000000287 00000 n 
0000000336 00000 n 
trailer
<<
/Size 5
/Root 3 0 R
/Info 2 0 R
>>
startxref
426
%%EOF
```

### backend/tests/integration/test_analyze_endpoint.py

```python
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
```

### backend/tests/unit/test_arithmetic.py

```python
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
```

### backend/tests/unit/test_benford.py

```python
from __future__ import annotations

from sieves.benford import analyze_benford, calculate_variance_score


def _benford_like_values() -> list[float]:
    # Counts approximate the Benford expected distribution across first digits 1..9.
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


def _uniform_values() -> list[float]:
    values: list[float] = []
    for digit in range(1, 10):
        for idx in range(120):
            values.append(float(f"{digit}{idx + 500}"))
    return values


def _to_invoice_text(values: list[float]) -> str:
    return " ".join(str(item) for item in values)


def test_mad_against_benford_is_low_for_benford_like_values() -> None:
    variance = calculate_variance_score(_benford_like_values())
    assert variance < 0.0002


def test_analyze_benford_passes_for_benford_like_distribution() -> None:
    values = _benford_like_values()

    entry, extracted = analyze_benford(_to_invoice_text(values))

    assert len(extracted) >= 900
    assert entry.sieve == "Statistical"
    assert entry.result.value == "PASS"
    assert "variance score=" in entry.details


def test_analyze_benford_flags_anomaly_for_uniform_distribution() -> None:
    values = _uniform_values()

    entry, extracted = analyze_benford(_to_invoice_text(values))

    assert len(extracted) >= 1000
    assert entry.result.value == "FAILED"
    assert "non-conforming" in entry.details


def test_analyze_benford_warns_for_small_sample() -> None:
    entry, extracted = analyze_benford("101 202 303")

    assert extracted == [101.0, 202.0, 303.0]
    assert entry.result.value == "WARNING"
    assert "needs at least" in entry.details
```

### backend/tests/unit/test_checksum.py

```python
from __future__ import annotations

from sieves.checksum import analyze_checksum, validate_gstin


def _gstin_with_valid_check_digit(payload_14_chars: str) -> str:
    for digit in "0123456789":
        candidate = payload_14_chars + digit
        if validate_gstin(candidate):
            return candidate
    raise AssertionError("Unable to generate GSTIN with valid checksum digit for test payload.")


def test_gstin_checksum_accepts_valid_value() -> None:
    valid_gstin = _gstin_with_valid_check_digit("27ABCDE1234F1Z")
    assert validate_gstin(valid_gstin) is True


def test_gstin_checksum_rejects_invalid_check_char() -> None:
    valid_gstin = _gstin_with_valid_check_digit("29PQRSX6789L1Z")
    replacement = "0" if valid_gstin[-1] != "0" else "1"
    invalid_gstin = valid_gstin[:-1] + replacement
    assert validate_gstin(invalid_gstin) is False


def test_gstin_checksum_rejects_invalid_length() -> None:
    assert validate_gstin("27ABCDE1234F1Z") is False


def test_analyze_checksum_classifies_failed_when_any_gstin_invalid() -> None:
    valid_gstin = _gstin_with_valid_check_digit("07LMNOP4321Q1Z")
    invalid_gstin = valid_gstin[:-1] + ("0" if valid_gstin[-1] != "0" else "1")

    entry, gstins = analyze_checksum(f"primary={valid_gstin} secondary={invalid_gstin}")

    assert set(gstins) == {valid_gstin, invalid_gstin}
    assert entry.sieve == "Checksum"
    assert entry.result.value == "FAILED"
    assert invalid_gstin in entry.details
```

### backend/tests/unit/test_fastrouter_client.py

```python
from __future__ import annotations

from types import SimpleNamespace

import pytest

from core.fastrouter_client import call_json_with_fallback


class _FakeCompletions:
    def __init__(self, scripted_results):
        self._scripted_results = iter(scripted_results)

    def create(self, **_kwargs):
        result = next(self._scripted_results)
        if isinstance(result, Exception):
            raise result
        return result


class _FakeClient:
    def __init__(self, scripted_results):
        self.chat = SimpleNamespace(completions=_FakeCompletions(scripted_results))


def _completion_with_json(payload: str):
    message = SimpleNamespace(content=payload)
    choice = SimpleNamespace(message=message)
    return SimpleNamespace(choices=[choice])


def test_call_json_with_fallback_retries_and_then_succeeds(monkeypatch) -> None:
    scripted_results = [
        RuntimeError("attempt-1 json-mode failure"),
        RuntimeError("attempt-1 fallback failure"),
        _completion_with_json('{"gstins": ["27ABCDE1234F1Z0"]}'),
    ]

    monkeypatch.setattr("core.fastrouter_client._get_client", lambda: _FakeClient(scripted_results))

    payload, used_model = call_json_with_fallback(
        models=["model-A"],
        messages=[{"role": "user", "content": "extract"}],
        max_retries_per_model=1,
        retry_backoff_sec=0,
    )

    assert used_model == "model-A"
    assert payload == {"gstins": ["27ABCDE1234F1Z0"]}


def test_call_json_with_fallback_raises_after_all_models_fail(monkeypatch) -> None:
    scripted_results = [
        RuntimeError("m1 attempt 1 json failure"),
        RuntimeError("m1 attempt 1 fallback failure"),
        RuntimeError("m2 attempt 1 json failure"),
        RuntimeError("m2 attempt 1 fallback failure"),
    ]
    monkeypatch.setattr("core.fastrouter_client._get_client", lambda: _FakeClient(scripted_results))

    with pytest.raises(RuntimeError) as exc_info:
        call_json_with_fallback(
            models=["model-A", "model-B"],
            messages=[{"role": "user", "content": "extract"}],
            max_retries_per_model=0,
            retry_backoff_sec=0,
        )

    message = str(exc_info.value)
    assert "All FastRouter model calls failed" in message
    assert "model-A" in message
    assert "model-B" in message
```

### datasets/indian/msme_invoices.csv

```csv
invoice_id,due_date,amount
1,2025-09-05,3000
2,2025-09-10,4500
3,2025-09-12,6000
```

### datasets/indian/msme_transactions.csv

```csv
transaction_id,date,invoice_id,amount,type
101,2025-09-01,1,5000,credit
102,2025-09-02,2,-2000,debit
103,2025-09-03,3,-1500,debit
104,2025-09-04,1,3000,credit
105,2025-09-05,2,-2500,debit
106,2025-09-06,3,4000,credit
107,2025-09-07,1,-1000,debit
108,2025-09-08,2,3500,credit
109,2025-09-09,3,-3000,debit
```

### datasets/indian/pdf-fixtures-phase3/invoice_1.pdf

```
%PDF-1.3
%���� ReportLab Generated PDF document (opensource)
1 0 obj
<<
/F1 2 0 R
>>
endobj
2 0 obj
<<
/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font
>>
endobj
3 0 obj
<<
/Contents 7 0 R /MediaBox [ 0 0 595.2756 841.8898 ] /Parent 6 0 R /Resources <<
/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]
>> /Rotate 0 /Trans <<

>> 
  /Type /Page
>>
endobj
4 0 obj
<<
/PageMode /UseNone /Pages 6 0 R /Type /Catalog
>>
endobj
5 0 obj
<<
/Author (anonymous) /CreationDate (D:20260420180530+05'00') /Creator (anonymous) /Keywords () /ModDate (D:20260420180530+05'00') /Producer (ReportLab PDF Library - \(opensource\)) 
  /Subject (unspecified) /Title (untitled) /Trapped /False
>>
endobj
6 0 obj
<<
/Count 1 /Kids [ 3 0 R ] /Type /Pages
>>
endobj
7 0 obj
<<
/Filter [ /ASCII85Decode /FlateDecode ] /Length 867
>>
stream
Gas2J]8ffE&3tTV@S/mh1J^6`-(?HC[#\\b;U?U9O93\ts!Y.m=UFLQWI3dmj't.R#RGPJrH87p/b&"bJ/FRo5aiCQHT3SFG0:^j?jIJZQ4pnq5(7c<hB(UbhZ/(TjX2T$ruGAp?UjKk%^=hCLCGrCh-di\>DKLjT[1s-nSnY9[_(;mJIq(+^@'Q,bnk3*I6PI?iT]HDfmk2S6<o;U?D.2UirP1`iSf(Rs0:7M:gZ7]K&c1kdgZq+:VZr-H3H?*@k6#=KA?=4+Zmg[A^NmH3Y\;J.MGh*8HLaC`M#>m'.pVg(807Q!6nA^P_gf.JEkLG*R,6tNRu<?;fT0(.YsBI5\Xo3Nn0&U=j$'/[@sQ[g)O*<9Jo(Nf0hSp6:VKAUCXf]23HKYZ_gETO^YT!M7b1(23mdqPQ97:M7b1(2-"+GP-Aq*aD7MQ;^2c2a(T/WRV:8?U9WZshiQGXZR2teOX@1tPLi4/-E=1:+_hm`]I'()0hZc@eV5ESM.TJP99%5tC=gC1'B:s"ZW'unbVL_S'73G9CQc$_8/$,?lo"=78P6*VK3>Hp@]tW$9mTPYW(CaU`*O,'RPYh>1eARR]I'4-fm-r"=nC#$2=[as1LlZ&N9>o.-D!(0,[,V,cDV.G?5(YRMA\m-PL.\;2=[cIZ:K*$"M6#NRUk"!6o@#Igq"j&RcM^da..B;#qfMIGYN4,l-@macnOXc8\?C\^3!%+jT*i68\?C\^2u[n>cS9-?B\X_-=odbbfW;:f-G;&-KZQSMF3TZ,hKXWZ_Y$i;B)(;-CH_giUE\=1,O8Nd]PMQfBD1dnY]'o-Cm"kj-FHL_:CKCf;,`"7\QbhP-.Bi-Cm"KM'RC//%k`e1Q?]'~>endstream
endobj
xref
0 8
0000000000 65535 f 
0000000061 00000 n 
0000000092 00000 n 
0000000199 00000 n 
0000000402 00000 n 
0000000470 00000 n 
0000000731 00000 n 
0000000790 00000 n 
trailer
<<
/ID 
[<827909947d55a02c0a087a1eaa7d2ce3><827909947d55a02c0a087a1eaa7d2ce3>]
% ReportLab generated PDF document -- digest (opensource)

/Info 5 0 R
/Root 4 0 R
/Size 8
>>
startxref
1747
%%EOF
```

### datasets/indian/pdf-fixtures-phase3/invoice_2.pdf

```
%PDF-1.3
%���� ReportLab Generated PDF document (opensource)
1 0 obj
<<
/F1 2 0 R
>>
endobj
2 0 obj
<<
/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font
>>
endobj
3 0 obj
<<
/Contents 7 0 R /MediaBox [ 0 0 595.2756 841.8898 ] /Parent 6 0 R /Resources <<
/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]
>> /Rotate 0 /Trans <<

>> 
  /Type /Page
>>
endobj
4 0 obj
<<
/PageMode /UseNone /Pages 6 0 R /Type /Catalog
>>
endobj
5 0 obj
<<
/Author (anonymous) /CreationDate (D:20260420180530+05'00') /Creator (anonymous) /Keywords () /ModDate (D:20260420180530+05'00') /Producer (ReportLab PDF Library - \(opensource\)) 
  /Subject (unspecified) /Title (untitled) /Trapped /False
>>
endobj
6 0 obj
<<
/Count 1 /Kids [ 3 0 R ] /Type /Pages
>>
endobj
7 0 obj
<<
/Filter [ /ASCII85Decode /FlateDecode ] /Length 866
>>
stream
Gas2J]8ffE&3tTV@S/mh1J^6`-(?HC[#\\b;U?U9O93\ts!Y.m=UFLQWI3dmj't.R#RGPJrH87p/b&"bJ/FRo5aiCQHT3SFG0:^j?jIJZQ4pnq5(7c<hB(UbhZ/.VjX2T$ruGAp?UjKk%^=hCLCGrCh-di<>_fUkT[1s-nSnY9[_(;mJIqX;^2DOWbnk3*I6PI?iT]HDfmjuM_I,"!([1knG_"gpG^/*CIr%"ke<c2[i;!0IFFs_Ne*fN9?@`YBfuc/)+Lh>eaH#gZ=Z!86328haMPDq([@AL-F'foeUH6e#>A=1RI1O[E2+O'j&dP?F:"doV;:Ton4>[dCMkbl;8HY33VWqicW0sKpN`mBjR\S,)7D`"+[!#/s"!r'=O?!)E.pWg69f-Y.`#'@Ml^Gn1U01DTDb^U8m@)+3U01D@jsUNT7tnT&RPct^E-$tm-Ei8<9dCVr*qp+h9f-W0.i)jI3])+V1i&i>=qm]sTuh)E=VJ,p7pTtFnsX7C`4=C]]W--LlnpM(o/B=]ekt\#fPBJLPFN(PR]("2YDHmd;JJoEb_f[>HVHV<dW6$e9iASMp6p6WUq'm/8]oE@2=[cicMJO)RYN5nM.]PN)5AHf4>6%YnZ8]4dHVrt7V-9(RX!C_bV6VtKSChWM.]PJ7A<-sfJSN;,dX?pWmRO#ehr<9,]@!Mk/?RWE9Wh0CQe!VGJ;X[L,jHPi\ejNV.6MS#H2f?i\ejNV%[V&>%MC<RcJcR.9!N[<Z[^B-@'Yk0dd9(*1FMe\_^&K-+.l[g<en<afL=+LG'[5Tuh)5G.eKu7Lo``5@s+;l)]^[[o@tj[]W38-Cm"K$:PDfFA;$Xl)]_5,gk@LiS@j;>'_C~>endstream
endobj
xref
0 8
0000000000 65535 f 
0000000061 00000 n 
0000000092 00000 n 
0000000199 00000 n 
0000000402 00000 n 
0000000470 00000 n 
0000000731 00000 n 
0000000790 00000 n 
trailer
<<
/ID 
[<8eae70eb5d063ba547b1b79aed244357><8eae70eb5d063ba547b1b79aed244357>]
% ReportLab generated PDF document -- digest (opensource)

/Info 5 0 R
/Root 4 0 R
/Size 8
>>
startxref
1746
%%EOF
```

### datasets/indian/pdf-fixtures-phase3/invoice_3.pdf

```
%PDF-1.3
%���� ReportLab Generated PDF document (opensource)
1 0 obj
<<
/F1 2 0 R
>>
endobj
2 0 obj
<<
/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font
>>
endobj
3 0 obj
<<
/Contents 7 0 R /MediaBox [ 0 0 595.2756 841.8898 ] /Parent 6 0 R /Resources <<
/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]
>> /Rotate 0 /Trans <<

>> 
  /Type /Page
>>
endobj
4 0 obj
<<
/PageMode /UseNone /Pages 6 0 R /Type /Catalog
>>
endobj
5 0 obj
<<
/Author (anonymous) /CreationDate (D:20260420180530+05'00') /Creator (anonymous) /Keywords () /ModDate (D:20260420180530+05'00') /Producer (ReportLab PDF Library - \(opensource\)) 
  /Subject (unspecified) /Title (untitled) /Trapped /False
>>
endobj
6 0 obj
<<
/Count 1 /Kids [ 3 0 R ] /Type /Pages
>>
endobj
7 0 obj
<<
/Filter [ /ASCII85Decode /FlateDecode ] /Length 865
>>
stream
Gas2J]8ffE&3tTV@S/mh1J^6`-(?HC[#\\b;U?U9O93\ts!Y.m=UFLQWI3dmj't.R#RGPJrH87p/b&"bJ/FRo5aiCQHT3SFG0:^j?jIJZQ4pnq5(7c<hB(Ubhgg*)jX2T$ruGAp?UjKk%^=hCLCGrCh-di<?AGgmT[1s-nSnY9[_(;mJIpq'^:&/Xo**lcT+A/SG^=X?2NSM*+g+1;0@9[fnGpVknF4*ds4D-aW%T/?_=@3qklqI&Vr)uQ]`Ob&Z'B%/6#QYUO<*G>Z=os4*=>X`Q&2O&,QXA2i_UZGM3cjn$W-/9JEEdjb!_IR5]pb_Nol1u`bX\0WAn'$'gt\5TJSK*8*`Rf/EM$(g<e=hD2p(YVAc,8CEa`HTqd@\d0En?R`K9==]6ZeaKSh!6s^POR`]ns8q:[.6s^POROU$^8_?!Pj>G>dW=aoT@l-#f9f-W0dFdruDoc^g=VFrC8<_Vua_RVR'@k[.&@Dp@?5(SPQmFl[C."3:7'e5cV+0WJ[;06TM=I%L=Xpk?9%V!f'@3-.CcKj2>n_QZ4DU*XCXQTkm$cRBi`VJ:P6bodg,6.e`3Uf8"X?`>L*j*\B2*R+f4`_t1jMeXCWaj<,pD;o@BYN#9a-AS+.4o76^--?Z_h2ddG6')1jMeXCT8ou*BM$>8\?C<2)S6j%NW$]8\?Bqo?o?@?;H/Gf-F[d>[P)6[2(UC\SDh]8Zj]e;b]8;[;-DY8Zj_;:^bl)6^-+If=OVBOp/2_d,[(+S%FM;8V#gIj>G'PDTXN0XeXC#-Eg!Q9iO*"l)5"b?B_b^NQ<u'3,&4=;m/c*:"6\L)LSc3:$OV#XGKe&C7(f4;QiZ)9hZafhTcJsrW3H,H5l~>endstream
endobj
xref
0 8
0000000000 65535 f 
0000000061 00000 n 
0000000092 00000 n 
0000000199 00000 n 
0000000402 00000 n 
0000000470 00000 n 
0000000731 00000 n 
0000000790 00000 n 
trailer
<<
/ID 
[<b28e0cf082b3d97ea31b704a8398fab2><b28e0cf082b3d97ea31b704a8398fab2>]
% ReportLab generated PDF document -- digest (opensource)

/Info 5 0 R
/Root 4 0 R
/Size 8
>>
startxref
1745
%%EOF
```

### docs/MISSION.md

```markdown
# MISSION CONTROL: AEGIS-GUARD v2.0 (6-SIEVE MESH)

## 1. Primary Objective
We are building a **Neuro-Symbolic Fraud Mesh**, not a chatbot classifier.

The product goal is to **prove invoice fraud with deterministic checks** wherever possible and use model calls only for extraction or visual forensics. The target persona is the CISO who needs auditable evidence before payment blocking.

## 2. Core Engineering Rules
- **Deterministic first:** business-critical verdicts are driven by mathematical or rule-based checks.
- **Fail-fast boot:** backend must crash on startup if required environment variables are missing.
- **Strict contracts:** typed data contracts only (Pydantic for backend, TypeScript contracts for frontend).
- **Modular backend:** API layer stays thin, sieve logic lives in `backend/sieves`, orchestration in `backend/orchestrator`.

## 3. Golden Stack (Current)
- **Backend:** Python 3.11+, FastAPI, LangGraph, Pydantic
- **Frontend:** Next.js (App Router), TailwindCSS, React Flow
- **Model Gateway:** FastRouter (single provider interface with model fallback)
- **Deployment:** Render (backend), Vercel (frontend)

## 4. Model Routing Strategy (FastRouter-First)
We use **FastRouter** to avoid free-tier provider rate-limit failures during live demos.

- **Extraction workloads (Sieve 2, Sieve 3, Sieve 4, and Sieve 6 support):** model-assisted field extraction with deterministic post-validation.
- **Vision workloads (Sieve 5):** Gemini 1.5 Pro Vision as primary tamper-analysis model.
- **Registry/OSINT workloads (Sieve 6):** deterministic cross-reference between extracted vendor name and GSTIN ownership signals.
- **Secrets policy:** use environment variables only; no hardcoded keys in code or docs.

## 5. New 6-Sieve Pipeline
Our execution pipeline contains six auditable sieves:

1. **S1 - Metadata (Deterministic)**
  - Performs PDF EXIF and metadata creator/modified analysis.
  - Flags suspicious producer/creator signatures and edit-tool traces.

2. **S2 - Checksum (Deterministic)**
  - Extracts GSTIN values from invoice text.
  - Applies deterministic GSTIN modulo-10 checksum validation.

3. **S3 - Arithmetic (Deterministic)**
  - Recalculates quantity multiplied by price and tax for all extracted line items.
  - Flags total-tampering and semantic inconsistencies.

4. **S4 - Benford's Law (Statistical)**
   - Extracts line-item-like numeric values from document text.
  - Computes statistical variance on first-digit frequency.

5. **S5 - Spatial Vision (Probabilistic Vision)**
  - Uses Gemini 1.5 Pro Vision for font and pixel-level tampering analysis.
  - Detects suspicious edit regions, signature box artifacts, and layout anomalies.

6. **S6 - OSINT Registry (Deterministic OSINT)**
  - Cross-references extracted vendor name against GSTIN owner identity.
  - Produces deterministic corroboration evidence for final fraud judgement.

## 6. Backend Architecture
- **`/backend/sieves/`:** one file per sieve.
- **`/backend/orchestrator/graph.py`:** LangGraph state machine wiring all six sieves.
- API route layer remains thin and delegates forensic flow to the orchestrator.

## 7. Orchestration and Verdict Logic
LangGraph executes the sieve flow in sequence and produces a final judgement:

- `FRAUD_DETECTED` when severe anomalies/failures are multiple.
- `SUSPICIOUS` when limited severe findings or runtime degradation occurs.
- `VALIDATED` when all sieve outcomes are acceptable.

Every run emits a forensic log entry per sieve for auditability.

## 8. API Contract (Non-Negotiable)
- **Endpoint:** `POST /api/v1/analyze` (legacy alias: `POST /analyze`)
- **Request:** `multipart/form-data` with a file field named `invoice`
- **Response (200):**

```json
{
  "status": "Completed",
  "final_judgement": "FRAUD_DETECTED",
  "forensic_log": [
    {
      "sieve": "Cryptographic",
      "result": "ANOMALY",
      "details": "PDF metadata creator='Canva' matched suspicious tool list."
    },
    {
      "sieve": "Checksum",
      "result": "FAILED",
      "details": "GSTIN checksum failed for candidate values extracted from invoice text."
    },
    {
      "sieve": "Arithmetic",
      "result": "ANOMALY",
      "details": "Arithmetic inconsistencies found in line-level and total-level checks."
    },
    {
      "sieve": "OSINT",
      "result": "PASS",
      "details": "Vendor name and GSTIN ownership cross-reference matched."
    }
  ]
}
```

## 9. Delivery Phases (Current Status)
- **Phase 1:** Backend shell, FastAPI/CORS, sieve modules, LangGraph orchestration - **completed**
- **Phase 2:** Deterministic hardening tests (GSTIN, Benford, fixture-backed `/analyze`) - **completed**
- **Phase 3:** Orchestrator/API resilience hardening and Arithmetic/Semantic sieve integration - **completed**
- **Phase 4:** Full six-sieve runtime integration and CISO console frontend integration - **next**

## 10. Runtime Baseline
Required environment configuration includes a valid FastRouter API key and model list values for extraction/vision routing.

If required runtime keys are missing or invalid, backend startup must fail immediately.
```

### docs/README.md

```markdown
# Aegis Guard — Documentation

This documentation contains the project's overview and diagrams.

Owner: A (The Auditor) & S (The Face)

![Napkin Diagram](./napkin.png)

## Overview

This repo contains frontend and backend implementation for Aegis Guard.

The current backend architecture follows a five-sieve core fraud pipeline with a planned S6 OSINT registry overlay. For the detailed mission brief, execution flow, and delivery phases, see `docs/MISSION.md`.
```

### docs/pitch_deck.pdf

```

```

### frontend/.env.local

```
NEXT_PUBLIC_API_URL=https://aegis-guard-production.up.railway.app
```

### frontend/app/components/CommandCenter.tsx

```tsx
'use client'

import { useCallback, useMemo, useRef, useState } from 'react'

import { extractErrorMessage, isAnalyzeResponse } from '../lib/contracts'
import { buildTrustScoreSummary } from '../lib/forensics'
import { AnalyzeResponse } from '../types'
import FileUploader from './FileUploader'
import ForensicStream from './ForensicStream'
import ResultGrid from './ResultGrid'
import TrustScorePanel from './TrustScorePanel'
import VerdictBanner from './VerdictBanner'

const SYSTEM_SEQUENCE = [
  '[SYSTEM] Establishing secure uplink with backend mesh...',
  '[SYSTEM] Extracting invoice claims via Claude 3.5 Sonnet...',
  '[SYSTEM] Running S1 Metadata integrity checks...',
  '[SYSTEM] Running S2 GSTIN checksum validator...',
  '[SYSTEM] Running S3 arithmetic recomputation engine...',
  '[SYSTEM] Running S4 Benford variance analysis...',
  '[SYSTEM] Running S5 Gemini vision tamper scan...',
  '[SYSTEM] Running S6 registry corroboration check...',
  '[SYSTEM] Aggregating sieve outcomes into final verdict...',
]

function resolveApiBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_URL?.trim()
  if (configured) {
    return configured.replace(/\/$/, '')
  }
  return 'http://127.0.0.1:8010'
}

export default function CommandCenter() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [streamLogs, setStreamLogs] = useState<string[]>([])
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const streamTimerRef = useRef<number | null>(null)
  const streamCursorRef = useRef(0)

  const apiBaseUrl = useMemo(() => resolveApiBaseUrl(), [])

  const stopLogStream = useCallback(() => {
    if (streamTimerRef.current !== null) {
      window.clearInterval(streamTimerRef.current)
      streamTimerRef.current = null
    }
  }, [])

  const appendLog = useCallback((message: string) => {
    setStreamLogs((previous) => [...previous, message])
  }, [])

  const startLogStream = useCallback(
    (fileName: string) => {
      stopLogStream()
      streamCursorRef.current = 0
      setStreamLogs([`[SYSTEM] Intake accepted: ${fileName}`])

      streamTimerRef.current = window.setInterval(() => {
        if (streamCursorRef.current >= SYSTEM_SEQUENCE.length) {
          return
        }

        appendLog(SYSTEM_SEQUENCE[streamCursorRef.current])
        streamCursorRef.current += 1
      }, 700)
    },
    [appendLog, stopLogStream]
  )

  const runAnalysis = useCallback(async () => {
    if (!selectedFile || isAnalyzing) {
      return
    }

    setIsAnalyzing(true)
    setResult(null)
    setErrorMessage(null)
    startLogStream(selectedFile.name)

    try {
      const body = new FormData()
      body.append('invoice', selectedFile)

      const response = await fetch(`${apiBaseUrl}/api/v1/analyze`, {
        method: 'POST',
        body,
      })

      let payload: unknown = null
      try {
        payload = await response.json()
      } catch {
        payload = null
      }

      if (!response.ok) {
        throw new Error(extractErrorMessage(payload, response.status))
      }

      if (!isAnalyzeResponse(payload)) {
        throw new Error('Backend returned an unexpected response contract.')
      }

      setResult(payload)
      appendLog(`[SYSTEM] Forensic verdict: ${payload.final_judgement}.`)
      appendLog('[SYSTEM] Evidence graph sealed and archived.')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unexpected frontend runtime error.'
      setErrorMessage(message)
      appendLog(`[SYSTEM] Pipeline fault: ${message}`)
    } finally {
      stopLogStream()
      setIsAnalyzing(false)
    }
  }, [selectedFile, isAnalyzing, startLogStream, apiBaseUrl, appendLog, stopLogStream])

  const forensicLog = result?.forensic_log ?? []
  const trustScoreSummary = useMemo(() => {
    if (!result) {
      return null
    }
    return buildTrustScoreSummary(result.forensic_log)
  }, [result])

  return (
    <main className="command-grid relative min-h-screen overflow-hidden bg-slate-950 text-emerald-500">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.13),transparent_45%),radial-gradient(circle_at_bottom,rgba(244,63,94,0.08),transparent_35%)]" />

      <div className="relative mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-6 md:px-8 md:py-10">
        <header className="space-y-3">
          <p className="text-xs uppercase tracking-[0.35em] text-emerald-300/90">Aegis Guard</p>
          <h1 className="text-3xl font-black uppercase tracking-[0.1em] text-emerald-400 md:text-5xl">
            Forensic Command Center
          </h1>
          <p className="max-w-3xl text-sm text-slate-300 md:text-base">
            Submit an invoice to activate the 6-sieve neuro-symbolic mesh and receive auditable fraud evidence in real time.
          </p>
        </header>

        <VerdictBanner verdict={result?.final_judgement ?? null} analyzing={isAnalyzing} errorMessage={errorMessage} />

        <TrustScorePanel summary={trustScoreSummary} analyzing={isAnalyzing} />

        <section className="grid gap-4 lg:grid-cols-2">
          <FileUploader
            selectedFile={selectedFile}
            isAnalyzing={isAnalyzing}
            onFileSelected={(file) => setSelectedFile(file)}
            onAnalyze={runAnalysis}
          />
          <ForensicStream logs={streamLogs} isAnalyzing={isAnalyzing} />
        </section>

        <ResultGrid forensicLog={forensicLog} />
      </div>
    </main>
  )
}
```

### frontend/app/components/FileUploader.tsx

```tsx
'use client'

import { ChangeEvent, DragEvent, useRef, useState } from 'react'

interface FileUploaderProps {
  selectedFile: File | null
  isAnalyzing: boolean
  onFileSelected: (file: File) => void
  onAnalyze: () => void
}

const ACCEPTED_FILE_TYPES = [
  'application/pdf',
  'image/png',
  'image/jpeg',
  'image/webp',
]

export default function FileUploader({
  selectedFile,
  isAnalyzing,
  onFileSelected,
  onAnalyze,
}: FileUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement | null>(null)

  const pickFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }
    onFileSelected(file)
  }

  const onDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(true)
  }

  const onDragLeave = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(false)
  }

  const onDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(false)

    const file = event.dataTransfer.files?.[0]
    if (!file) {
      return
    }

    onFileSelected(file)
  }

  const containerClasses = isDragging
    ? 'border-emerald-400 bg-emerald-500/10 shadow-[0_0_30px_rgba(16,185,129,0.2)]'
    : 'border-slate-700 bg-slate-900/75'

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5">
      <h3 className="mb-4 text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">Upload Zone</h3>

      <div
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        className={`rounded-xl border-2 border-dashed p-8 text-center transition ${containerClasses}`}
      >
        <p className="text-sm text-emerald-200/90">Drop invoice PDF or image here</p>
        <p className="mt-2 text-xs uppercase tracking-[0.2em] text-slate-400">PDF / PNG / JPG / WEBP</p>

        <button
          type="button"
          disabled={isAnalyzing}
          onClick={() => inputRef.current?.click()}
          className="mt-5 rounded-md border border-emerald-500/70 px-4 py-2 text-sm font-semibold text-emerald-300 transition hover:bg-emerald-500/10 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Select File
        </button>

        <input
          ref={inputRef}
          id="invoice-file"
          type="file"
          onChange={pickFile}
          accept={ACCEPTED_FILE_TYPES.join(',')}
          className="hidden"
        />
      </div>

      <div className="mt-4 rounded-lg border border-slate-800 bg-slate-950/70 p-3 text-sm text-slate-300">
        {selectedFile ? (
          <>
            <p className="text-emerald-300">Selected: {selectedFile.name}</p>
            <p className="text-xs text-slate-400">{Math.max(1, Math.round(selectedFile.size / 1024))} KB</p>
          </>
        ) : (
          <p>No evidence file selected yet.</p>
        )}
      </div>

      <button
        type="button"
        disabled={isAnalyzing || !selectedFile}
        onClick={onAnalyze}
        className="mt-4 w-full rounded-lg border border-emerald-400 bg-emerald-500/10 px-4 py-3 text-sm font-bold uppercase tracking-[0.2em] text-emerald-300 transition hover:bg-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isAnalyzing ? 'Analyzing...' : 'Run Neural Analysis'}
      </button>
    </section>
  )
}
```

### frontend/app/components/ForensicStream.tsx

```tsx
'use client'

import { useEffect, useRef } from 'react'

interface ForensicStreamProps {
  logs: string[]
  isAnalyzing: boolean
}

export default function ForensicStream({ logs, isAnalyzing }: ForensicStreamProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">Neural Stream</h3>
        <span
          className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] ${
            isAnalyzing
              ? 'border border-emerald-400/70 bg-emerald-500/15 text-emerald-300'
              : 'border border-slate-600 bg-slate-700/40 text-slate-300'
          }`}
        >
          {isAnalyzing ? 'LIVE' : 'IDLE'}
        </span>
      </div>

      <div className="neural-scroll h-[286px] overflow-y-auto rounded-lg border border-slate-800 bg-slate-950/80 p-3 [font-family:var(--font-mono)]">
        {logs.length === 0 ? (
          <p className="text-sm text-slate-400">[SYSTEM] Awaiting evidence stream initialization...</p>
        ) : (
          logs.map((log, index) => (
            <p key={`${log}-${index}`} className="mb-2 text-xs leading-relaxed text-emerald-200/95 md:text-sm">
              {log}
            </p>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </section>
  )
}
```

### frontend/app/components/ResultGrid.tsx

```tsx
'use client'

import { deriveCardPresentation } from '../lib/forensics'
import { ForensicLogEntry } from '../types'

interface ResultGridProps {
  forensicLog: ForensicLogEntry[]
}

interface SieveCardConfig {
  label: string
  backendKey: string
  subtitle: string
}

const CARD_CONFIG: SieveCardConfig[] = [
  { label: 'Metadata', backendKey: 'Cryptographic', subtitle: 'EXIF and creator integrity' },
  { label: 'Checksum', backendKey: 'Checksum', subtitle: 'GSTIN deterministic validation' },
  { label: 'Arithmetic', backendKey: 'Arithmetic', subtitle: 'Qty x Price + Tax consistency' },
  { label: 'Benford', backendKey: 'Statistical', subtitle: 'First-digit variance profile' },
  { label: 'Vision', backendKey: 'Spatial', subtitle: 'Pixel and font tamper scan' },
  { label: 'Registry', backendKey: 'OSINT', subtitle: 'Vendor and GSTIN corroboration' },
]

function findLog(forensicLog: ForensicLogEntry[], backendKey: string): ForensicLogEntry | null {
  return forensicLog.find((entry) => entry.sieve === backendKey) ?? null
}

export default function ResultGrid({ forensicLog }: ResultGridProps) {
  return (
    <section>
      <header className="mb-4 flex items-end justify-between">
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">6-Sieve Result Grid</h3>
        <span className="text-xs uppercase tracking-[0.2em] text-slate-400">2 x 3 Forensic Matrix</span>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {CARD_CONFIG.map((card) => {
          const log = findLog(forensicLog, card.backendKey)
          const presentation = deriveCardPresentation(forensicLog, card.backendKey, card.label)
          const isPass = presentation.state === 'PASS'
          const isWarning = presentation.state === 'WARNING'
          const isFail = presentation.state === 'FAIL'

          const cardClass = isPass
            ? 'border-emerald-500 bg-emerald-950/20'
            : isWarning
            ? 'border-amber-400 bg-amber-950/20'
            : isFail
            ? 'border-rose-500 bg-rose-950/20 animate-pulse'
            : 'border-slate-700 bg-slate-900/65'

          const badgeClass = isPass
            ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/50'
            : isWarning
            ? 'bg-amber-400/15 text-amber-300 border border-amber-400/50'
            : isFail
            ? 'bg-rose-500/15 text-rose-300 border border-rose-500/50'
            : 'bg-slate-500/15 text-slate-300 border border-slate-500/40'

          const title = isPass
            ? 'No Anomaly Detected.'
            : isWarning
            ? `REVIEW REQUIRED: ${presentation.reason}`
            : isFail
            ? `FRAUD DETECTED: ${presentation.reason}`
            : 'Awaiting analysis output.'

          return (
            <article key={card.label} className={`rounded-xl border p-4 transition ${cardClass}`}>
              <div className="mb-3 flex items-start justify-between gap-2">
                <div>
                  <h4 className="text-lg font-semibold text-emerald-300">{card.label}</h4>
                  <p className="text-xs text-slate-300">{card.subtitle}</p>
                </div>
                <span className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] ${badgeClass}`}>
                  {isPass ? 'PASS' : isWarning ? 'WARN' : isFail ? 'FAIL' : 'PENDING'}
                </span>
              </div>

              <p className={`text-sm leading-relaxed ${isFail ? 'text-rose-200' : isWarning ? 'text-amber-200' : 'text-emerald-200/90'}`}>
                {title}
              </p>

              {log && presentation.technicalDetail ? (
                <p className="mt-2 text-xs leading-relaxed text-slate-400">Evidence: {presentation.technicalDetail}</p>
              ) : null}
            </article>
          )
        })}
      </div>
    </section>
  )
}
```

### frontend/app/components/TrustScorePanel.tsx

```tsx
'use client'

import { TrustScoreSummary } from '../lib/forensics'

interface TrustScorePanelProps {
  summary: TrustScoreSummary | null
  analyzing: boolean
}

export default function TrustScorePanel({ summary, analyzing }: TrustScorePanelProps) {
  if (analyzing) {
    return (
      <section className="rounded-2xl border border-emerald-500/50 bg-slate-900/70 p-5">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-emerald-400">Trust Score</h3>
        <p className="mt-3 text-sm text-slate-300">Computing forensic confidence from six-sieve evidence...</p>
      </section>
    )
  }

  if (!summary) {
    return (
      <section className="rounded-2xl border border-slate-700 bg-slate-900/70 p-5">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-emerald-400">Trust Score</h3>
        <p className="mt-3 text-sm text-slate-300">Run analysis to generate a trust score and human-readable fraud reasons.</p>
      </section>
    )
  }

  const tone =
    summary.band === 'HIGH'
      ? 'text-emerald-300 border-emerald-500/60'
      : summary.band === 'MEDIUM'
      ? 'text-amber-300 border-amber-400/60'
      : summary.band === 'LOW'
      ? 'text-orange-300 border-orange-400/60'
      : 'text-rose-300 border-rose-500/70'

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/75 p-5">
      <div className="grid gap-5 lg:grid-cols-[270px_1fr]">
        <div className={`rounded-xl border bg-slate-950/70 p-5 ${tone}`}>
          <h3 className="text-xs uppercase tracking-[0.25em] text-slate-300">Trust Score</h3>
          <p className="mt-3 text-6xl font-black leading-none">{summary.score}</p>
          <p className="mt-2 text-sm font-semibold uppercase tracking-[0.22em]">{summary.band} TRUST</p>
        </div>

        <div className="space-y-4">
          <div className="rounded-lg border border-slate-700 bg-slate-950/60 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-emerald-300">Scoring Math</p>
            <p className="mt-2 text-sm text-slate-200">{summary.formula}</p>
            <p className="mt-1 text-xs text-slate-400">Risk factors: PASS=0, WARNING=0.45, FAIL/ANOMALY=1, ERROR=0.85</p>
          </div>

          <div className="rounded-lg border border-slate-700 bg-slate-950/60 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-rose-300">Why It Was Flagged</p>
            {summary.reasons.length === 0 ? (
              <p className="mt-2 text-sm text-emerald-300">All sieve checks passed with no fraud indicators.</p>
            ) : (
              <ul className="mt-2 space-y-2 text-sm text-slate-200">
                {summary.reasons.map((reason) => (
                  <li key={reason} className="rounded-md border border-rose-500/20 bg-rose-950/10 px-3 py-2">
                    {reason}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
```

### frontend/app/components/VerdictBanner.tsx

```tsx
'use client'

import { Verdict } from '../types'

interface VerdictBannerProps {
  verdict: Verdict | null
  analyzing: boolean
  errorMessage: string | null
}

export default function VerdictBanner({ verdict, analyzing, errorMessage }: VerdictBannerProps) {
  if (errorMessage) {
    return (
      <section className="rounded-2xl border-2 border-rose-500 bg-rose-950/40 px-6 py-8 shadow-[0_0_35px_rgba(244,63,94,0.25)]">
        <p className="text-xs uppercase tracking-[0.35em] text-rose-300">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-rose-400 md:text-5xl">PIPELINE ERROR</h2>
        <p className="mt-3 max-w-4xl text-sm text-rose-200 md:text-base">{errorMessage}</p>
      </section>
    )
  }

  if (analyzing) {
    return (
      <section className="relative overflow-hidden rounded-2xl border-2 border-emerald-500/70 bg-slate-900/80 px-6 py-8">
        <div className="absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-transparent via-emerald-400/25 to-transparent animate-scan" />
        <p className="text-xs uppercase tracking-[0.35em] text-emerald-300">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-emerald-400 md:text-5xl">ANALYSIS IN PROGRESS</h2>
        <p className="mt-3 text-sm text-emerald-200/85 md:text-base">Neural mesh is running deterministic and probabilistic forensics.</p>
      </section>
    )
  }

  if (!verdict) {
    return (
      <section className="rounded-2xl border-2 border-slate-700 bg-slate-900/70 px-6 py-8">
        <p className="text-xs uppercase tracking-[0.35em] text-slate-400">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-emerald-500/80 md:text-5xl">AWAITING EVIDENCE</h2>
        <p className="mt-3 text-sm text-slate-300/85 md:text-base">Upload an invoice to trigger the forensic command pipeline.</p>
      </section>
    )
  }

  const styleByVerdict: Record<Verdict, { border: string; title: string; tone: string }> = {
    VALIDATED: {
      border: 'border-emerald-500 bg-emerald-950/20 shadow-[0_0_35px_rgba(16,185,129,0.2)]',
      title: 'VALIDATED',
      tone: 'text-emerald-300',
    },
    SUSPICIOUS: {
      border: 'border-amber-400 bg-amber-950/20 shadow-[0_0_35px_rgba(251,191,36,0.2)]',
      title: 'SUSPICIOUS',
      tone: 'text-amber-300',
    },
    FRAUD_DETECTED: {
      border: 'border-rose-500 bg-rose-950/20 shadow-[0_0_40px_rgba(244,63,94,0.3)]',
      title: 'FRAUD DETECTED',
      tone: 'text-rose-400',
    },
  }

  const style = styleByVerdict[verdict]

  return (
    <section className={`rounded-2xl border-2 px-6 py-8 ${style.border}`}>
      <p className="text-xs uppercase tracking-[0.35em] text-slate-300">Final Verdict</p>
      <h2 className={`mt-2 text-4xl font-black tracking-wide md:text-6xl ${style.tone}`}>{style.title}</h2>
    </section>
  )
}
```

### frontend/app/globals.css

```
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  background: #020617;
}

.command-grid {
  background-image:
    linear-gradient(rgba(16, 185, 129, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(16, 185, 129, 0.06) 1px, transparent 1px);
  background-size: 26px 26px;
}

.neural-scroll::-webkit-scrollbar {
  width: 8px;
}

.neural-scroll::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.35);
  border-radius: 999px;
}

.neural-scroll::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.7);
}
```

### frontend/app/layout.tsx

```tsx
import './globals.css'
import { Share_Tech_Mono, Space_Grotesk } from 'next/font/google'

const headingFont = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-heading',
})

const monoFont = Share_Tech_Mono({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-mono',
})

export const metadata = {
  title: 'Aegis Guard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${headingFont.variable} ${monoFont.variable}`}>
      <body className="bg-slate-950 text-emerald-500 [font-family:var(--font-heading)]">{children}</body>
    </html>
  )
}
```

### frontend/app/lib/contracts.ts

```typescript
import { AnalyzeResponse, ApiErrorDetail, ApiErrorEnvelope, ForensicLogEntry, Verdict } from '../types'

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isVerdict(value: unknown): value is Verdict {
  return value === 'VALIDATED' || value === 'SUSPICIOUS' || value === 'FRAUD_DETECTED'
}

function isForensicLogEntry(value: unknown): value is ForensicLogEntry {
  if (!isRecord(value)) {
    return false
  }

  return (
    typeof value.sieve === 'string' &&
    typeof value.result === 'string' &&
    typeof value.details === 'string'
  )
}

export function isAnalyzeResponse(value: unknown): value is AnalyzeResponse {
  if (!isRecord(value)) {
    return false
  }

  if (value.status !== 'Completed' || !isVerdict(value.final_judgement)) {
    return false
  }

  if (!Array.isArray(value.forensic_log)) {
    return false
  }

  return value.forensic_log.every((entry) => isForensicLogEntry(entry))
}

function isApiErrorDetail(value: unknown): value is ApiErrorDetail {
  if (!isRecord(value)) {
    return false
  }

  return (
    typeof value.code === 'string' &&
    typeof value.message === 'string' &&
    typeof value.request_id === 'string'
  )
}

function isApiErrorEnvelope(value: unknown): value is ApiErrorEnvelope {
  if (!isRecord(value)) {
    return false
  }

  return isApiErrorDetail(value.detail)
}

export function extractErrorMessage(payload: unknown, statusCode: number): string {
  if (isApiErrorEnvelope(payload)) {
    const details = payload.detail.details ? ` (${payload.detail.details})` : ''
    return `${payload.detail.message}${details}`
  }

  if (typeof payload === 'string' && payload.trim()) {
    return payload
  }

  return `Backend request failed with status ${statusCode}.`
}
```

### frontend/app/lib/forensics.ts

```typescript
import { BackendSieveOutcome, ForensicLogEntry } from '../types'

export type SieveDisplayState = 'PENDING' | 'PASS' | 'WARNING' | 'FAIL'

interface SieveWeightConfig {
  key: string
  label: string
  weight: number
}

const SIEVE_WEIGHT_CONFIG: SieveWeightConfig[] = [
  { key: 'Cryptographic', label: 'Metadata', weight: 15 },
  { key: 'Checksum', label: 'Checksum', weight: 20 },
  { key: 'Arithmetic', label: 'Arithmetic', weight: 20 },
  { key: 'Statistical', label: 'Benford', weight: 10 },
  { key: 'Spatial', label: 'Vision', weight: 20 },
  { key: 'OSINT', label: 'Registry', weight: 15 },
]

const OUTCOME_RISK: Record<BackendSieveOutcome, number> = {
  PASS: 0,
  WARNING: 0.45,
  FAILED: 1,
  ANOMALY: 1,
  ERROR: 0.85,
}

export interface TrustBreakdownRow {
  key: string
  label: string
  weight: number
  risk: number
  penalty: number
  state: SieveDisplayState
  reason: string
  technicalDetail: string
}

export interface TrustScoreSummary {
  score: number
  band: 'HIGH' | 'MEDIUM' | 'LOW' | 'CRITICAL'
  totalPenalty: number
  formula: string
  reasons: string[]
  breakdown: TrustBreakdownRow[]
}

function normalizeWhitespace(value: string): string {
  return value.replace(/\s+/g, ' ').trim()
}

function shorten(value: string, maxLength = 220): string {
  if (value.length <= maxLength) {
    return value
  }
  return `${value.slice(0, maxLength - 1)}…`
}

export function getForensicEntry(forensicLog: ForensicLogEntry[], key: string): ForensicLogEntry | null {
  return forensicLog.find((entry) => entry.sieve === key) ?? null
}

export function toDisplayState(entry: ForensicLogEntry | null): SieveDisplayState {
  if (!entry) {
    return 'PENDING'
  }
  if (entry.result === 'PASS') {
    return 'PASS'
  }
  if (entry.result === 'WARNING') {
    return 'WARNING'
  }
  return 'FAIL'
}

export function humanizeReason(entry: ForensicLogEntry | null, label: string): string {
  if (!entry) {
    return 'Awaiting analysis output.'
  }

  const detail = normalizeWhitespace(entry.details)
  const detailLower = detail.toLowerCase()

  if (entry.result === 'PASS') {
    return 'No Anomaly Detected.'
  }

  if (entry.sieve === 'Cryptographic') {
    if (detailLower.includes('suspicious') || detailLower.includes('flagged')) {
      return 'Document metadata suggests the file may have been modified using external editing tools.'
    }
    return 'Metadata integrity could not be fully confirmed.'
  }

  if (entry.sieve === 'Checksum') {
    if (detailLower.includes('no gstin')) {
      return 'The invoice does not provide a valid GSTIN for deterministic verification.'
    }
    if (detailLower.includes('failed')) {
      return 'GSTIN checksum verification failed, indicating tax identity inconsistency.'
    }
    return 'Tax identity verification returned a non-pass result.'
  }

  if (entry.sieve === 'Arithmetic') {
    if (detailLower.includes('skipped')) {
      return 'Invoice math fields were incomplete, so arithmetic consistency could not be verified.'
    }
    if (detailLower.includes('mismatch') || detailLower.includes('failed')) {
      return 'Line totals, subtotal, tax, or grand total are mathematically inconsistent.'
    }
    return 'Arithmetic consistency check did not pass.'
  }

  if (entry.sieve === 'Statistical') {
    if (detailLower.includes('needs at least')) {
      return 'Not enough numeric evidence was found for a reliable Benford analysis.'
    }
    if (detailLower.includes('non-conforming') || detailLower.includes('failed')) {
      return 'Number patterns deviate from expected real-world invoice distributions.'
    }
    return 'Statistical consistency check did not pass.'
  }

  if (entry.sieve === 'Spatial') {
    if (detailLower.includes('failed') && detailLower.includes('model')) {
      return 'Vision verification service is currently unavailable; manual visual review is required.'
    }
    if (detailLower.includes('tamper') || detailLower.includes('anomal')) {
      return 'Visual analysis detected potential tampering artifacts.'
    }
    return 'Visual integrity check did not pass.'
  }

  if (entry.sieve === 'OSINT') {
    if (detailLower.includes('missing')) {
      return 'Vendor and GSTIN evidence was incomplete for registry corroboration.'
    }
    if (detailLower.includes('failed')) {
      return 'Vendor identity could not be corroborated against registry intelligence.'
    }
    return 'Registry corroboration check did not pass.'
  }

  return `${label} check requires manual review.`
}

export interface SieveCardPresentation {
  state: SieveDisplayState
  reason: string
  technicalDetail: string
}

export function deriveCardPresentation(
  forensicLog: ForensicLogEntry[],
  key: string,
  label: string
): SieveCardPresentation {
  const entry = getForensicEntry(forensicLog, key)
  return {
    state: toDisplayState(entry),
    reason: humanizeReason(entry, label),
    technicalDetail: entry ? shorten(normalizeWhitespace(entry.details), 240) : '',
  }
}

export function buildTrustScoreSummary(forensicLog: ForensicLogEntry[]): TrustScoreSummary {
  const breakdown = SIEVE_WEIGHT_CONFIG.map((config): TrustBreakdownRow => {
    const entry = getForensicEntry(forensicLog, config.key)
    const state = toDisplayState(entry)
    const risk = entry ? OUTCOME_RISK[entry.result] ?? 0.65 : 0
    const penalty = config.weight * risk

    return {
      key: config.key,
      label: config.label,
      weight: config.weight,
      risk,
      penalty,
      state,
      reason: humanizeReason(entry, config.label),
      technicalDetail: entry ? shorten(normalizeWhitespace(entry.details), 220) : '',
    }
  })

  const totalPenalty = breakdown.reduce((sum, item) => sum + item.penalty, 0)
  const score = Math.max(0, Math.round(100 - totalPenalty))

  const band: TrustScoreSummary['band'] =
    score >= 80 ? 'HIGH' : score >= 60 ? 'MEDIUM' : score >= 40 ? 'LOW' : 'CRITICAL'

  const reasons = breakdown
    .filter((item) => item.state === 'FAIL' || item.state === 'WARNING')
    .map((item) => `${item.label}: ${item.reason}`)

  return {
    score,
    band,
    totalPenalty,
    formula: `Trust Score = max(0, 100 - Σ(weight × risk)) = max(0, 100 - ${totalPenalty.toFixed(1)}) = ${score}`,
    reasons,
    breakdown,
  }
}
```

### frontend/app/page.tsx

```tsx
import CommandCenter from './components/CommandCenter'

export default function Page() {
  return <CommandCenter />
}
```

### frontend/app/types.ts

```typescript
export type Verdict = 'VALIDATED' | 'SUSPICIOUS' | 'FRAUD_DETECTED'

export type BackendSieveOutcome = 'PASS' | 'FAILED' | 'WARNING' | 'ANOMALY' | 'ERROR'

export interface ForensicLogEntry {
  sieve: string
  result: BackendSieveOutcome
  details: string
  correlation_id?: string
  duration_ms?: number
}

export interface AnalyzeResponse {
  status: 'Completed'
  final_judgement: Verdict
  forensic_log: ForensicLogEntry[]
}

export interface ApiErrorDetail {
  code: string
  message: string
  request_id: string
  details?: string
}

export interface ApiErrorEnvelope {
  detail: ApiErrorDetail
}
```

### frontend/next-env.d.ts

```typescript
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/building-your-application/configuring/typescript for more information.
```

### frontend/package-lock.json

```text
{
  "name": "aegis-guard-frontend",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "aegis-guard-frontend",
      "version": "0.1.0",
      "dependencies": {
        "next": "14",
        "react": "18",
        "react-dom": "18"
      },
      "devDependencies": {
        "@types/node": "^22.7.7",
        "@types/react": "^18.3.12",
        "autoprefixer": "^10.4.20",
        "postcss": "^8.4.47",
        "tailwindcss": "^3.4.17",
        "typescript": "^5.6.3"
      }
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@next/env": {
      "version": "14.2.35",
      "resolved": "https://registry.npmjs.org/@next/env/-/env-14.2.35.tgz",
      "integrity": "sha512-DuhvCtj4t9Gwrx80dmz2F4t/zKQ4ktN8WrMwOuVzkJfBilwAwGr6v16M5eI8yCuZ63H9TTuEU09Iu2HqkzFPVQ==",
      "license": "MIT"
    },
    "node_modules/@next/swc-darwin-arm64": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-darwin-arm64/-/swc-darwin-arm64-14.2.33.tgz",
      "integrity": "sha512-HqYnb6pxlsshoSTubdXKu15g3iivcbsMXg4bYpjL2iS/V6aQot+iyF4BUc2qA/J/n55YtvE4PHMKWBKGCF/+wA==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-darwin-x64": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-darwin-x64/-/swc-darwin-x64-14.2.33.tgz",
      "integrity": "sha512-8HGBeAE5rX3jzKvF593XTTFg3gxeU4f+UWnswa6JPhzaR6+zblO5+fjltJWIZc4aUalqTclvN2QtTC37LxvZAA==",
      "cpu": [
        "x64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-arm64-gnu": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-arm64-gnu/-/swc-linux-arm64-gnu-14.2.33.tgz",
      "integrity": "sha512-JXMBka6lNNmqbkvcTtaX8Gu5by9547bukHQvPoLe9VRBx1gHwzf5tdt4AaezW85HAB3pikcvyqBToRTDA4DeLw==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-arm64-musl": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-arm64-musl/-/swc-linux-arm64-musl-14.2.33.tgz",
      "integrity": "sha512-Bm+QulsAItD/x6Ih8wGIMfRJy4G73tu1HJsrccPW6AfqdZd0Sfm5Imhgkgq2+kly065rYMnCOxTBvmvFY1BKfg==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-x64-gnu": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-x64-gnu/-/swc-linux-x64-gnu-14.2.33.tgz",
      "integrity": "sha512-FnFn+ZBgsVMbGDsTqo8zsnRzydvsGV8vfiWwUo1LD8FTmPTdV+otGSWKc4LJec0oSexFnCYVO4hX8P8qQKaSlg==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-x64-musl": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-x64-musl/-/swc-linux-x64-musl-14.2.33.tgz",
      "integrity": "sha512-345tsIWMzoXaQndUTDv1qypDRiebFxGYx9pYkhwY4hBRaOLt8UGfiWKr9FSSHs25dFIf8ZqIFaPdy5MljdoawA==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-win32-arm64-msvc": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-win32-arm64-msvc/-/swc-win32-arm64-msvc-14.2.33.tgz",
      "integrity": "sha512-nscpt0G6UCTkrT2ppnJnFsYbPDQwmum4GNXYTeoTIdsmMydSKFz9Iny2jpaRupTb+Wl298+Rh82WKzt9LCcqSQ==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-win32-ia32-msvc": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-win32-ia32-msvc/-/swc-win32-ia32-msvc-14.2.33.tgz",
      "integrity": "sha512-pc9LpGNKhJ0dXQhZ5QMmYxtARwwmWLpeocFmVG5Z0DzWq5Uf0izcI8tLc+qOpqxO1PWqZ5A7J1blrUIKrIFc7Q==",
      "cpu": [
        "ia32"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-win32-x64-msvc": {
      "version": "14.2.33",
      "resolved": "https://registry.npmjs.org/@next/swc-win32-x64-msvc/-/swc-win32-x64-msvc-14.2.33.tgz",
      "integrity": "sha512-nOjfZMy8B94MdisuzZo9/57xuFVLHJaDj5e/xrduJp9CV2/HrfxTRH2fbyLe+K9QT41WBLUd4iXX3R7jBp0EUg==",
      "cpu": [
        "x64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@swc/counter": {
      "version": "0.1.3",
      "resolved": "https://registry.npmjs.org/@swc/counter/-/counter-0.1.3.tgz",
      "integrity": "sha512-e2BR4lsJkkRlKZ/qCHPw9ZaSxc0MVUd7gtbtaB7aMvHeJVYe8sOB8DBZkP2DtISHGSku9sCK6T6cnY0CtXrOCQ==",
      "license": "Apache-2.0"
    },
    "node_modules/@swc/helpers": {
      "version": "0.5.5",
      "resolved": "https://registry.npmjs.org/@swc/helpers/-/helpers-0.5.5.tgz",
      "integrity": "sha512-KGYxvIOXcceOAbEk4bi/dVLEK9z8sZ0uBB3Il5b1rhfClSpcX0yfRO0KmTkqR2cnQDymwLB+25ZyMzICg/cm/A==",
      "license": "Apache-2.0",
      "dependencies": {
        "@swc/counter": "^0.1.3",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@types/node": {
      "version": "22.19.17",
      "resolved": "https://registry.npmjs.org/@types/node/-/node-22.19.17.tgz",
      "integrity": "sha512-wGdMcf+vPYM6jikpS/qhg6WiqSV/OhG+jeeHT/KlVqxYfD40iYJf9/AE1uQxVWFvU7MipKRkRv8NSHiCGgPr8Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "undici-types": "~6.21.0"
      }
    },
    "node_modules/@types/prop-types": {
      "version": "15.7.15",
      "resolved": "https://registry.npmjs.org/@types/prop-types/-/prop-types-15.7.15.tgz",
      "integrity": "sha512-F6bEyamV9jKGAFBEmlQnesRPGOQqS2+Uwi0Em15xenOxHaf2hv6L8YCVn3rPdPJOiJfPiCnLIRyvwVaqMY3MIw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/react": {
      "version": "18.3.28",
      "resolved": "https://registry.npmjs.org/@types/react/-/react-18.3.28.tgz",
      "integrity": "sha512-z9VXpC7MWrhfWipitjNdgCauoMLRdIILQsAEV+ZesIzBq/oUlxk0m3ApZuMFCXdnS4U7KrI+l3WRUEGQ8K1QKw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/prop-types": "*",
        "csstype": "^3.2.2"
      }
    },
    "node_modules/any-promise": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/any-promise/-/any-promise-1.3.0.tgz",
      "integrity": "sha512-7UvmKalWRt1wgjL1RrGxoSJW/0QZFIegpeGvZG9kjp8vrRu55XTHbwnqq2GpXm9uLbcuhxm3IqX9OB4MZR1b2A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/anymatch": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/anymatch/-/anymatch-3.1.3.tgz",
      "integrity": "sha512-KMReFUr0B4t+D+OBkjR3KYqvocp2XaSzO55UcB6mgQMd3KbcE+mWTyvVV7D/zsdEbNnV6acZUutkiHQXvTr1Rw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "normalize-path": "^3.0.0",
        "picomatch": "^2.0.4"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/arg": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/arg/-/arg-5.0.2.tgz",
      "integrity": "sha512-PYjyFOLKQ9y57JvQ6QLo8dAgNqswh8M1RMJYdQduT6xbWSgK36P/Z/v+p888pM69jMMfS8Xd8F6I1kQ/I9HUGg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/autoprefixer": {
      "version": "10.5.0",
      "resolved": "https://registry.npmjs.org/autoprefixer/-/autoprefixer-10.5.0.tgz",
      "integrity": "sha512-FMhOoZV4+qR6aTUALKX2rEqGG+oyATvwBt9IIzVR5rMa2HRWPkxf+P+PAJLD1I/H5/II+HuZcBJYEFBpq39ong==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/autoprefixer"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.28.2",
        "caniuse-lite": "^1.0.30001787",
        "fraction.js": "^5.3.4",
        "picocolors": "^1.1.1",
        "postcss-value-parser": "^4.2.0"
      },
      "bin": {
        "autoprefixer": "bin/autoprefixer"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.10.20",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.10.20.tgz",
      "integrity": "sha512-1AaXxEPfXT+GvTBJFuy4yXVHWJBXa4OdbIebGN/wX5DlsIkU0+wzGnd2lOzokSk51d5LUmqjgBLRLlypLUqInQ==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.cjs"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/binary-extensions": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-2.3.0.tgz",
      "integrity": "sha512-Ceh+7ox5qe7LJuLHoY0feh3pHuUDHAcRUeyL2VYghZwfpkNIy/+8Ocg0a3UuSoYzavmylwuLWQOf3hl0jjMMIw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/browserslist": {
      "version": "4.28.2",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.28.2.tgz",
      "integrity": "sha512-48xSriZYYg+8qXna9kwqjIVzuQxi+KYWp2+5nCYnYKPTr0LvD89Jqk2Or5ogxz0NUMfIjhh2lIUX/LyX9B4oIg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "baseline-browser-mapping": "^2.10.12",
        "caniuse-lite": "^1.0.30001782",
        "electron-to-chromium": "^1.5.328",
        "node-releases": "^2.0.36",
        "update-browserslist-db": "^1.2.3"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/busboy": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/busboy/-/busboy-1.6.0.tgz",
      "integrity": "sha512-8SFQbg/0hQ9xy3UNTB0YEnsNBbWfhf7RtnzpL7TkBiTBRfrQ9Fxcnz7VJsleJpyp6rVLvXiuORqjlHi5q+PYuA==",
      "dependencies": {
        "streamsearch": "^1.1.0"
      },
      "engines": {
        "node": ">=10.16.0"
      }
    },
    "node_modules/camelcase-css": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/camelcase-css/-/camelcase-css-2.0.1.tgz",
      "integrity": "sha512-QOSvevhslijgYwRx6Rv7zKdMF8lbRmx+uQGx2+vDc+KI/eBnsy9kit5aj23AgGu3pa4t9AgwbnXWqS+iOY+2aA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001788",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001788.tgz",
      "integrity": "sha512-6q8HFp+lOQtcf7wBK+uEenxymVWkGKkjFpCvw5W25cmMwEDU45p1xQFBQv8JDlMMry7eNxyBaR+qxgmTUZkIRQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/chokidar": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-3.6.0.tgz",
      "integrity": "sha512-7VT13fmjotKpGipCW9JEQAusEPE+Ei8nl6/g4FBAmIm0GOOLMua9NDDo/DWp0ZAxCr3cPq5ZpBqmPAQgDda2Pw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "anymatch": "~3.1.2",
        "braces": "~3.0.2",
        "glob-parent": "~5.1.2",
        "is-binary-path": "~2.1.0",
        "is-glob": "~4.0.1",
        "normalize-path": "~3.0.0",
        "readdirp": "~3.6.0"
      },
      "engines": {
        "node": ">= 8.10.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/chokidar/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/client-only": {
      "version": "0.0.1",
      "resolved": "https://registry.npmjs.org/client-only/-/client-only-0.0.1.tgz",
      "integrity": "sha512-IV3Ou0jSMzZrd3pZ48nLkT9DA7Ag1pnPzaiQhpW7c3RbcqqzvzzVu+L8gfqMp/8IM2MQtSiqaCxrrcfu8I8rMA==",
      "license": "MIT"
    },
    "node_modules/commander": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/commander/-/commander-4.1.1.tgz",
      "integrity": "sha512-NOKm8xhkzAjzFx8B2v5OAHT+u5pRQc2UCa2Vq9jYL/31o2wi9mxBA7LIFs3sV5VSC49z6pEhfbMULvShKj26WA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/cssesc": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/cssesc/-/cssesc-3.0.0.tgz",
      "integrity": "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "cssesc": "bin/cssesc"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/csstype": {
      "version": "3.2.3",
      "resolved": "https://registry.npmjs.org/csstype/-/csstype-3.2.3.tgz",
      "integrity": "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/didyoumean": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/didyoumean/-/didyoumean-1.2.2.tgz",
      "integrity": "sha512-gxtyfqMg7GKyhQmb056K7M3xszy/myH8w+B4RT+QXBQsvAOdc3XymqDDPHx1BgPgsdAA5SIifona89YtRATDzw==",
      "dev": true,
      "license": "Apache-2.0"
    },
    "node_modules/dlv": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/dlv/-/dlv-1.1.3.tgz",
      "integrity": "sha512-+HlytyjlPKnIG8XuRG8WvmBP8xs8P71y+SKKS6ZXWoEgLuePxtDoUEiH7WkdePWrQ5JBpE6aoVqfZfJUQkjXwA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.340",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.340.tgz",
      "integrity": "sha512-908qahOGocRMinT2nM3ajCEM99H4iPdv84eagPP3FfZy/1ZGeOy2CZYzjhms81ckOPCXPlW7LkY4XpxD8r1DrA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/fast-glob": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.3.tgz",
      "integrity": "sha512-7MptL8U0cqcFdzIzwOTHoilX9x5BrNqye7Z/LuC7kCMRio1EMSyqRK3BEAUD7sXRq4iT4AzTVuZdhgQ2TCvYLg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.8"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/fast-glob/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fastq": {
      "version": "1.20.1",
      "resolved": "https://registry.npmjs.org/fastq/-/fastq-1.20.1.tgz",
      "integrity": "sha512-GGToxJ/w1x32s/D2EKND7kTil4n8OVk/9mycTc4VDza13lOvpUZTGX3mFSCtV9ksdGBVzvsyAVLM6mHFThxXxw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "reusify": "^1.0.4"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/fraction.js": {
      "version": "5.3.4",
      "resolved": "https://registry.npmjs.org/fraction.js/-/fraction.js-5.3.4.tgz",
      "integrity": "sha512-1X1NTtiJphryn/uLQz3whtY6jK3fTqoE3ohKs0tT+Ujr1W59oopxmoEh7Lu5p6vBaPbgoM0bzveAW4Qi5RyWDQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "*"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/rawify"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/glob-parent": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-6.0.2.tgz",
      "integrity": "sha512-XxwI8EOhVQgWp6iDL+3b0r86f4d6AX6zSU55HfB4ydCEuXLXc5FcYeOu+nnGftS4TEju/11rt4KJPTMgbfmv4A==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/graceful-fs": {
      "version": "4.2.11",
      "resolved": "https://registry.npmjs.org/graceful-fs/-/graceful-fs-4.2.11.tgz",
      "integrity": "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ==",
      "license": "ISC"
    },
    "node_modules/hasown": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.3.tgz",
      "integrity": "sha512-ej4AhfhfL2Q2zpMmLo7U1Uv9+PyhIZpgQLGT1F9miIGmiCJIoCgSmczFdrc97mWT4kVY72KA+WnnhJ5pghSvSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/is-binary-path": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-2.1.0.tgz",
      "integrity": "sha512-ZMERYes6pDydyuGidse7OsHxtbI7WVeUEozgR/g7rd0xUimYNlvZRE/K2MgZTjWy725IfelLeVcEM97mmtRGXw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "binary-extensions": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-core-module": {
      "version": "2.16.1",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.1.tgz",
      "integrity": "sha512-UfoeMA6fIJ8wTYFEUjelnaGI67v6+N7qXJEvQuIGa99l4xsCruSYOVSQ0uPANn4dAzm8lkYPaKLrrijLq7x23w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/jiti": {
      "version": "1.21.7",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-1.21.7.tgz",
      "integrity": "sha512-/imKNG4EbWNrVjoNC/1H5/9GFy+tqjGBHCaSsN+P2RnPqjsLmv6UD3Ej+Kj8nBWaRAwyk7kK5ZUc+OEatnTR3A==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "jiti": "bin/jiti.js"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/merge2": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/merge2/-/merge2-1.4.1.tgz",
      "integrity": "sha512-8q7VEgMJW4J8tcfVPy8g09NcQwZdbwFEqhe/WZkoIzjn/3TGDwtOCYtXGxA3O8tPzpczCCDgv+P2P5y00ZJOOg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/micromatch": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/micromatch/-/micromatch-4.0.8.tgz",
      "integrity": "sha512-PXwfBhYu0hBCPw8Dn0E+WDYb7af3dSLVWKi3HGv84IdF4TyFoC0ysxFd0Goxw7nSv4T/PzEJQxsYsEiFCKo2BA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "braces": "^3.0.3",
        "picomatch": "^2.3.1"
      },
      "engines": {
        "node": ">=8.6"
      }
    },
    "node_modules/mz": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/mz/-/mz-2.7.0.tgz",
      "integrity": "sha512-z81GNO7nnYMEhrGh9LeymoE4+Yr0Wn5McHIZMK5cfQCl+NDX08sCZgUc9/6MHni9IWuFLm1Z3HTCXu2z9fN62Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0",
        "object-assign": "^4.0.1",
        "thenify-all": "^1.0.0"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.11",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.11.tgz",
      "integrity": "sha512-N8SpfPUnUp1bK+PMYW8qSWdl9U+wwNWI4QKxOYDy9JAro3WMX7p2OeVRF9v+347pnakNevPmiHhNmZ2HbFA76w==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/next": {
      "version": "14.2.35",
      "resolved": "https://registry.npmjs.org/next/-/next-14.2.35.tgz",
      "integrity": "sha512-KhYd2Hjt/O1/1aZVX3dCwGXM1QmOV4eNM2UTacK5gipDdPN/oHHK/4oVGy7X8GMfPMsUTUEmGlsy0EY1YGAkig==",
      "license": "MIT",
      "dependencies": {
        "@next/env": "14.2.35",
        "@swc/helpers": "0.5.5",
        "busboy": "1.6.0",
        "caniuse-lite": "^1.0.30001579",
        "graceful-fs": "^4.2.11",
        "postcss": "8.4.31",
        "styled-jsx": "5.1.1"
      },
      "bin": {
        "next": "dist/bin/next"
      },
      "engines": {
        "node": ">=18.17.0"
      },
      "optionalDependencies": {
        "@next/swc-darwin-arm64": "14.2.33",
        "@next/swc-darwin-x64": "14.2.33",
        "@next/swc-linux-arm64-gnu": "14.2.33",
        "@next/swc-linux-arm64-musl": "14.2.33",
        "@next/swc-linux-x64-gnu": "14.2.33",
        "@next/swc-linux-x64-musl": "14.2.33",
        "@next/swc-win32-arm64-msvc": "14.2.33",
        "@next/swc-win32-ia32-msvc": "14.2.33",
        "@next/swc-win32-x64-msvc": "14.2.33"
      },
      "peerDependencies": {
        "@opentelemetry/api": "^1.1.0",
        "@playwright/test": "^1.41.2",
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "sass": "^1.3.0"
      },
      "peerDependenciesMeta": {
        "@opentelemetry/api": {
          "optional": true
        },
        "@playwright/test": {
          "optional": true
        },
        "sass": {
          "optional": true
        }
      }
    },
    "node_modules/next/node_modules/postcss": {
      "version": "8.4.31",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.4.31.tgz",
      "integrity": "sha512-PS08Iboia9mts/2ygV3eLpY5ghnUcfLV/EXTOW1E2qYxJKGGBUtNjN76FYHnMs36RmARn41bC0AZmn+rR0OVpQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.6",
        "picocolors": "^1.0.0",
        "source-map-js": "^1.0.2"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/node-releases": {
      "version": "2.0.37",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.37.tgz",
      "integrity": "sha512-1h5gKZCF+pO/o3Iqt5Jp7wc9rH3eJJ0+nh/CIoiRwjRxde/hAHyLPXYN4V3CqKAbiZPSeJFSWHmJsbkicta0Eg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/normalize-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/normalize-path/-/normalize-path-3.0.0.tgz",
      "integrity": "sha512-6eZs5Ls3WtCisHWp9S2GUy8dqkpGi4BVSz3GaqiE6ezub0512ESztXUwUB6C6IKbQkY2Pnb/mD4WYojCRwcwLA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-hash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/object-hash/-/object-hash-3.0.0.tgz",
      "integrity": "sha512-RSn9F68PjH9HqtltsSnqYC1XXoWe9Bju5+213R98cNGttag9q9yAOTzdbsqvIa7aNm5WffBZFpWYr2aWrklWAw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "2.3.2",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.2.tgz",
      "integrity": "sha512-V7+vQEJ06Z+c5tSye8S+nHUfI51xoXIXjHQ99cQtKUkQqqO1kO/KCJUfZXuB47h/YBlDhah2H3hdUGXn8ie0oA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/pify": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/pify/-/pify-2.3.0.tgz",
      "integrity": "sha512-udgsAY+fTnvv7kI7aaxbqwWNb0AHiB0qBO89PZKPkoTmGOgdbrHDKD+0B2X4uTfJ/FT1R09r9gTsjUjNJotuog==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/pirates": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/pirates/-/pirates-4.0.7.tgz",
      "integrity": "sha512-TfySrs/5nm8fQJDcBDuUng3VOUKsd7S+zqvbOTiGXHfxX4wK31ard+hoNuvkicM/2YFzlpDgABOevKSsB4G/FA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.10",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.10.tgz",
      "integrity": "sha512-pMMHxBOZKFU6HgAZ4eyGnwXF/EvPGGqUr0MnZ5+99485wwW41kW91A4LOGxSHhgugZmSChL5AlElNdwlNgcnLQ==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.11",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/postcss-import": {
      "version": "15.1.0",
      "resolved": "https://registry.npmjs.org/postcss-import/-/postcss-import-15.1.0.tgz",
      "integrity": "sha512-hpr+J05B2FVYUAXHeK1YyI267J/dDDhMU6B6civm8hSY1jYJnBXxzKDKDswzJmtLHryrjhnDjqqp/49t8FALew==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.0.0",
        "read-cache": "^1.0.0",
        "resolve": "^1.1.7"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-js": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-js/-/postcss-js-4.1.0.tgz",
      "integrity": "sha512-oIAOTqgIo7q2EOwbhb8UalYePMvYoIeRY2YKntdpFQXNosSu3vLrniGgmH9OKs/qAkfoj5oB3le/7mINW1LCfw==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "camelcase-css": "^2.0.1"
      },
      "engines": {
        "node": "^12 || ^14 || >= 16"
      },
      "peerDependencies": {
        "postcss": "^8.4.21"
      }
    },
    "node_modules/postcss-load-config": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/postcss-load-config/-/postcss-load-config-6.0.1.tgz",
      "integrity": "sha512-oPtTM4oerL+UXmx+93ytZVN82RrlY/wPUV8IeDxFrzIjXOLF1pN+EmKPLbubvKHT2HC20xXsCAH2Z+CKV6Oz/g==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "lilconfig": "^3.1.1"
      },
      "engines": {
        "node": ">= 18"
      },
      "peerDependencies": {
        "jiti": ">=1.21.0",
        "postcss": ">=8.0.9",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        },
        "postcss": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    },
    "node_modules/postcss-nested": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nested/-/postcss-nested-6.2.0.tgz",
      "integrity": "sha512-HQbt28KulC5AJzG+cZtj9kvKB93CFCdLvog1WFLf1D+xmMvPGlBstkpTEZfK5+AN9hfJocyBFCNiqyS48bpgzQ==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.1.1"
      },
      "engines": {
        "node": ">=12.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.14"
      }
    },
    "node_modules/postcss-selector-parser": {
      "version": "6.1.2",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-6.1.2.tgz",
      "integrity": "sha512-Q8qQfPiZ+THO/3ZrOrO0cJJKfpYCagtMUkXbnEfmgUjwXg6z/WBeOyS9APBBPCTSiDV+s4SwQGu8yFsiMRIudg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-value-parser": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-value-parser/-/postcss-value-parser-4.2.0.tgz",
      "integrity": "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/queue-microtask": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/queue-microtask/-/queue-microtask-1.2.3.tgz",
      "integrity": "sha512-NuaNSa6flKT5JaSYQzJok04JzTL1CA6aGhv5rfLW3PgqA+M2ChpZQnAC8h8i4ZFkBS8X5RqkDBHA7r4hej3K9A==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/react": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react/-/react-18.3.1.tgz",
      "integrity": "sha512-wS+hAgJShR0KhEvPJArfuPVN1+Hz1t0Y6n5jLrGQbkb4urgPE/0Rve+1kMB1v/oWgHgm4WIcV+i7F2pTVj+2iQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-dom": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz",
      "integrity": "sha512-5m4nQKp+rZRb09LNH59GM4BxTh9251/ylbKIbpe7TpGxfJ+9kv6BLkLBXIjjspbgbnIBNqlI23tRnTWT0snUIw==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0",
        "scheduler": "^0.23.2"
      },
      "peerDependencies": {
        "react": "^18.3.1"
      }
    },
    "node_modules/read-cache": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/read-cache/-/read-cache-1.0.0.tgz",
      "integrity": "sha512-Owdv/Ft7IjOgm/i0xvNDZ1LrRANRfew4b2prF3OWMQLxLfu3bS8FVhCsrSCMK4lR56Y9ya+AThoTpDCTxCmpRA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "pify": "^2.3.0"
      }
    },
    "node_modules/readdirp": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-3.6.0.tgz",
      "integrity": "sha512-hOS089on8RduqdbhvQ5Z37A0ESjsqz6qnRcffsMU3495FuTdqSm+7bhJ29JvIOsBDEEnan5DPu9t3To9VRlMzA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "picomatch": "^2.2.1"
      },
      "engines": {
        "node": ">=8.10.0"
      }
    },
    "node_modules/resolve": {
      "version": "1.22.12",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.12.tgz",
      "integrity": "sha512-TyeJ1zif53BPfHootBGwPRYT1RUt6oGWsaQr8UyZW/eAm9bKoijtvruSDEmZHm92CwS9nj7/fWttqPCgzep8CA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/reusify": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/reusify/-/reusify-1.1.0.tgz",
      "integrity": "sha512-g6QUff04oZpHs0eG5p83rFLhHeV00ug/Yf9nZM6fLeUrPguBTkTQOdpAWWspMh55TZfVQDPaN3NQJfbVRAxdIw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "iojs": ">=1.0.0",
        "node": ">=0.10.0"
      }
    },
    "node_modules/run-parallel": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/run-parallel/-/run-parallel-1.2.0.tgz",
      "integrity": "sha512-5l4VyZR86LZ/lDxZTR6jqL8AFE2S0IFLMP26AbjsLVADxHdhB/c0GUsH+y39UfCi3dzz8OlQuPmnaJOMoDHQBA==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "queue-microtask": "^1.2.2"
      }
    },
    "node_modules/scheduler": {
      "version": "0.23.2",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.23.2.tgz",
      "integrity": "sha512-UOShsPwz7NrMUqhR6t0hWjFduvOzbtv7toDH1/hIrfRNIDBnnBWd0CwJTGvTpngVlmwGCdP9/Zl/tVrDqcuYzQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/streamsearch": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/streamsearch/-/streamsearch-1.1.0.tgz",
      "integrity": "sha512-Mcc5wHehp9aXz1ax6bZUyY5afg9u2rv5cqQI3mRrYkGC8rW2hM02jWuwjtL++LS5qinSyhj2QfLyNsuc+VsExg==",
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/styled-jsx": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/styled-jsx/-/styled-jsx-5.1.1.tgz",
      "integrity": "sha512-pW7uC1l4mBZ8ugbiZrcIsiIvVx1UmTfw7UkC3Um2tmfUq9Bhk8IiyEIPl6F8agHgjzku6j0xQEZbfA5uSgSaCw==",
      "license": "MIT",
      "dependencies": {
        "client-only": "0.0.1"
      },
      "engines": {
        "node": ">= 12.0.0"
      },
      "peerDependencies": {
        "react": ">= 16.8.0 || 17.x.x || ^18.0.0-0"
      },
      "peerDependenciesMeta": {
        "@babel/core": {
          "optional": true
        },
        "babel-plugin-macros": {
          "optional": true
        }
      }
    },
    "node_modules/sucrase": {
      "version": "3.35.1",
      "resolved": "https://registry.npmjs.org/sucrase/-/sucrase-3.35.1.tgz",
      "integrity": "sha512-DhuTmvZWux4H1UOnWMB3sk0sbaCVOoQZjv8u1rDoTV0HTdGem9hkAZtl4JZy8P2z4Bg0nT+YMeOFyVr4zcG5Tw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.2",
        "commander": "^4.0.0",
        "lines-and-columns": "^1.1.6",
        "mz": "^2.7.0",
        "pirates": "^4.0.1",
        "tinyglobby": "^0.2.11",
        "ts-interface-checker": "^0.1.9"
      },
      "bin": {
        "sucrase": "bin/sucrase",
        "sucrase-node": "bin/sucrase-node"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/tailwindcss": {
      "version": "3.4.19",
      "resolved": "https://registry.npmjs.org/tailwindcss/-/tailwindcss-3.4.19.tgz",
      "integrity": "sha512-3ofp+LL8E+pK/JuPLPggVAIaEuhvIz4qNcf3nA1Xn2o/7fb7s/TYpHhwGDv1ZU3PkBluUVaF8PyCHcm48cKLWQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@alloc/quick-lru": "^5.2.0",
        "arg": "^5.0.2",
        "chokidar": "^3.6.0",
        "didyoumean": "^1.2.2",
        "dlv": "^1.1.3",
        "fast-glob": "^3.3.2",
        "glob-parent": "^6.0.2",
        "is-glob": "^4.0.3",
        "jiti": "^1.21.7",
        "lilconfig": "^3.1.3",
        "micromatch": "^4.0.8",
        "normalize-path": "^3.0.0",
        "object-hash": "^3.0.0",
        "picocolors": "^1.1.1",
        "postcss": "^8.4.47",
        "postcss-import": "^15.1.0",
        "postcss-js": "^4.0.1",
        "postcss-load-config": "^4.0.2 || ^5.0 || ^6.0",
        "postcss-nested": "^6.2.0",
        "postcss-selector-parser": "^6.1.2",
        "resolve": "^1.22.8",
        "sucrase": "^3.35.0"
      },
      "bin": {
        "tailwind": "lib/cli.js",
        "tailwindcss": "lib/cli.js"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/thenify": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/thenify/-/thenify-3.3.1.tgz",
      "integrity": "sha512-RVZSIV5IG10Hk3enotrhvz0T9em6cyHBLkH/YAZuKqd8hRkKhSfCGIcP2KUY0EPxndzANBmNllzWPwak+bheSw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0"
      }
    },
    "node_modules/thenify-all": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/thenify-all/-/thenify-all-1.6.0.tgz",
      "integrity": "sha512-RNxQH/qI8/t3thXJDwcstUO4zeqo64+Uy/+sNVRBx4Xn2OX+OZ9oP+iJnNFqplFra2ZUVeKCSa2oVWi3T4uVmA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "thenify": ">= 3.1.0 < 4"
      },
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/tinyglobby": {
      "version": "0.2.16",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.16.tgz",
      "integrity": "sha512-pn99VhoACYR8nFHhxqix+uvsbXineAasWm5ojXoN8xEwK5Kd3/TrhNn1wByuD52UxWRLy8pu+kRMniEi6Eq9Zg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tinyglobby/node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/tinyglobby/node_modules/picomatch": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.4.tgz",
      "integrity": "sha512-QP88BAKvMam/3NxH6vj2o21R6MjxZUAd6nlwAS/pnGvN9IVLocLHxGYIzFhg6fUQ+5th6P4dv4eW9jX3DSIj7A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/ts-interface-checker": {
      "version": "0.1.13",
      "resolved": "https://registry.npmjs.org/ts-interface-checker/-/ts-interface-checker-0.1.13.tgz",
      "integrity": "sha512-Y/arvbn+rrz3JCKl9C4kVNfTfSm2/mEp5FSz5EsZSANGPSlQrpRI5M4PKF+mJnE52jOO90PnPSc3Ur3bTQw0gA==",
      "dev": true,
      "license": "Apache-2.0"
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "license": "0BSD"
    },
    "node_modules/typescript": {
      "version": "5.9.3",
      "resolved": "https://registry.npmjs.org/typescript/-/typescript-5.9.3.tgz",
      "integrity": "sha512-jl1vZzPDinLr9eUt3J/t7V6FgNEw9QjvBPdysz9KfQDD41fQrC2Y4vKQdiaUpFT4bXlb1RHhLpp8wtm6M5TgSw==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "tsc": "bin/tsc",
        "tsserver": "bin/tsserver"
      },
      "engines": {
        "node": ">=14.17"
      }
    },
    "node_modules/undici-types": {
      "version": "6.21.0",
      "resolved": "https://registry.npmjs.org/undici-types/-/undici-types-6.21.0.tgz",
      "integrity": "sha512-iwDZqg0QAGrg9Rav5H4n0M64c3mkR59cJ6wQp+7C4nI0gsmExaedaYLNO44eT4AtBBwjbTiGPMlt2Md0T9H9JQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/update-browserslist-db": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.2.3.tgz",
      "integrity": "sha512-Js0m9cx+qOgDxo0eMiFGEueWztz+d4+M3rGlmKPT+T4IS/jP4ylw3Nwpu6cpTTP8R1MAC1kF4VbdLt3ARf209w==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/util-deprecate": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz",
      "integrity": "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw==",
      "dev": true,
      "license": "MIT"
    }
  }
}
```

### frontend/package.json

```json
{
  "name": "aegis-guard-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14",
    "react": "18",
    "react-dom": "18"
  },
  "devDependencies": {
    "@types/node": "^22.7.7",
    "@types/react": "^18.3.12",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.17",
    "typescript": "^5.6.3"
  }
}
```

### frontend/postcss.config.js

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### frontend/tailwind.config.ts

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      keyframes: {
        scan: {
          '0%': { transform: 'translateX(-120%)' },
          '100%': { transform: 'translateX(120%)' },
        },
      },
      animation: {
        scan: 'scan 2.4s linear infinite',
      },
    },
  },
  plugins: [],
}

export default config
```

### frontend/tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

