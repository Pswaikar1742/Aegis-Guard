import './globals.css'
import { Inter, Share_Tech_Mono } from 'next/font/google'
import { ThemeProvider } from './components/ThemeProvider'

const primaryFont = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
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
    <html lang="en" suppressHydrationWarning className={`${primaryFont.variable} ${monoFont.variable}`}>
      <body className="bg-background text-text-primary dark:bg-dark-background dark:text-dark-text-primary [font-family:var(--font-sans)] transition-colors duration-300">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
