import { ProcessInput } from "../../application/use-cases/ProcessInput";
import { EnvironmentInput } from "../../domain/models/EnvironmentInput";

const useCase = new ProcessInput();

// Simulate environment inputs
const inputs: EnvironmentInput[] = [
  { type: "text", payload: "Hello" },
  { type: "text", payload: "What's the weather?" },
  { type: "text", payload: "Random input" },
];

// Process each input
inputs.forEach((input) => {
  const response = useCase.execute(input);

  if (response.action === "speak") {
    console.log(`Agent says: ${response.payload}`);
  } else if (response.action === "log") {
    console.log(`Agent logs: ${response.payload}`);
  }
});
