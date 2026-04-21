'use client'

import { TrustScoreSummary } from '../lib/forensics'

interface TrustScorePanelProps {
  summary: TrustScoreSummary | null
  analyzing: boolean
  onOpenEvidence: () => void
}

export default function TrustScorePanel({ summary, analyzing, onOpenEvidence }: TrustScorePanelProps) {
  if (analyzing) {
    return (
      <section className="rounded-[2rem] border border-black/5 dark:border-white/5 backdrop-blur-md bg-stone-50/40 dark:bg-slate-900/40 px-6 py-4 transition-all duration-300">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">TRUST SCORE</h3>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400">Computing forensic confidence from six-sieve evidence...</p>
      </section>
    )
  }

  if (!summary) {
    return (
      <section className="rounded-[2rem] border border-black/5 dark:border-white/5 backdrop-blur-md bg-stone-50/40 dark:bg-slate-900/40 px-6 py-4 transition-all duration-300">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">TRUST SCORE</h3>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400">Run analysis to generate a trust score and human-readable fraud reasons.</p>
      </section>
    )
  }

  const flags = summary.breakdown.filter((item) => item.state === 'FAIL' || item.state === 'WARNING')

  return (
    <section className="rounded-[2rem] border border-black/5 dark:border-white/5 backdrop-blur-md bg-stone-50/40 dark:bg-slate-900/40 px-6 py-4 transition-all duration-300">
      <div className="grid gap-4 xl:grid-cols-[250px_1fr]">
        <div className="rounded-[1.5rem] border border-black/5 dark:border-white/5 bg-white/20 dark:bg-slate-900/50 p-5 flex flex-col justify-between shadow-sm">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">TRUST SCORE</h3>
            <p className="mt-2 text-6xl font-black leading-none text-text-primary dark:text-dark-text-primary">{summary.score}</p>
            <p className="mt-1 text-sm font-semibold uppercase tracking-[0.22em] text-text-primary dark:text-dark-text-primary">{summary.band} TRUST</p>
          </div>
          <p className="text-[10px] uppercase text-stone-500 dark:text-stone-400 mt-5 leading-tight opacity-80">{summary.formula}</p>
        </div>

        <div className="flex flex-col justify-between h-full">
          <div className="rounded-[1.5rem] border border-black/5 dark:border-white/5 bg-white/20 dark:bg-slate-900/50 p-5 shadow-sm flex-1">
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">ANOMALY TAGS</h3>
            {flags.length === 0 ? (
              <p className="text-sm text-stone-600 dark:text-stone-400">0 anomalies detected in standard matrix.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {flags.map((flag) => (
                  <span
                    key={flag.key}
                    className={`rounded-full px-3 py-1.5 text-xs font-bold uppercase tracking-wider shadow-sm ${
                      flag.state === 'FAIL'
                        ? 'bg-red-500/20 text-red-600 dark:text-red-400 border border-red-500/10'
                        : 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 border border-yellow-500/10'
                    }`}
                  >
                    {flag.label} {flag.state}
                  </span>
                ))}
              </div>
            )}
          </div>
          
          <button
            onClick={onOpenEvidence}
            className="mt-3 flex w-full animate-pulse items-center justify-center rounded-[1.25rem] border border-black/5 dark:border-white/5 bg-stone-200/50 dark:bg-slate-800/80 py-3 text-xs font-bold uppercase tracking-widest text-text-primary dark:text-dark-text-primary transition-all hover:bg-stone-300/50 dark:hover:bg-slate-700/80 hover:shadow-md"
          >
            <svg className="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            VIEW FORENSIC EVIDENCE
          </button>
        </div>
      </div>
    </section>
  )
}
