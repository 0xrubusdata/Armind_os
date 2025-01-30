import { Select as MUISelect, MenuItem, SelectChangeEvent } from "@mui/material";

interface CustomSelectProps {
  options: { value: string; label: string }[];
  value?: string;
  onChange?: (event: SelectChangeEvent<string>) => void;
  disabled?: boolean;
}

const Select: React.FC<CustomSelectProps> = ({ options, ...props }) => (
  <MUISelect {...props}>
    {options.map((option) => (
      <MenuItem key={option.value} value={option.value}>
        {option.label}
      </MenuItem>
    ))}
  </MUISelect>
);

export default Select;
