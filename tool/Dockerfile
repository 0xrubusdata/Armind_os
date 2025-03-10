FROM python:3.9-slim
# Définir un argument qui sera passé lors du build
ARG TOOL_PORT
# Installer les dépendances nécessaires pour la compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*
# Installer TA-Lib via le paquet Debian
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib_0.6.4_amd64.deb && \
    dpkg -i ta-lib_0.6.4_amd64.deb && \
    rm ta-lib_0.6.4_amd64.deb

WORKDIR /app
# Copier le fichier des dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copier le code source
COPY . .

EXPOSE ${TOOL_PORT}
# Définir ENV à partir de ARG pour que la variable soit disponible au runtime
ENV PORT=${TOOL_PORT}
# Démarrer l'application avec uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]