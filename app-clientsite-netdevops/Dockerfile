# Multi-stage build for optimized production image
# Stage 1: Build stage (if needed for future enhancements like build tools)
FROM node:18-alpine AS builder

# Set working directory for build stage
WORKDIR /build

# Install build dependencies if needed (currently minimal for static site)
# This stage can be expanded for TypeScript compilation, SASS processing, etc.
RUN apk add --no-cache \
    # Only essential build tools
    git \
    && rm -rf /var/cache/apk/*

# Copy package files first for better Docker layer caching
# COPY package*.json ./
# RUN npm ci --only=production --no-audit --no-fund

# Copy source files
COPY index.html ./

# Build optimization step (placeholder for future build processes)
# RUN npm run build

# Stage 2: Production image with nginx
FROM nginx:1.25-alpine AS production

# Metadata labels for better container management
LABEL maintainer="your-email@example.com" \
      version="1.0.0" \
      description="Cute customizable website with optimized nginx" \
      org.opencontainers.image.title="Cute Website" \
      org.opencontainers.image.description="A delightfully customizable website template" \
      org.opencontainers.image.vendor="Your Company"

# Create non-root user for security
RUN addgroup -g 1001 -S nginx-app && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx-app -g nginx-app nginx-app

# Install only necessary runtime packages
RUN apk add --no-cache \
    # Security updates and certificates
    ca-certificates \
    # Timezone data for proper logging
    tzdata \
    # Curl for health checks
    curl \
    # Remove package cache to reduce image size
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/*

# Create necessary directories with proper permissions
RUN mkdir -p /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
             /var/log/nginx \
             /var/run \
    && chown -R nginx-app:nginx-app /var/cache/nginx \
    && chown -R nginx-app:nginx-app /var/log/nginx \
    && chown -R nginx-app:nginx-app /var/run

# Copy optimized nginx configuration
COPY --chown=nginx-app:nginx-app nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx-app:nginx-app default.conf /etc/nginx/conf.d/default.conf

# Copy website files from builder stage (or directly if no build needed)
COPY --from=builder --chown=nginx-app:nginx-app /build/index.html /usr/share/nginx/html/

# Copy additional static assets if they exist
# COPY --chown=nginx-app:nginx-app ./assets/ /usr/share/nginx/html/assets/

# Set proper permissions for web content
RUN chmod -R 755 /usr/share/nginx/html

# Create startup script for better container initialization
COPY --chown=nginx-app:nginx-app entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER nginx-app

# Expose port (using non-privileged port)
EXPOSE 8080

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Use entrypoint script for better initialization
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command
CMD ["nginx", "-g", "daemon off;"]