"use client";

import { useState, useEffect } from "react";
import Select from "./Select";

const languages = [
  { code: "en", label: "🇬🇧 English" },
  { code: "fr", label: "🇫🇷 Français" },
  { code: "es", label: "🇪🇸 Español" },
  { code: "ar", label: "🇸🇦 العربية" },
  { code: "jp", label: "🇯🇵 日本語" },
  { code: "pt", label: "🇵🇹 Português" },
  { code: "ru", label: "🇷🇺 Русский" }
];

interface LanguageSelectProps {
  onLanguageChange: (language: string) => void;
}

const LanguageSelect: React.FC<LanguageSelectProps> = ({ onLanguageChange }) => {
  const [language, setLanguage] = useState<string>("en");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLanguage = localStorage.getItem("language");
      if (savedLanguage) {
        setLanguage(savedLanguage);
        onLanguageChange(savedLanguage);
      }
    }
  }, [onLanguageChange]);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedLang = event.target.value;
    setLanguage(selectedLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("language", selectedLang);
    }
    onLanguageChange(selectedLang);
  };

  return (
    <Select
      value={language}
      onChange={handleChange}
      options={languages.map((lang) => ({
        value: lang.code,
        label: lang.label
      }))}
    />
  );
};

export default LanguageSelect;
