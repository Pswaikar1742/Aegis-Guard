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
