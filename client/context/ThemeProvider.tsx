"use client";

import { createContext, useState, useContext } from "react";
import { themes } from "../config/theme";

type ThemeType = keyof typeof themes;

interface ThemeContextType {
  theme: ThemeType;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: "pro",
  toggleTheme: () => {}
});

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<ThemeType>("pro");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "pro" ? "crypto" : "pro"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div style={{
        backgroundColor: themes[theme].background,
        color: themes[theme].text,
        fontFamily: themes[theme].font,
        minHeight: "100vh"
      }}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
