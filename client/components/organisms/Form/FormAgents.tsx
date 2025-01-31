"use client";

import { useState } from "react";
import FormField from "../../molecules/FormField";

interface FormAgentProps {
    onSave: (data: { agentName: string; agentContext: string }) => void;
  }
  
const FormAgent: React.FC<FormAgentProps> = ({ onSave }) => {
  const [name, setName] = useState("");
  const [image, setImage] = useState("");
  const [useGlobalAI, setUseGlobalAI] = useState(true);
  const [customAPIKey, setCustomAPIKey] = useState("");
  const [agents, setAgents] = useState<Array<{
    name: string;
    image: string;
    aiModel: "global" | "custom";
    apiKey?: string;
  }>>([]);
  

  const getAPIKey = (aiModel: string, agentAPIKey: string) => {
    if (aiModel === "global") {
      return process.env.NEXT_PUBLIC_OPEN_AI_API_KEY;
    }
    return agentAPIKey;
  };
  
return (
  <div>
    <FormField label="Nom de l'agent" value={name} onChange={setName} />
    <FormField label="Image (URL)" value={image} onChange={setImage} />

    <label className="block text-gray-800 dark:text-gray-200 font-medium mb-2">
      Modèle d'IA :
    </label>
    <select
      className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      value={useGlobalAI ? "global" : "custom"}
      onChange={(e) => setUseGlobalAI(e.target.value === "global")}
    >
      <option value="global">Utiliser l'AI Globale</option>
      <option value="custom">Définir un modèle spécifique</option>
    </select>

    {!useGlobalAI && (
      <FormField label="API Key" value={customAPIKey} onChange={setCustomAPIKey} />
    )}

    <button
      className="px-4 py-2 bg-green-600 text-white rounded"
      onClick={() => {
        if (name) {
          setAgents([
            ...agents,
            { name, image, aiModel: useGlobalAI ? "global" : "custom", apiKey: customAPIKey },
          ]);
          setName("");
          setImage("");
          setCustomAPIKey("");
        }
      }}
    >
      Ajouter l'agent
    </button>
  </div>
);

};

export default FormAgent;
