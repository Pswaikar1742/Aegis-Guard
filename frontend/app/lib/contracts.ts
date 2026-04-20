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
