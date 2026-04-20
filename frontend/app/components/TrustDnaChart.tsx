'use client'

import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'
import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer } from 'recharts'

import { ForensicLogEntry, Verdict } from '../types'

interface TrustDnaChartProps {
  forensicLog: ForensicLogEntry[]
  verdict: Verdict | null
}

const SCORE_MAP: Record<string, number> = {
  PASS: 100,
  WARNING: 50,
  FAILED: 0,
  ANOMALY: 0,
  ERROR: 0,
}

const SIEVES = [
  { key: 'Cryptographic', subject: 'Metadata' },
  { key: 'Checksum', subject: 'Checksum' },
  { key: 'Arithmetic', subject: 'Arithmetic' },
  { key: 'Statistical', subject: 'Benford' },
  { key: 'Spatial', subject: 'Vision' },
  { key: 'OSINT', subject: 'Registry' },
]

export default function TrustDnaChart({ forensicLog, verdict }: TrustDnaChartProps) {
  const { resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const data = SIEVES.map((s) => {
    const entry = forensicLog.find((e) => e.sieve === s.key)
    const score = entry ? SCORE_MAP[entry.result] ?? 0 : 0
    return { subject: s.subject, score }
  })

  // Avoid hydration mismatch for Recharts + Theme
  if (!mounted) {
    return <div className="h-[250px] w-full" />
  }

  const labelColor = resolvedTheme === 'dark' ? '#e2e8f0' : '#1A1815'

  let radarColor = '#C3ED00' // primary-accent
  if (verdict === 'VALIDATED') {
    radarColor = '#22c55e' // text-green-500
  } else if (verdict === 'SUSPICIOUS') {
    radarColor = '#eab308' // text-yellow-500
  } else if (verdict === 'FRAUD_DETECTED') {
    radarColor = '#ef4444' // text-red-500
  }

  return (
    <div className="h-[250px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke={resolvedTheme === 'dark' ? '#334155' : '#EAEAEA'} />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: labelColor, fontSize: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em' }}
          />
          <Radar
            name="Trust Score"
            dataKey="score"
            stroke={radarColor}
            fill={radarColor}
            fillOpacity={0.5}
            isAnimationActive={true}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
