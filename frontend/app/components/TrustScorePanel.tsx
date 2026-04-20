'use client'

import { TrustScoreSummary } from '../lib/forensics'

interface TrustScorePanelProps {
  summary: TrustScoreSummary | null
  analyzing: boolean
}

export default function TrustScorePanel({ summary, analyzing }: TrustScorePanelProps) {
  if (analyzing) {
    return (
      <section className="rounded-2xl border border-subtle-border bg-background p-5">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-text-primary">Trust Score</h3>
        <p className="mt-3 text-sm text-stone-600">Computing forensic confidence from six-sieve evidence...</p>
      </section>
    )
  }

  if (!summary) {
    return (
      <section className="rounded-2xl border border-subtle-border bg-background p-5">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-text-primary">Trust Score</h3>
        <p className="mt-3 text-sm text-stone-600">Run analysis to generate a trust score and human-readable fraud reasons.</p>
      </section>
    )
  }

  return (
    <section className="rounded-2xl border border-subtle-border bg-background p-5">
      <div className="grid gap-5 lg:grid-cols-[270px_1fr]">
        <div className="rounded-xl border border-subtle-border bg-background p-5">
          <h3 className="text-xs uppercase tracking-[0.25em] text-text-primary">Trust Score</h3>
          <p className="mt-3 text-6xl font-black leading-none text-text-primary">{summary.score}</p>
          <p className="mt-2 text-sm font-semibold uppercase tracking-[0.22em] text-text-primary">{summary.band} TRUST</p>
        </div>

        <div className="space-y-4">
          <div className="rounded-lg border border-subtle-border bg-background p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-text-primary">Scoring Math</p>
            <p className="mt-2 text-sm text-text-primary">{summary.formula}</p>
            <p className="mt-1 text-xs text-stone-500">Risk factors: PASS=0, WARNING=0.45, FAIL/ANOMALY=1, ERROR=0.85</p>
          </div>

          <div className="rounded-lg border border-subtle-border bg-background p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-text-primary">Why It Was Flagged</p>
            {summary.reasons.length === 0 ? (
              <p className="mt-2 text-sm text-text-primary">All sieve checks passed with no fraud indicators.</p>
            ) : (
              <ul className="mt-2 space-y-2 text-sm text-text-primary">
                {summary.reasons.map((reason) => (
                  <li key={reason} className="rounded-md border border-subtle-border bg-background px-3 py-2">
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
