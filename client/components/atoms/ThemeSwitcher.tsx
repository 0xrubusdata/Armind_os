"use client";

import { useTheme } from "../../context/ThemeProvider";
import { Button } from "@mui/material";

const ThemeSwitcher = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button variant="contained" color="primary" onClick={toggleTheme}>
      {theme === "pro" ? "🎮 Mode Crypto" : "💼 Mode Pro"}
    </Button>
  );
};

export default ThemeSwitcher;
