"use client";

import { useState } from "react";
import FormField from "../../molecules/FormField";

interface FormNetworkProps {
  onSave: (data: { networkName: string; networkContext: string }) => void;
}

const FormNetwork: React.FC<FormNetworkProps> = () => {
  const [networkName, setNetworkName] = useState("");
  const [networkContext, setNetworkContext] = useState("");

  return (
    <div>
      <FormField
        label="Network's Name"
        name="networkName"
        type="text"
        value={networkName}
        onChange={(e) => setNetworkName(e.target.value)}
      />

      <FormField
        label="Network's Context"
        name="networkContext"
        type="text"
        value={networkContext}
        onChange={(e) => setNetworkContext(e.target.value)}
      />

    </div>
  );
};

export default FormNetwork;
