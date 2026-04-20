'use client'

import { useEffect, useRef } from 'react'

interface ForensicStreamProps {
  logs: string[]
  isAnalyzing: boolean
}

export default function ForensicStream({ logs, isAnalyzing }: ForensicStreamProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">Neural Stream</h3>
        <span
          className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] ${
            isAnalyzing
              ? 'border border-emerald-400/70 bg-emerald-500/15 text-emerald-300'
              : 'border border-slate-600 bg-slate-700/40 text-slate-300'
          }`}
        >
          {isAnalyzing ? 'LIVE' : 'IDLE'}
        </span>
      </div>

      <div className="neural-scroll h-[286px] overflow-y-auto rounded-lg border border-slate-800 bg-slate-950/80 p-3 [font-family:var(--font-mono)]">
        {logs.length === 0 ? (
          <p className="text-sm text-slate-400">[SYSTEM] Awaiting evidence stream initialization...</p>
        ) : (
          logs.map((log, index) => (
            <p key={`${log}-${index}`} className="mb-2 text-xs leading-relaxed text-emerald-200/95 md:text-sm">
              {log}
            </p>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </section>
  )
}
