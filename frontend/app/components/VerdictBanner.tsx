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
      <section className="rounded-2xl border-2 border-rose-500 bg-rose-950/40 px-6 py-8 shadow-[0_0_35px_rgba(244,63,94,0.25)]">
        <p className="text-xs uppercase tracking-[0.35em] text-rose-300">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-rose-400 md:text-5xl">PIPELINE ERROR</h2>
        <p className="mt-3 max-w-4xl text-sm text-rose-200 md:text-base">{errorMessage}</p>
      </section>
    )
  }

  if (analyzing) {
    return (
      <section className="relative overflow-hidden rounded-2xl border-2 border-emerald-500/70 bg-slate-900/80 px-6 py-8">
        <div className="absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-transparent via-emerald-400/25 to-transparent animate-scan" />
        <p className="text-xs uppercase tracking-[0.35em] text-emerald-300">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-emerald-400 md:text-5xl">ANALYSIS IN PROGRESS</h2>
        <p className="mt-3 text-sm text-emerald-200/85 md:text-base">Neural mesh is running deterministic and probabilistic forensics.</p>
      </section>
    )
  }

  if (!verdict) {
    return (
      <section className="rounded-2xl border-2 border-slate-700 bg-slate-900/70 px-6 py-8">
        <p className="text-xs uppercase tracking-[0.35em] text-slate-400">Final Verdict</p>
        <h2 className="mt-2 text-3xl font-bold tracking-wide text-emerald-500/80 md:text-5xl">AWAITING EVIDENCE</h2>
        <p className="mt-3 text-sm text-slate-300/85 md:text-base">Upload an invoice to trigger the forensic command pipeline.</p>
      </section>
    )
  }

  const styleByVerdict: Record<Verdict, { border: string; title: string; tone: string }> = {
    VALIDATED: {
      border: 'border-emerald-500 bg-emerald-950/20 shadow-[0_0_35px_rgba(16,185,129,0.2)]',
      title: 'VALIDATED',
      tone: 'text-emerald-300',
    },
    SUSPICIOUS: {
      border: 'border-amber-400 bg-amber-950/20 shadow-[0_0_35px_rgba(251,191,36,0.2)]',
      title: 'SUSPICIOUS',
      tone: 'text-amber-300',
    },
    FRAUD_DETECTED: {
      border: 'border-rose-500 bg-rose-950/20 shadow-[0_0_40px_rgba(244,63,94,0.3)]',
      title: 'FRAUD DETECTED',
      tone: 'text-rose-400',
    },
  }

  const style = styleByVerdict[verdict]

  return (
    <section className={`rounded-2xl border-2 px-6 py-8 ${style.border}`}>
      <p className="text-xs uppercase tracking-[0.35em] text-slate-300">Final Verdict</p>
      <h2 className={`mt-2 text-4xl font-black tracking-wide md:text-6xl ${style.tone}`}>{style.title}</h2>
    </section>
  )
}
