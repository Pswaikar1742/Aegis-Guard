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
