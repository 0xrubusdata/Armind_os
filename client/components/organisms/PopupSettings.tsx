"use client";

import { useEffect, useState } from "react";
import FormLanguage from "./Form/FormLanguage";
import FormAI from "./Form/FormAI";
import FormNetwork from "./Form/FormNetwork";
import FormServices from "./Form/FormServices";
import FormAgents from "./Form/FormAgents";

const PopupSettings = () => {
  const [step, setStep] = useState(0);
  const [language, setLanguage] = useState("en");

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    setStep(1); // Passe directement à FormAI après sélection de la langue
  };

  const nextStep = () => setStep((prev) => prev + 1);

  const handleSave = () => {
    console.log("Save");
  };

  useEffect(() => {
    document.body.classList.add("overflow-hidden");
    return () => document.body.classList.remove("overflow-hidden");
  }, []);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-md z-50">
      <div className="bg-white dark:bg-gray-900 shadow-xl rounded-lg p-6 w-full max-w-md transform transition-all duration-300 ease-in-out scale-95 animate-fadeIn">
        <h2 className="text-xl font-semibold text-center mb-4 text-gray-900 dark:text-gray-100">
          {step === 0 ? "Select Language" :
           step === 1 ? "AI Configuration" :
           step === 2 ? "Network Configuration" :
           step === 3 ? "Service Configuration" :
                        "Agent Configuration"}
        </h2>

        {step === 0 && <FormLanguage onLanguageChange={handleLanguageChange} />}
        {step === 1 && <FormAI onSave={nextStep} />}
        {step === 2 && <FormNetwork onSave={nextStep} />}
        {step === 3 && <FormServices onSave={nextStep} />}
        {step === 4 && <FormAgents onSave={nextStep} />}

        <div className="mt-6 flex justify-between">
          <button
            className="px-4 py-2 bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white rounded transition-all hover:bg-gray-400 dark:hover:bg-gray-600 disabled:opacity-50"
            disabled={step === 0}
            onClick={() => setStep((prev) => prev - 1)}
          >
            Back
          </button>

          <button
            className="px-4 py-2 bg-green-600 dark:bg-green-500 text-white rounded transition-all hover:bg-green-700 dark:hover:bg-green-400"
            onClick={() => {
              handleSave();
              setStep((prev) => prev + 1);
            }}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default PopupSettings;
