# MISSION BRIEF: AEGIS-GUARD (RIH 2026)

## 1. PRIMARY OBJECTIVE
We are building a **Neuro-Symbolic Fraud Mesh**, not a simple AI chatbot. Our mission is to **mathematically prove** invoice fraud, not just probabilistically guess. We serve a "CISO Persona" who demands 100% deterministic proof before blocking a payment.

## 2. THE GOLDEN STACK
- **Backend:** Python (FastAPI), LangGraph
- **Frontend:** Next.js, TailwindCSS
- **AI Core:** Google Gemini (1.5 Flash for extraction, 1.5 Pro for vision)
- **Deployment:** Render (Backend), Vercel (Frontend)

## 3. THE 4-SIEVE ARCHITECTURE
Our system is a pipeline of four independent, failsafe "Sieves."
- **Sieve 1 (Cryptographic):** Extracts PDF binary metadata (`PyPDF2`). Flags non-standard creators (e.g., "Canva", "Photoshop").
- **Sieve 2 (Checksum):** Extracts GSTIN/PAN strings (Gemini) and runs a deterministic modulo-10 algorithm (`checksum.py`).
- **Sieve 3 (Statistical):** Extracts line-item values (Gemini) and runs Benford's Law analysis (`benford.py`) to detect human-generated number patterns.
- **Sieve 4 (Spatial):** Uses Gemini Vision (`vision.py`) to detect pixel-level tampering (font mismatches, signature compression anomalies).

## 4. THE API CONTRACT (Non-Negotiable)
- **Endpoint:** `POST /analyze`
- **Request:** `Multipart/form-data` with a file named `invoice`.
- **Response (200 OK):**
  ```json
  {
    "status": "Completed",
    "final_judgement": "FRAUD_DETECTED" | "SUSPICIOUS" | "VALIDATED",
    "forensic_log": [
      {
        "sieve": "Cryptographic",
        "result": "ANOMALY",
        "details": "PDF Creator identified as 'Canva'. Expected enterprise ERP."
      },
      {
        "sieve": "Checksum",
        "result": "FAILED",
        "details": "GSTIN '27FAKE12345M1Z5' failed modulo-10 validation."
      }
    ]
  }