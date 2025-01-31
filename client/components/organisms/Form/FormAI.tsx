"use client";

import { useState } from "react";
import FormField from "../../molecules/FormField";

interface FormAIProps {
  onSave: (data: { aiProvider: string; apiKey: string }) => void;
}

const FormAI: React.FC<FormAIProps> = () => {
  const [aiProvider, setAiProvider] = useState("");
  const [apiKey, setApiKey] = useState("");

  return (
    <div>
      <FormField
        label="AI Provider"
        name="aiProvider"
        type="select"
        value={aiProvider}
        onChange={(e) => setAiProvider(e.target.value)}
        options={[
          { value: "deepseek-r1", label: "DeepSeek R1" },
          { value: "llama3.2", label: "Llama 3.2" },
          { value: "gemma", label: "Gemma" },
          { value: "openai", label: "OpenAI" },
          { value: "anthropic", label: "Anthropic Claude" }
        ]}
      />

      <FormField
        label="API Key"
        name="apiKey"
        type="text"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
      />
    </div>
  );
};

export default FormAI;
