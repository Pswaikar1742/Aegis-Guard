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
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">6-Sieve Result Grid</h3>
        <span className="text-xs uppercase tracking-[0.2em] text-slate-400">2 x 3 Forensic Matrix</span>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {CARD_CONFIG.map((card) => {
          const log = findLog(forensicLog, card.backendKey)
          const presentation = deriveCardPresentation(forensicLog, card.backendKey, card.label)
          const isPass = presentation.state === 'PASS'
          const isWarning = presentation.state === 'WARNING'
          const isFail = presentation.state === 'FAIL'

          const cardClass = isPass
            ? 'border-emerald-500 bg-emerald-950/20'
            : isWarning
            ? 'border-amber-400 bg-amber-950/20'
            : isFail
            ? 'border-rose-500 bg-rose-950/20 animate-pulse'
            : 'border-slate-700 bg-slate-900/65'

          const badgeClass = isPass
            ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/50'
            : isWarning
            ? 'bg-amber-400/15 text-amber-300 border border-amber-400/50'
            : isFail
            ? 'bg-rose-500/15 text-rose-300 border border-rose-500/50'
            : 'bg-slate-500/15 text-slate-300 border border-slate-500/40'

          const title = isPass
            ? 'No Anomaly Detected.'
            : isWarning
            ? `REVIEW REQUIRED: ${presentation.reason}`
            : isFail
            ? `FRAUD DETECTED: ${presentation.reason}`
            : 'Awaiting analysis output.'

          return (
            <article key={card.label} className={`rounded-xl border p-4 transition ${cardClass}`}>
              <div className="mb-3 flex items-start justify-between gap-2">
                <div>
                  <h4 className="text-lg font-semibold text-emerald-300">{card.label}</h4>
                  <p className="text-xs text-slate-300">{card.subtitle}</p>
                </div>
                <span className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] ${badgeClass}`}>
                  {isPass ? 'PASS' : isWarning ? 'WARN' : isFail ? 'FAIL' : 'PENDING'}
                </span>
              </div>

              <p className={`text-sm leading-relaxed ${isFail ? 'text-rose-200' : isWarning ? 'text-amber-200' : 'text-emerald-200/90'}`}>
                {title}
              </p>

              {log && presentation.technicalDetail ? (
                <p className="mt-2 text-xs leading-relaxed text-slate-400">Evidence: {presentation.technicalDetail}</p>
              ) : null}
            </article>
          )
        })}
      </div>
    </section>
  )
}
