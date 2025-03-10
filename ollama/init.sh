#!/bin/sh

# Wait a few seconds before starting Ollama
sleep 5

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be available
echo "$(date) - Waiting for Ollama to be available..."
until curl -s http://localhost:11434/api/models > /dev/null 2>&1; do
    echo "$(date) - Ollama is not ready yet. Retrying in 5 seconds..."
    sleep 5
done

echo "$(date) - Downloading local model: ${MODEL_NAME}..."
ollama pull ${MODEL_NAME}

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "$(date) - Model ${MODEL_NAME} downloaded successfully"
else
    echo "$(date) - Failed to download model ${MODEL_NAME}"
    exit 1
fi

# Starting FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port ${OLLAMA_PORT}