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
    ? 'border-primary-accent bg-background dark:bg-dark-panel'
    : 'border-subtle-border bg-background dark:bg-dark-panel'

  return (
    <section className="rounded-3xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-6">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">UPLOAD ZONE</h3>

      <div
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        className={`rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-300 ${containerClasses}`}
      >
        <p className="text-sm text-stone-700 dark:text-stone-300">Drop invoice PDF or image here</p>
        <p className="mt-2 text-xs uppercase tracking-[0.2em] text-stone-500 dark:text-stone-400">PDF / PNG / JPG / WEBP</p>

        <button
          type="button"
          disabled={isAnalyzing}
          onClick={() => inputRef.current?.click()}
          className="mt-5 rounded-xl border border-subtle-border dark:border-slate-700 px-4 py-2 text-sm font-semibold text-text-primary dark:text-dark-text-primary transition-all duration-300 hover:bg-stone-100 dark:hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
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

      <div className="mt-4 rounded-2xl border border-subtle-border dark:border-slate-700 bg-stone-50 dark:bg-slate-800 p-4 text-sm text-stone-700 dark:text-stone-300">
        {selectedFile ? (
          <>
            <p className="text-text-primary dark:text-dark-text-primary">Selected: {selectedFile.name}</p>
            <p className="text-xs text-stone-500 dark:text-stone-400">{Math.max(1, Math.round(selectedFile.size / 1024))} KB</p>
          </>
        ) : (
          <p>No evidence file selected yet.</p>
        )}
      </div>

      <button
        type="button"
        disabled={isAnalyzing || !selectedFile}
        onClick={onAnalyze}
        className="mt-4 w-full rounded-2xl border border-lime-400 dark:border-lime-500 bg-lime-400 dark:bg-lime-500 px-8 py-3 text-sm font-bold uppercase tracking-wider text-text-primary transition-colors duration-300 hover:bg-lime-500 dark:hover:bg-lime-600 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isAnalyzing ? 'Analyzing...' : 'Run Neural Analysis'}
      </button>
    </section>
  )
}
