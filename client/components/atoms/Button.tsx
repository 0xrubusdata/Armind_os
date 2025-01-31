"use client";

import React from "react";
import { Button as MUIButton, ButtonProps } from "@mui/material";

const Button = (props: ButtonProps) => (
  <MUIButton variant="contained" {...props} />
);

export default Button;
