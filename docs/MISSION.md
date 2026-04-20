# MISSION BRIEF: AEGIS-GUARD (RIH 2026)

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

- **Extraction workloads (Sieve 2 and Sieve 3 support):** Claude/GPT class models via FastRouter with fallback sequencing.
- **Vision workloads (Sieve 4):** multimodal models via FastRouter with fallback sequencing.
- **Secrets policy:** use environment variables only; no hardcoded keys in code or docs.

## 5. The 4-Sieve Architecture
Our pipeline contains four independent, auditable sieves:

1. **Sieve 1 - Cryptographic / Metadata**
   - Reads PDF metadata via PyPDF2.
   - Flags suspicious producer/creator signatures (for example, editing-tool traces).

2. **Sieve 2 - Checksum**
   - Extracts GSTIN candidates from document text (regex plus model-assisted fallback).
   - Applies deterministic GSTIN checksum validation.

3. **Sieve 3 - Statistical (Benford)**
   - Extracts line-item-like numeric values from document text.
   - Computes Benford conformity using MAD thresholding.

4. **Sieve 4 - Spatial / Vision**
   - Renders PDF page imagery and performs visual tamper analysis via multimodal model.
   - Detects signals such as local compression artifacts, alignment issues, and layout inconsistencies.

## 6. Orchestration and Verdict Logic
LangGraph executes the sieve flow in sequence and produces a final judgement:

- `FRAUD_DETECTED` when severe anomalies/failures are multiple.
- `SUSPICIOUS` when limited severe findings or runtime degradation occurs.
- `VALIDATED` when all sieve outcomes are acceptable.

Every run emits a forensic log entry per sieve for auditability.

## 7. API Contract (Non-Negotiable)
- **Endpoint:** `POST /analyze`
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
    }
  ]
}
```

## 8. Delivery Phases (Current Status)
- **Phase 1:** Backend shell, FastAPI/CORS, sieve modules, LangGraph orchestration - **completed**
- **Phase 2:** Deterministic hardening tests (GSTIN, Benford, fixture-backed `/analyze`) - **completed**
- **Phase 3:** Orchestrator/API resilience hardening - **completed**
- **Phase 4:** CISO console frontend integration and final demo polish - **next**

## 9. Runtime Baseline
Required environment configuration includes a valid FastRouter API key and model list values for extraction/vision routing.

If required runtime keys are missing or invalid, backend startup must fail immediately.