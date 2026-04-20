'use client'

import { ChangeEvent, DragEvent, useRef, useState } from 'react'

interface FileUploaderProps {
  selectedFile: File | null
  isAnalyzing: boolean
  onFileSelected: (file: File) => void
  onAnalyze: () => void
}

const ACCEPTED_FILE_TYPES = [
  'application/pdf',
  'image/png',
  'image/jpeg',
  'image/webp',
]

export default function FileUploader({
  selectedFile,
  isAnalyzing,
  onFileSelected,
  onAnalyze,
}: FileUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement | null>(null)

  const pickFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }
    onFileSelected(file)
  }

  const onDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(true)
  }

  const onDragLeave = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(false)
  }

  const onDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(false)

    const file = event.dataTransfer.files?.[0]
    if (!file) {
      return
    }

    onFileSelected(file)
  }

  const containerClasses = isDragging
    ? 'border-emerald-400 bg-emerald-500/10 shadow-[0_0_30px_rgba(16,185,129,0.2)]'
    : 'border-slate-700 bg-slate-900/75'

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5">
      <h3 className="mb-4 text-lg font-semibold uppercase tracking-[0.25em] text-emerald-400">Upload Zone</h3>

      <div
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        className={`rounded-xl border-2 border-dashed p-8 text-center transition ${containerClasses}`}
      >
        <p className="text-sm text-emerald-200/90">Drop invoice PDF or image here</p>
        <p className="mt-2 text-xs uppercase tracking-[0.2em] text-slate-400">PDF / PNG / JPG / WEBP</p>

        <button
          type="button"
          disabled={isAnalyzing}
          onClick={() => inputRef.current?.click()}
          className="mt-5 rounded-md border border-emerald-500/70 px-4 py-2 text-sm font-semibold text-emerald-300 transition hover:bg-emerald-500/10 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Select File
        </button>

        <input
          ref={inputRef}
          id="invoice-file"
          type="file"
          onChange={pickFile}
          accept={ACCEPTED_FILE_TYPES.join(',')}
          className="hidden"
        />
      </div>

      <div className="mt-4 rounded-lg border border-slate-800 bg-slate-950/70 p-3 text-sm text-slate-300">
        {selectedFile ? (
          <>
            <p className="text-emerald-300">Selected: {selectedFile.name}</p>
            <p className="text-xs text-slate-400">{Math.max(1, Math.round(selectedFile.size / 1024))} KB</p>
          </>
        ) : (
          <p>No evidence file selected yet.</p>
        )}
      </div>

      <button
        type="button"
        disabled={isAnalyzing || !selectedFile}
        onClick={onAnalyze}
        className="mt-4 w-full rounded-lg border border-emerald-400 bg-emerald-500/10 px-4 py-3 text-sm font-bold uppercase tracking-[0.2em] text-emerald-300 transition hover:bg-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isAnalyzing ? 'Analyzing...' : 'Run Neural Analysis'}
      </button>
    </section>
  )
}
