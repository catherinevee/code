# Build stage for React frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Build stage for Node.js backend
FROM node:18-alpine AS backend-build
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm install
COPY backend/ ./

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=backend-build /app/backend ./
COPY --from=frontend-build /app/frontend/build ./public
ENV NODE_ENV=production
EXPOSE 4000
CMD ["node", "server.js"]
