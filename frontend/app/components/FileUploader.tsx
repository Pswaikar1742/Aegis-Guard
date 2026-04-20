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
    ? 'border-primary-accent bg-background'
    : 'border-subtle-border bg-background'

  return (
    <section className="rounded-2xl border border-subtle-border bg-background p-5">
      <h3 className="mb-4 text-lg font-semibold uppercase tracking-[0.25em] text-text-primary">Upload Zone</h3>

      <div
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        className={`rounded-xl border-2 border-dashed p-8 text-center transition ${containerClasses}`}
      >
        <p className="text-sm text-stone-700">Drop invoice PDF or image here</p>
        <p className="mt-2 text-xs uppercase tracking-[0.2em] text-stone-500">PDF / PNG / JPG / WEBP</p>

        <button
          type="button"
          disabled={isAnalyzing}
          onClick={() => inputRef.current?.click()}
          className="mt-5 rounded-md border border-subtle-border px-4 py-2 text-sm font-semibold text-text-primary transition hover:bg-stone-100 disabled:cursor-not-allowed disabled:opacity-50"
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

      <div className="mt-4 rounded-lg border border-subtle-border bg-stone-50 p-3 text-sm text-stone-700">
        {selectedFile ? (
          <>
            <p className="text-text-primary">Selected: {selectedFile.name}</p>
            <p className="text-xs text-stone-500">{Math.max(1, Math.round(selectedFile.size / 1024))} KB</p>
          </>
        ) : (
          <p>No evidence file selected yet.</p>
        )}
      </div>

      <button
        type="button"
        disabled={isAnalyzing || !selectedFile}
        onClick={onAnalyze}
        className="mt-4 w-full rounded-lg border border-primary-accent bg-primary-accent px-4 py-3 text-sm font-bold uppercase tracking-[0.2em] text-text-primary transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isAnalyzing ? 'Analyzing...' : 'Run Neural Analysis'}
      </button>
    </section>
  )
}
