FROM node:18-alpine

# Create app directory and a non-root user
WORKDIR /app
RUN addgroup -g 1001 appuser && \
    adduser -u 1001 -G appuser -D appuser

COPY --chown=appuser:appuser . .
RUN npm install

# Switch to non-root user
USER appuser

CMD ["node", "server.js"]
