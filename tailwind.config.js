/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./templates/case-study/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        teal: {
          900: '#0B3B3C',
          700: '#0F5C5E',
          500: '#138585',
          300: '#4DB8B8',
        },
        orange: {
          700: '#B8500A',
          500: '#F28A1C',
        },
        ink: {
          900: '#1A2B33',
          500: '#5B6D78',
        },
        paper: {
          50:  '#F6F8F9',
          100: '#EBF1F3',
        },
        line: '#D8E2E6',
      },
      fontFamily: {
        display: ['Outfit', 'system-ui', 'sans-serif'],
        body:    ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 1px 3px rgba(11,59,60,.06), 0 4px 12px rgba(11,59,60,.04)',
        lift: '0 8px 24px rgba(11,59,60,.10)',
      },
      borderRadius: {
        card: '1rem',
      },
      maxWidth: {
        shell: '72rem',
      },
      animation: {
        marquee: 'marquee 40s linear infinite',
        'fade-in': 'fadeIn .6s ease both',
      },
      keyframes: {
        marquee: {
          '0%':   { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        fadeIn: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}