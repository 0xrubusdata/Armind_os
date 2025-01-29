# Stage 1: Build the app
FROM node:23 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build
RUN ls -la /app

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the build output to the nginx HTML directory
COPY --from=build /app/.next /usr/share/nginx/html

# Expose the port that nginx is listening on
EXPOSE 80

# No need for a command here, nginx will handle it