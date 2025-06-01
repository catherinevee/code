# Multi-stage build for CSS processing
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY src/ ./src/
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Build CSS
RUN npm run build-css

FROM nginx:alpine
COPY --from=builder /app/dist/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]