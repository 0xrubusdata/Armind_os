# Use an official Python runtime as a parent image
FROM python:3.10-slim
# Définir un argument qui sera passé lors du build
ARG FAISS_PORT

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for model storage
RUN mkdir -p models

EXPOSE ${FAISS_PORT}
# Définir ENV à partir de ARG pour que la variable soit disponible au runtime
ENV PORT=${FAISS_PORT}
# Démarrer l'application avec uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]