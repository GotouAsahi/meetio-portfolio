/** @type {import('tailwindcss').Config} */
module.exports = {
  // purge: [],　
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      animation: {
        "fade-in": "fade-in 3.0s",
        "slide-in-right": "slide-in-right 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940)   both"
      },
      keyframes: {
        "fade-in": {
          "0%": {
            opacity: "0.3"
          },
          to: {
            opacity: "1"
          }
        },
        "slide-in-right": {
          "0%": {
            transform: "translateX(1000px)",
            opacity: "1"
          },
          to: {
            transform: "translateX(0)",
            opacity: "1"
          }
        }
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

