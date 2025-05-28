# Dockerfile for lightweight nginx web application
# Multi-stage build for optimal image size and security

# Stage 1: Build stage (if needed for processing static assets)
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files if you have any build process
# COPY package*.json ./
# RUN npm ci --only=production

# For this simple HTML app, we just copy the files
COPY index.html ./

# Stage 2: Production stage with nginx
FROM nginx:1.25-alpine

# Metadata labels for better container management
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Lightweight modern web application with nginx"

# Install additional packages for better functionality and security
RUN apk add --no-cache \
    # Security updates
    curl \
    # For health checks
    wget \
    # For log rotation and management
    logrotate \
    # Clean up cache
    && rm -rf /var/cache/apk/*

# Create non-root user for security (nginx will still run as nginx user)
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy HTML files from builder stage (or directly)
COPY --from=builder /app/index.html /usr/share/nginx/html/
# Alternative: COPY index.html /usr/share/nginx/html/

# Create custom error pages for better user experience
RUN echo '<!DOCTYPE html><html><head><title>404 Not Found</title><style>body{font-family:Arial,sans-serif;text-align:center;padding:50px;background:#f5f5f5;}h1{color:#333;font-size:2em;}p{color:#666;font-size:1.2em;}a{color:#007bff;text-decoration:none;}a:hover{text-decoration:underline;}</style></head><body><h1>404 - Page Not Found</h1><p>The page you are looking for does not exist.</p><a href="/">Return to Home</a></body></html>' > /usr/share/nginx/html/404.html

RUN echo '<!DOCTYPE html><html><head><title>500 Server Error</title><style>body{font-family:Arial,sans-serif;text-align:center;padding:50px;background:#f5f5f5;}h1{color:#d32f2f;font-size:2em;}p{color:#666;font-size:1.2em;}a{color:#007bff;text-decoration:none;}a:hover{text-decoration:underline;}</style></head><body><h1>500 - Server Error</h1><p>Something went wrong on our end. Please try again later.</p><a href="/">Return to Home</a></body></html>' > /usr/share/nginx/html/50x.html

# Create robots.txt for SEO
RUN echo 'User-agent: *' > /usr/share/nginx/html/robots.txt && \
    echo 'Allow: /' >> /usr/share/nginx/html/robots.txt && \
    echo 'Sitemap: /sitemap.xml' >> /usr/share/nginx/html/robots.txt

# Create a basic sitemap.xml
RUN echo '<?xml version="1.0" encoding="UTF-8"?>' > /usr/share/nginx/html/sitemap.xml && \
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' >> /usr/share/nginx/html/sitemap.xml && \
    echo '  <url><loc>http://localhost/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>' >> /usr/share/nginx/html/sitemap.xml && \
    echo '</urlset>' >> /usr/share/nginx/html/sitemap.xml

# Set proper permissions for security
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Create directory for nginx cache (if needed)
RUN mkdir -p /var/cache/nginx && \
    chown -R nginx:nginx /var/cache/nginx

# Create nginx log directory with proper permissions
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx

# Setup log rotation for nginx logs
COPY <<EOF /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 nginx nginx
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 \$(cat /var/run/nginx.pid)
        fi
    endscript
}
EOF

# Copy startup script for better container management
COPY <<'EOF' /usr/local/bin/docker-entrypoint.sh
#!/bin/sh
set -e

# Function to handle graceful shutdown
graceful_shutdown() {
    echo "Received shutdown signal, stopping nginx gracefully..."
    nginx -s quit
    exit 0
}

# Set up signal handlers
trap graceful_shutdown SIGTERM SIGINT

# Validate nginx configuration before starting
echo "Validating nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid"
else
    echo "Nginx configuration is invalid, exiting..."
    exit 1
fi

# Start nginx in background
echo "Starting nginx..."
nginx -g "daemon off;" &

# Store nginx PID
NGINX_PID=$!

# Wait for nginx to start
sleep 2

# Health check to ensure nginx is running
if ! curl -f http://localhost/health > /dev/null 2>&1; then
    echo "Health check failed, nginx may not be running properly"
    exit 1
fi

echo "Nginx started successfully with PID: $NGINX_PID"

# Keep the script running and wait for nginx
wait $NGINX_PID
EOF

# Make the startup script executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create health check script
COPY <<'EOF' /usr/local/bin/healthcheck.sh
#!/bin/sh
# Health check script for container monitoring

# Check if nginx process is running
if ! pgrep nginx > /dev/null; then
    echo "Nginx process not found"
    exit 1
fi

# Check if nginx is responding to HTTP requests
if ! wget --quiet --tries=1 --spider http://localhost/health; then
    echo "Nginx health endpoint not responding"
    exit 1
fi

echo "Health check passed"
exit 0
EOF

RUN chmod +x /usr/local/bin/healthcheck.sh

# Expose port 80 for HTTP traffic
EXPOSE 80

# Optional: Expose port 443 for HTTPS (uncomment if using SSL)
# EXPOSE 443

# Add health check for container orchestration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh

# Security: Don't run as root
USER nginx

# Set working directory
WORKDIR /usr/share/nginx/html

# Use custom entrypoint for better process management
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command (will be executed by entrypoint)
CMD ["nginx", "-g", "daemon off;"]

# Build-time environment variables (can be overridden)
ARG BUILD_DATE
ARG VERSION=1.0

# Runtime environment variables
ENV NGINX_WORKER_PROCESSES=auto
ENV NGINX_WORKER_CONNECTIONS=1024
ENV NGINX_KEEPALIVE_TIMEOUT=65

# Add labels for better image management
LABEL org.opencontainers.image.created=$BUILD_DATE
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.title="Lightweight Modern Web App"
LABEL org.opencontainers.image.description="A modern, lightweight web application running on nginx in Alpine Linux"
LABEL org.opencontainers.image.source="https://github.com/yourusername/your-repo"