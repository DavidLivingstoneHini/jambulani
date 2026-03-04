import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/components/**/*.{js,vue,ts}",
    "./app/layouts/**/*.vue",
    "./app/pages/**/*.vue",
    "./app/plugins/**/*.{js,ts}",
    "./app/app.vue",
    "./app/error.vue",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#fadd18",
          50: "#fffbeb",
          100: "#fef3c7",
          500: "#fadd18",
          600: "#d4a017",
        },
        dark: {
          DEFAULT: "#1a1a1a",
          800: "#2a2a2a",
          900: "#111111",
        },
      },
      fontFamily: {
        display: ['"Barlow Condensed"', "sans-serif"],
        heading: ['"Bebas Neue"', "sans-serif"],
        body: ["Barlow", "sans-serif"],
      },
      screens: {
        xs: "480px",
      },
    },
  },
  plugins: [],
} satisfies Config;
