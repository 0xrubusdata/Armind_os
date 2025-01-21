export class IntentRecognizer {
    recognizeIntent(input: string): string {
      if (input.toLowerCase().includes("hello")) {
        return "greet";
      } else if (input.toLowerCase().includes("weather")) {
        return "weather_info";
      }
      return "unknown";
    }
  }
  