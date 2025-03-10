FROM python:3.9-slim
# Définir un argument qui sera passé lors du build
ARG FAISS_PORT

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# Copier le fichier des dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copier le code source
COPY . .
EXPOSE ${FAISS_PORT}
# Définir ENV à partir de ARG pour que la variable soit disponible au runtime
ENV PORT=${FAISS_PORT}
# Démarrer l'application avec uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]