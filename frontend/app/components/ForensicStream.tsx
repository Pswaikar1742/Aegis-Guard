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
    <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-text-primary dark:text-dark-text-primary">Neural Stream</h3>
        <span
          className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] transition-all duration-300 ${
            isAnalyzing
              ? 'border border-subtle-border dark:border-slate-700 bg-stone-100 dark:bg-slate-700 text-text-primary dark:text-dark-text-primary'
              : 'border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel text-text-primary dark:text-dark-text-primary'
          }`}
        >
          {isAnalyzing ? 'LIVE' : 'IDLE'}
        </span>
      </div>

      <div className="neural-scroll h-[286px] overflow-y-auto rounded-2xl border border-subtle-border dark:border-slate-700 bg-stone-50 dark:bg-slate-800 p-4 [font-family:var(--font-mono)]">
        {logs.length === 0 ? (
          <p className="text-sm text-stone-500 dark:text-stone-400">[SYSTEM] Awaiting evidence stream initialization...</p>
        ) : (
          logs.map((log, index) => (
            <p key={`${log}-${index}`} className="mb-2 text-xs leading-relaxed text-text-primary dark:text-dark-text-primary md:text-sm">
              {log}
            </p>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </section>
  )
}
