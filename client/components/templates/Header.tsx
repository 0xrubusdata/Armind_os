"use client";

import React from "react";
import { Typography, Button } from "@mui/material";
import LanguageSelect from "../atoms/LanguageSelect";
import ThemeSwitcher from "../atoms/ThemeSwitcher";

const Header = () => {
  const handleLanguageChange = (language: string) => {
    // Handle language change here
    console.log('Language changed to:', language);
  };

  return (
    <>
      <Typography variant="body1">ArmindOS</Typography>
      <LanguageSelect onLanguageChange={handleLanguageChange} />
      <ThemeSwitcher />
      <Button onClick={() => {
  localStorage.clear();
  window.location.reload();
}}>Reset App</Button>

    </>
  );
};

export default Header;
