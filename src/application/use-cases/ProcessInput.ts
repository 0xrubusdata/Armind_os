import { EnvironmentInput } from "../../domain/models/EnvironmentInput";
import { AgentResponse } from "../../domain/models/AgentResponse";
import { IntentRecognizer } from "../../infrastructure/services/IntentRecognizer";

export class ProcessInput {
  private intentRecognizer: IntentRecognizer;

  constructor() {
    this.intentRecognizer = new IntentRecognizer();
  }

  execute(input: EnvironmentInput): AgentResponse {
    const intent = this.intentRecognizer.recognizeIntent(input.payload);

    switch (intent) {
      case "greet":
        return { action: "speak", payload: "Hello! How can I assist you?" };
      case "weather_info":
        return { action: "speak", payload: "I can't fetch weather data yet, but I'm learning!" };
      default:
        return { action: "log", payload: "I don't understand this input." };
    }
  }
}
