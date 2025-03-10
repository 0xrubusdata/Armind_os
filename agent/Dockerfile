FROM node:22

ARG AGENT_PORT

WORKDIR /app

# Copier package.json et package-lock.json pour installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le reste du code
COPY . .

# Construire l’application (assurez-vous d'avoir une commande build dans votre package.json)
RUN npm run build

EXPOSE ${AGENT_PORT}

# Démarrer en mode production
CMD ["npm", "run", "start:prod"]
