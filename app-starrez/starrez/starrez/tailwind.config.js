/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'college-blue': '#1E40AF',
        'college-gold': '#F59E0B',
        'flower-pink': '#EC4899',
        'flower-purple': '#8B5CF6',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}