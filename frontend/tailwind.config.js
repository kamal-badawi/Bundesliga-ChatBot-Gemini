/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx,html}", 
  ],
  theme: {
    extend: {width: {
        '1/20': '5%',
        '19/20': '95%',
      },
    colors: {
        bundesliga: {
    DEFAULT: '#E30613',
    dark: '#B2000F',
    light: '#FF4C5B', 
  },
        grau: {
          DEFAULT: '#6B7280',  
          dark: '#4B5563',     
          light: '#D1D5DB',  
        },
      },},
  },
  plugins: [],
}
