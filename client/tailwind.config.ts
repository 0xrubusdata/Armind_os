import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
} satisfies Config;

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        pro: {
          background: "#F8F9FA",
          text: "#212529",
          primary: "#0D6EFD",
          secondary: "#6C757D",
        },
        crypto: {
          background: "#0B0F19",
          text: "#E0E7FF",
          primary: "#8B5CF6",
          secondary: "#4C1D95",
        },
      },
    },
  },
  plugins: [],
};
