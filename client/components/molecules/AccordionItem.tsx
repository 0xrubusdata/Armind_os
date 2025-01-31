"use client";

import { Accordion, AccordionSummary, AccordionDetails, Typography, Button } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

interface AccordionItemProps {
  title: string;
  content?: string;
  isEditable?: boolean;
  onEdit?: () => void;
  nestedItems?: { id: number; name: string }[];
}

const AccordionItem: React.FC<AccordionItemProps> = ({ title, content, isEditable, onEdit, nestedItems }) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>{title}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        {nestedItems ? (
          // Mode sous-accordéon (utilisé pour Services et Agents)
          nestedItems.map((item) => (
            <Accordion key={item.id}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>{item.name}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>Détails de {item.name}</Typography>
                <Button variant="outlined">Modifier</Button>
              </AccordionDetails>
            </Accordion>
          ))
        ) : (
          // Mode simple (utilisé pour AI et Network)
          <>
            <Typography>{content}</Typography>
            {isEditable && <Button onClick={onEdit} variant="outlined">Modifier</Button>}
          </>
        )}
      </AccordionDetails>
    </Accordion>
  );
};

export default AccordionItem;
