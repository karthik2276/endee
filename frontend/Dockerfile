# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies based on package.json
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine

# Copy the build output from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
