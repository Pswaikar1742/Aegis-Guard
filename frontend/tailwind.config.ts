import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        background: '#FFFFFF',
        'text-primary': '#1A1815',
        'primary-accent': '#C3ED00',
        'subtle-border': '#EAEAEA',
        'dark-background': '#0f172a',
        'dark-panel': '#1e293b',
        'dark-text-primary': '#e2e8f0',
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateX(-120%)' },
          '100%': { transform: 'translateX(120%)' },
        },
      },
      animation: {
        scan: 'scan 2.4s linear infinite',
      },
    },
  },
  plugins: [],
}

export default config
