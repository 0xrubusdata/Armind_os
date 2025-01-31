import { Box } from "@mui/material";
import SettingsSidebar from "../organisms/SettingsSidebar";

const Main: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <Box sx={{ display: "flex", flexDirection: "row", height: "calc(100vh - 80px)" }}>
      {/* Sidebar à gauche */}
      <SettingsSidebar />

      {/* Contenu principal qui prend l'espace restant */}
      <Box sx={{ flexGrow: 1, padding: 3, overflow: "auto" }}>
        {children}
      </Box>
    </Box>
  );
};

export default Main;
