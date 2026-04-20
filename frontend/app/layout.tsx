import './globals.css'
import { Share_Tech_Mono, Space_Grotesk } from 'next/font/google'

const headingFont = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-heading',
})

const monoFont = Share_Tech_Mono({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-mono',
})

export const metadata = {
  title: 'Aegis Guard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${headingFont.variable} ${monoFont.variable}`}>
      <body className="bg-slate-950 text-emerald-500 [font-family:var(--font-heading)]">{children}</body>
    </html>
  )
}
