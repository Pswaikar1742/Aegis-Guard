import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        background: '#FFFFFF',
        'text-primary': '#1A1815',
        'primary-accent': '#C3ED00',
        'subtle-border': '#EAEAEA',
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
