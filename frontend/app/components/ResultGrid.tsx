'use client'

import { deriveCardPresentation } from '../lib/forensics'
import { ForensicLogEntry } from '../types'

interface ResultGridProps {
  forensicLog: ForensicLogEntry[]
}

interface SieveCardConfig {
  label: string
  backendKey: string
  subtitle: string
}

const CARD_CONFIG: SieveCardConfig[] = [
  { label: 'Metadata', backendKey: 'Cryptographic', subtitle: 'EXIF and creator integrity' },
  { label: 'Checksum', backendKey: 'Checksum', subtitle: 'GSTIN deterministic validation' },
  { label: 'Arithmetic', backendKey: 'Arithmetic', subtitle: 'Qty x Price + Tax consistency' },
  { label: 'Benford', backendKey: 'Statistical', subtitle: 'First-digit variance profile' },
  { label: 'Vision', backendKey: 'Spatial', subtitle: 'Pixel and font tamper scan' },
  { label: 'Registry', backendKey: 'OSINT', subtitle: 'Vendor and GSTIN corroboration' },
]

function findLog(forensicLog: ForensicLogEntry[], backendKey: string): ForensicLogEntry | null {
  return forensicLog.find((entry) => entry.sieve === backendKey) ?? null
}

export default function ResultGrid({ forensicLog }: ResultGridProps) {
  return (
    <section>
      <header className="mb-4 flex items-end justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">6-SIEVE RESULT GRID</h3>
        <span className="text-xs uppercase tracking-[0.2em] text-stone-500 dark:text-stone-400">2 x 3 Forensic Matrix</span>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {CARD_CONFIG.map((card) => {
          const log = findLog(forensicLog, card.backendKey)
          const presentation = deriveCardPresentation(forensicLog, card.backendKey, card.label)
          const isPass = presentation.state === 'PASS'
          const isWarning = presentation.state === 'WARNING'
          const isFail = presentation.state === 'FAIL'

          const cardClass = isPass
            ? 'border border-primary-accent bg-stone-50/40 dark:bg-slate-900/40 dark:border-primary-accent'
            : isWarning
            ? 'border border-black/10 border-dashed bg-stone-50/40 dark:bg-slate-900/40 dark:border-white/20'
            : isFail
            ? 'border-2 border-text-primary dark:border-red-500 bg-stone-50/40 dark:bg-slate-900/40'
            : 'border border-black/5 bg-stone-50/40 dark:bg-slate-900/40 dark:border-white/5'

          const badgeClass = isPass
            ? 'border border-primary-accent bg-white/50 dark:bg-slate-800/50 text-text-primary dark:text-dark-text-primary dark:border-primary-accent'
            : isWarning
            ? 'border border-black/10 bg-white/50 dark:bg-slate-800/50 text-text-primary dark:text-dark-text-primary dark:border-white/20'
            : isFail
            ? 'border border-text-primary dark:border-red-500 bg-white/50 dark:bg-slate-800/50 text-text-primary dark:text-dark-text-primary'
            : 'border border-black/5 bg-white/50 dark:bg-slate-800/50 text-text-primary dark:text-dark-text-primary dark:border-white/5'

          const title = isPass
            ? 'No Anomaly Detected.'
            : isWarning
            ? `REVIEW REQUIRED: ${presentation.reason}`
            : isFail
            ? `FRAUD DETECTED: ${presentation.reason}`
            : 'Awaiting analysis output.'

          return (
            <article key={card.label} className={`rounded-[1.5rem] backdrop-blur-md p-5 transition-all duration-300 hover:scale-[1.02] shadow-sm ${cardClass}`}>
              <div className="mb-3 flex items-start justify-between gap-2">
                <div>
                  <h4 className="text-lg font-semibold text-text-primary dark:text-dark-text-primary">{card.label}</h4>
                  <p className="text-xs text-text-primary dark:text-dark-text-primary opacity-70">{card.subtitle}</p>
                </div>
                <span className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] shadow-sm ${badgeClass}`}>
                  {isPass ? 'PASS' : isWarning ? 'WARN' : isFail ? 'FAIL' : 'PENDING'}
                </span>
              </div>

              <p className="text-sm leading-relaxed text-text-primary dark:text-dark-text-primary">
                {title}
              </p>

              {log && presentation.technicalDetail ? (
                <p className="mt-3 text-xs leading-relaxed text-stone-500 dark:text-stone-400 border-t border-black/5 dark:border-white/5 pt-2">Evidence: {presentation.technicalDetail}</p>
              ) : null}
            </article>
          )
        })}
      </div>
    </section>
  )
}
