'use client'

import { useCallback, useMemo, useRef, useState } from 'react'

import { extractErrorMessage, isAnalyzeResponse } from '../lib/contracts'
import { buildTrustScoreSummary } from '../lib/forensics'
import { AnalyzeResponse } from '../types'
import FileUploader from './FileUploader'
import ForensicStream from './ForensicStream'
import ResultGrid from './ResultGrid'
import TrustScorePanel from './TrustScorePanel'
import VerdictBanner from './VerdictBanner'

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
    <main className="min-h-screen bg-background text-text-primary">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-6 md:px-8 md:py-10">
        <header className="space-y-3">
          <p className="text-xs uppercase tracking-[0.35em] text-text-primary">Aegis Guard</p>
          <h1 className="text-3xl font-black uppercase tracking-[0.1em] text-text-primary md:text-5xl">
            Forensic Command Center
          </h1>
          <p className="max-w-3xl text-sm text-stone-600 md:text-base">
            Submit an invoice to activate the 6-sieve neuro-symbolic mesh and receive auditable fraud evidence in real time.
          </p>
        </header>

        <VerdictBanner verdict={result?.final_judgement ?? null} analyzing={isAnalyzing} errorMessage={errorMessage} />

        <TrustScorePanel summary={trustScoreSummary} analyzing={isAnalyzing} />

        <section className="grid gap-4 lg:grid-cols-2">
          <FileUploader
            selectedFile={selectedFile}
            isAnalyzing={isAnalyzing}
            onFileSelected={(file) => setSelectedFile(file)}
            onAnalyze={runAnalysis}
          />
          <ForensicStream logs={streamLogs} isAnalyzing={isAnalyzing} />
        </section>

        <ResultGrid forensicLog={forensicLog} />
      </div>
    </main>
  )
}
