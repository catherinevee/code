FROM node:18-alpine
WORKDIR /app

# Dependencies change less frequently than source code
COPY package*.json ./
RUN apk add --no-cache python3 make g++ \
    && npm install \
    && npm cache clean --force
# Source code changes most frequently
COPY . .

# The app binds to port 3000
EXPOSE 3000

# Define the command to run your app
CMD ["node", "index.js"]
