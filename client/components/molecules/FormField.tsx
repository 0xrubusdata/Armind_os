"use client";

import { TextField, Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from "@mui/material";
import { ChangeEvent, ChangeEventHandler } from "react";

interface FormFieldProps {
  label: string;
  name: string;
  type?: "text" | "select";
  value: string;
  onChange: (event: ChangeEvent<HTMLInputElement> | SelectChangeEvent) => void;
  options?: { value: string; label: string }[];
}

const FormField: React.FC<FormFieldProps> = ({ label, name, type = "text", value, onChange, options }) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement> | SelectChangeEvent) => {
    onChange(event);
  };

  return (
    <FormControl fullWidth margin="normal">
      <div className="mb-4">
  {label && (
    <label htmlFor={name} className="block text-gray-800 dark:text-gray-200 font-medium mb-2">
      {label}
    </label>
  )}

  {type === "select" ? (
    <select
      id={name}
      name={name}
      value={value}
      onChange={onChange}
      className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
    >
      {options?.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  ) : (
    <input
      id={name}
      type={type}
      name={name}
      value={value}
      onChange={onChange}
      placeholder={label}
      className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
    />
  )}
</div>

    </FormControl>
  );
};

export default FormField;
