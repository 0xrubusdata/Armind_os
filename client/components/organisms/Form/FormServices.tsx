"use client";

import { useState } from "react";
import FormField from "../../molecules/FormField";

interface FormServiceProps {
  onSave: (data: { serviceName: string; serviceContext: string }) => void;
}

const FormService: React.FC<FormServiceProps> = () => {
  const [serviceName, setServiceName] = useState("");
  const [serviceContext, setServiceContext] = useState("");

  return (
    <div>
      <FormField
        label="Service's Name"
        name="serviceName"
        type="text"
        value={serviceName}
        onChange={(e) => setServiceName(e.target.value)}
      />

      <FormField
        label="Service's Context"
        name="serviceContext"
        type="text"
        value={serviceContext}
        onChange={(e) => setServiceContext(e.target.value)}
      />

    </div>
  );
};

export default FormService;
