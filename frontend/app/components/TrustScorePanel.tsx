'use client'

import { TrustScoreSummary } from '../lib/forensics'

interface TrustScorePanelProps {
  summary: TrustScoreSummary | null
  analyzing: boolean
}

export default function TrustScorePanel({ summary, analyzing }: TrustScorePanelProps) {
  if (analyzing) {
    return (
      <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-text-primary dark:text-dark-text-primary">Trust Score</h3>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400">Computing forensic confidence from six-sieve evidence...</p>
      </section>
    )
  }

  if (!summary) {
    return (
      <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
        <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-text-primary dark:text-dark-text-primary">Trust Score</h3>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400">Run analysis to generate a trust score and human-readable fraud reasons.</p>
      </section>
    )
  }

  return (
    <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
      <div className="grid gap-5 lg:grid-cols-[270px_1fr]">
        <div className="rounded-2xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
          <h3 className="text-xs uppercase tracking-[0.25em] text-text-primary dark:text-dark-text-primary">Trust Score</h3>
          <p className="mt-3 text-6xl font-black leading-none text-text-primary dark:text-dark-text-primary">{summary.score}</p>
          <p className="mt-2 text-sm font-semibold uppercase tracking-[0.22em] text-text-primary dark:text-dark-text-primary">{summary.band} TRUST</p>
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-5">
            <p className="text-xs uppercase tracking-[0.2em] text-text-primary dark:text-dark-text-primary">Scoring Math</p>
            <p className="mt-2 text-sm text-text-primary dark:text-dark-text-primary">{summary.formula}</p>
            <p className="mt-1 text-xs text-stone-500 dark:text-stone-400">Risk factors: PASS=0, WARNING=0.45, FAIL/ANOMALY=1, ERROR=0.85</p>
          </div>

          <div className="rounded-2xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-5">
            <p className="text-xs uppercase tracking-[0.2em] text-text-primary dark:text-dark-text-primary">Why It Was Flagged</p>
            {summary.reasons.length === 0 ? (
              <p className="mt-2 text-sm text-text-primary dark:text-dark-text-primary">All sieve checks passed with no fraud indicators.</p>
            ) : (
              <ul className="mt-2 space-y-2 text-sm text-text-primary dark:text-dark-text-primary">
                {summary.reasons.map((reason) => (
                  <li key={reason} className="rounded-2xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel px-4 py-3">
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
