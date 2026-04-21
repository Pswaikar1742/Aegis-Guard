'use client'

import { motion } from 'framer-motion'
import { useEffect, useRef } from 'react'
import { TrustScoreSummary } from '../lib/forensics'

interface ForensicReasonModalProps {
  summary: TrustScoreSummary
  onClose: () => void
}

export default function ForensicReasonModal({ summary, onClose }: ForensicReasonModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKeyDown)
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    }
  }, [onClose])

  return (
    <motion.div
      ref={overlayRef}
      role="dialog"
      aria-modal="true"
      onClick={(e) => {
        if (e.target === overlayRef.current) onClose()
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xl sm:p-6"
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.8, opacity: 0, y: 20 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="w-full max-w-2xl overflow-hidden rounded-[2.5rem] border border-white/10 bg-slate-900/80 shadow-2xl backdrop-blur-2xl"
      >
        <div className="p-8 md:p-10">
          <header className="mb-8 flex items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-white">
              Forensic Deep-Dive Log
            </h2>
            <button
              onClick={onClose}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-stone-300 transition-colors hover:bg-white/20 hover:text-white"
              aria-label="Close modal"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </header>

          <div className="space-y-6 max-h-[60vh] overflow-y-auto pr-2">
            {summary.reasons.length === 0 ? (
              <div className="flex flex-col items-center gap-4 py-8 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-500/20 text-green-400">
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <p className="text-lg font-medium text-stone-300">
                  No anomalous markers were triggered during the sieve pipeline. The baseline looks solid.
                </p>
              </div>
            ) : (
              <ul className="space-y-4">
                {summary.reasons.map((reason, idx) => {
                  const label = reason.split(':')[0]
                  const description = reason.split(':').slice(1).join(':').trim()
                  
                  return (
                    <li key={idx} className="flex gap-4 items-start rounded-[1.5rem] bg-white/5 p-6 border border-white/5">
                      <span className="mt-1 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20 text-red-500">
                        <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </span>
                      <div>
                        <span className="mb-1 block text-xs font-bold uppercase tracking-widest text-red-400">
                          Sieve Flag: {label}
                        </span>
                        <p className="text-base font-medium leading-relaxed text-stone-200 md:text-lg">
                          {description || reason}
                        </p>
                      </div>
                    </li>
                  )
                })}
              </ul>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}
