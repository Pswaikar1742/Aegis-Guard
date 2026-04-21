import { BackendSieveOutcome, ForensicLogEntry } from '../types'

export type SieveDisplayState = 'PENDING' | 'PASS' | 'WARNING' | 'FAIL'

interface SieveWeightConfig {
  key: string
  label: string
  weight: number
}

const SIEVE_WEIGHT_CONFIG: SieveWeightConfig[] = [
  { key: 'Cryptographic', label: 'Metadata', weight: 15 },
  { key: 'Checksum', label: 'Checksum', weight: 10 },
  { key: 'Arithmetic', label: 'Arithmetic', weight: 20 },
  { key: 'Statistical', label: 'Benford', weight: 10 },
  { key: 'Spatial', label: 'Vision', weight: 20 },
  { key: 'OSINT', label: 'Registry', weight: 8 },
]

const OUTCOME_RISK: Record<BackendSieveOutcome, number> = {
  PASS: 0,
  WARNING: 0.2,
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
