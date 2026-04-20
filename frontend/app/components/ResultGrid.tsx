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
        <h3 className="text-lg font-semibold uppercase tracking-[0.25em] text-text-primary">6-Sieve Result Grid</h3>
        <span className="text-xs uppercase tracking-[0.2em] text-stone-500">2 x 3 Forensic Matrix</span>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {CARD_CONFIG.map((card) => {
          const log = findLog(forensicLog, card.backendKey)
          const presentation = deriveCardPresentation(forensicLog, card.backendKey, card.label)
          const isPass = presentation.state === 'PASS'
          const isWarning = presentation.state === 'WARNING'
          const isFail = presentation.state === 'FAIL'

          const cardClass = isPass
            ? 'border border-primary-accent bg-background'
            : isWarning
            ? 'border border-subtle-border border-dashed bg-background'
            : isFail
            ? 'border-2 border-text-primary bg-background'
            : 'border border-subtle-border bg-background'

          const badgeClass = isPass
            ? 'border border-primary-accent bg-background text-text-primary'
            : isWarning
            ? 'border border-subtle-border bg-background text-text-primary'
            : isFail
            ? 'border border-text-primary bg-background text-text-primary'
            : 'border border-subtle-border bg-background text-text-primary'

          const title = isPass
            ? 'No Anomaly Detected.'
            : isWarning
            ? `REVIEW REQUIRED: ${presentation.reason}`
            : isFail
            ? `FRAUD DETECTED: ${presentation.reason}`
            : 'Awaiting analysis output.'

          return (
            <article key={card.label} className={`rounded-xl p-4 transition ${cardClass}`}>
              <div className="mb-3 flex items-start justify-between gap-2">
                <div>
                  <h4 className="text-lg font-semibold text-text-primary">{card.label}</h4>
                  <p className="text-xs text-text-primary">{card.subtitle}</p>
                </div>
                <span className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] ${badgeClass}`}>
                  {isPass ? 'PASS' : isWarning ? 'WARN' : isFail ? 'FAIL' : 'PENDING'}
                </span>
              </div>

              <p className="text-sm leading-relaxed text-text-primary">
                {title}
              </p>

              {log && presentation.technicalDetail ? (
                <p className="mt-2 text-xs leading-relaxed text-text-primary">Evidence: {presentation.technicalDetail}</p>
              ) : null}
            </article>
          )
        })}
      </div>
    </section>
  )
}
