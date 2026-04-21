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
    <section className="flex flex-col overflow-hidden rounded-[2.5rem] border border-black/5 dark:border-white/5 backdrop-blur-md bg-stone-50/40 dark:bg-slate-900/40 p-0">
      <header className="flex items-center justify-between border-b border-black/5 dark:border-white/5 bg-white/20 dark:bg-slate-900/60 px-5 py-4">
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-text-primary dark:text-dark-text-primary">Neural Stream</h3>
        <span
          className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] transition-all duration-300 ${
            isAnalyzing
              ? 'border border-black/5 dark:border-white/5 bg-white/40 dark:bg-slate-700 text-text-primary dark:text-dark-text-primary shadow-sm'
              : 'border border-black/5 dark:border-white/5 bg-white/20 dark:bg-slate-800 text-text-primary dark:text-dark-text-primary'
          }`}
        >
          {isAnalyzing ? 'LIVE' : 'IDLE'}
        </span>
      </header>

      <div className="neural-scroll h-[300px] overflow-y-auto p-5 [font-family:var(--font-mono)]">
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
