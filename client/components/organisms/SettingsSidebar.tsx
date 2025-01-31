"use client";

import { useState } from "react";
import { Drawer, IconButton, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import AccordionItem from "../molecules/AccordionItem";

const SettingsSidebar = () => {
  const [open, setOpen] = useState(true);

  return (
    <>
      {/* Bouton pour ouvrir la sidebar */}
      <IconButton
        onClick={() => setOpen(true)}
        sx={{ position: "absolute", top: 10, left: 10 }}
      >
        <MenuIcon />
      </IconButton>

      {/* Sidebar Drawer */}
      <Drawer anchor="left" open={open} onClose={() => setOpen(false)}>
        <div style={{ width: 250, padding: 10 }}>
          <IconButton onClick={() => setOpen(false)}>
            <CloseIcon />
          </IconButton>
          <Typography variant="h6">Settings</Typography>
          
          {/* AI Section */}
          <AccordionItem title="AI" content="OpenAI" isEditable onEdit={() => console.log("Edit AI")} />

          {/* Network Section */}
          <AccordionItem title="Network" content="Main Network" isEditable onEdit={() => console.log("Edit Network")} />

          {/* Services Section */}
          <AccordionItem title="Services" nestedItems={[
            { id: 1, name: "Service 1" },
            { id: 2, name: "Service 2" }
          ]} />

          {/* Agents Section */}
          <AccordionItem title="Agents" nestedItems={[
            { id: 1, name: "Agent 1" },
            { id: 2, name: "Agent 2" }
          ]} />
        </div>
      </Drawer>
    </>
  );
};

export default SettingsSidebar;
