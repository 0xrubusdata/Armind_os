FROM node:22

ARG CLIENT_PORT

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE ${CLIENT_PORT}

CMD ["npm", "start"]
