import { Button as MUIButton, ButtonProps } from "@mui/material";

interface CustomButtonProps extends ButtonProps {
  children: React.ReactNode;
}

const Button: React.FC<CustomButtonProps> = ({ children, variant = "contained", ...props }) => (
  <MUIButton variant={variant} {...props}>
    {children}
  </MUIButton>
);

export default Button;
