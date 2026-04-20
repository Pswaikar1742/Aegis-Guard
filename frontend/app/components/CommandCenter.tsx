'use client'

import { useCallback, useMemo, useRef, useState } from 'react'

import { extractErrorMessage, isAnalyzeResponse } from '../lib/contracts'
import { buildTrustScoreSummary } from '../lib/forensics'
import { AnalyzeResponse } from '../types'
import ThemeToggle from './ThemeToggle'
import FileUploader from './FileUploader'
import ForensicStream from './ForensicStream'
import ResultGrid from './ResultGrid'
import ResultGridSkeleton from './ResultGridSkeleton'
import TrustScorePanel from './TrustScorePanel'
import VerdictBanner from './VerdictBanner'

import TrustDnaChart from './TrustDnaChart'

const SYSTEM_SEQUENCE = [
  '[SYSTEM] Establishing secure uplink with backend mesh...',
  '[SYSTEM] Extracting invoice claims via Claude 3.5 Sonnet...',
  '[SYSTEM] Running S1 Metadata integrity checks...',
  '[SYSTEM] Running S2 GSTIN checksum validator...',
  '[SYSTEM] Running S3 arithmetic recomputation engine...',
  '[SYSTEM] Running S4 Benford variance analysis...',
  '[SYSTEM] Running S5 Gemini vision tamper scan...',
  '[SYSTEM] Running S6 registry corroboration check...',
  '[SYSTEM] Aggregating sieve outcomes into final verdict...',
]

function resolveApiBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_URL?.trim()
  if (configured) {
    return configured.replace(/\/$/, '')
  }
  return 'http://127.0.0.1:8010'
}

export default function CommandCenter() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [streamLogs, setStreamLogs] = useState<string[]>([])
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const streamTimerRef = useRef<number | null>(null)
  const streamCursorRef = useRef(0)

  const apiBaseUrl = useMemo(() => resolveApiBaseUrl(), [])

  const stopLogStream = useCallback(() => {
    if (streamTimerRef.current !== null) {
      window.clearInterval(streamTimerRef.current)
      streamTimerRef.current = null
    }
  }, [])

  const appendLog = useCallback((message: string) => {
    setStreamLogs((previous) => [...previous, message])
  }, [])

  const startLogStream = useCallback(
    (fileName: string) => {
      stopLogStream()
      streamCursorRef.current = 0
      setStreamLogs([`[SYSTEM] Intake accepted: ${fileName}`])

      streamTimerRef.current = window.setInterval(() => {
        if (streamCursorRef.current >= SYSTEM_SEQUENCE.length) {
          return
        }

        appendLog(SYSTEM_SEQUENCE[streamCursorRef.current])
        streamCursorRef.current += 1
      }, 700)
    },
    [appendLog, stopLogStream]
  )

  const runAnalysis = useCallback(async () => {
    if (!selectedFile || isAnalyzing) {
      return
    }

    setIsAnalyzing(true)
    setResult(null)
    setErrorMessage(null)
    startLogStream(selectedFile.name)

    try {
      const body = new FormData()
      body.append('invoice', selectedFile)

      const response = await fetch(`${apiBaseUrl}/api/v1/analyze`, {
        method: 'POST',
        body,
      })

      let payload: unknown = null
      try {
        payload = await response.json()
      } catch {
        payload = null
      }

      if (!response.ok) {
        throw new Error(extractErrorMessage(payload, response.status))
      }

      if (!isAnalyzeResponse(payload)) {
        throw new Error('Backend returned an unexpected response contract.')
      }

      setResult(payload)
      appendLog(`[SYSTEM] Forensic verdict: ${payload.final_judgement}.`)
      appendLog('[SYSTEM] Evidence graph sealed and archived.')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unexpected frontend runtime error.'
      setErrorMessage(message)
      appendLog(`[SYSTEM] Pipeline fault: ${message}`)
    } finally {
      stopLogStream()
      setIsAnalyzing(false)
    }
  }, [selectedFile, isAnalyzing, startLogStream, apiBaseUrl, appendLog, stopLogStream])

  const forensicLog = result?.forensic_log ?? []
  const trustScoreSummary = useMemo(() => {
    if (!result) {
      return null
    }
    return buildTrustScoreSummary(result.forensic_log)
  }, [result])

  return (
    <main className="min-h-screen bg-background dark:bg-dark-background text-text-primary dark:text-dark-text-primary transition-colors duration-300">
      <div className="mx-auto flex w-full max-w-screen-xl flex-col gap-8 px-6 py-10 md:px-12 md:py-14 lg:px-16 lg:py-16">
        <header className="flex items-start justify-between">
          <div className="space-y-3">
            <p className="text-xs uppercase tracking-[0.35em] text-text-primary dark:text-dark-text-primary">Aegis Guard</p>
            <h1 className="text-4xl font-bold uppercase tracking-[0.1em] text-text-primary dark:text-dark-text-primary md:text-5xl">
              Forensic Command Center
            </h1>
            <p className="max-w-3xl text-sm text-stone-600 dark:text-stone-400 md:text-base">
              Submit an invoice to activate the 6-sieve neuro-symbolic mesh and receive auditable fraud evidence in real time.
            </p>
          </div>
          <ThemeToggle />
        </header>

        <div className="grid gap-8">
          {/* Top Row */}
          <div className="grid gap-4 lg:grid-cols-2">
            <FileUploader
              selectedFile={selectedFile}
              isAnalyzing={isAnalyzing}
              onFileSelected={(file) => setSelectedFile(file)}
              onAnalyze={runAnalysis}
            />
            <VerdictBanner verdict={result?.final_judgement ?? null} analyzing={isAnalyzing} errorMessage={errorMessage} />
          </div>

          {/* Bottom Row */}
          <div className="grid gap-4 lg:grid-cols-2">
            {isAnalyzing ? <ResultGridSkeleton /> : <ResultGrid forensicLog={forensicLog} />}

            <div className="flex flex-col gap-4">
              <section className="flex flex-col justify-center rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
                <h3 className="mb-4 text-center text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">
                  TRUST DNA RADAR
                </h3>
                <TrustDnaChart forensicLog={forensicLog} verdict={result?.final_judgement ?? null} />
              </section>
              <ForensicStream logs={streamLogs} isAnalyzing={isAnalyzing} />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
