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