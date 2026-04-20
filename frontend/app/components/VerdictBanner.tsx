'use client'

import { Verdict } from '../types'

interface VerdictBannerProps {
  verdict: Verdict | null
  analyzing: boolean
  errorMessage: string | null
}

export default function VerdictBanner({ verdict, analyzing, errorMessage }: VerdictBannerProps) {
  if (errorMessage) {
    return (
      <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel px-7 py-9 transition-all duration-300">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">FINAL VERDICT</h3>
        <p className="mt-2 text-2xl font-medium tracking-wide text-text-primary dark:text-dark-text-primary">PIPELINE ERROR</p>
        <p className="mt-3 max-w-4xl text-sm text-stone-600 dark:text-stone-400 md:text-base">{errorMessage}</p>
      </section>
    )
  }

  if (analyzing) {
    return (
      <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel px-7 py-9 transition-all duration-300">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">FINAL VERDICT</h3>
        <p className="mt-2 text-2xl font-medium tracking-wide text-text-primary dark:text-dark-text-primary">ANALYSIS IN PROGRESS</p>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400 md:text-base">Neural mesh is running deterministic and probabilistic forensics.</p>
      </section>
    )
  }

  if (!verdict) {
    return (
      <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel px-7 py-9 transition-all duration-300">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">FINAL VERDICT</h3>
        <p className="mt-2 text-2xl font-medium tracking-wide text-text-primary dark:text-dark-text-primary">AWAITING EVIDENCE</p>
        <p className="mt-3 text-sm text-stone-600 dark:text-stone-400 md:text-base">Upload an invoice to trigger the forensic command pipeline.</p>
      </section>
    )
  }

  const styleByVerdict: Record<Verdict, { border: string; title: string }> = {
    VALIDATED: {
      border: 'border border-primary-accent dark:border-primary-accent',
      title: 'VALIDATED',
    },
    SUSPICIOUS: {
      border: 'border border-subtle-border dark:border-slate-700',
      title: 'SUSPICIOUS',
    },
    FRAUD_DETECTED: {
      border: 'border-2 border-text-primary dark:border-red-500',
      title: 'FRAUD DETECTED',
    },
  }

  const style = styleByVerdict[verdict]

  return (
    <section className={`rounded-3xl bg-background dark:bg-dark-panel px-7 py-9 transition-all duration-300 ${style.border}`}>
      <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">FINAL VERDICT</h3>
      <p className="mt-2 text-2xl font-medium tracking-wide text-text-primary dark:text-dark-text-primary">{style.title}</p>
    </section>
  )
}
