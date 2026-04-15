/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './frontend/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './frontend/components/**/*.{js,ts,jsx,tsx,mdx}',
    './frontend/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: '#C9A84C',
        'gold-light': '#E8C97A',
        'gold-pale': '#F5EDD5',
        dark: {
          DEFAULT: '#0A0A0F',
          2: '#12121A',
          3: '#1C1C2A',
          4: '#252535',
        },
      },
      fontFamily: {
        'display': ['Playfair Display', 'serif'],
        'body': ['DM Sans', 'sans-serif'],
        'mono': ['Space Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}