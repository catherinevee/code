#!/bin/sh

# Entrypoint script for nginx container
# Handles initialization, configuration validation, and graceful startup

set -e  # Exit on any error

# Color codes for better logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to handle graceful shutdown
cleanup() {
    log_info "Received shutdown signal, stopping nginx gracefully..."
    nginx -s quit
    exit 0
}

# Trap SIGTERM and SIGINT for graceful shutdown
trap cleanup TERM INT

# Startup banner
echo "=================================================="
echo "🌸 Cute Website Container Starting 🌸"
echo "=================================================="

# Validate required files exist
log_info "Validating configuration files..."

required_files="/etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf /usr/share/nginx/html/index.html"
for file in $required_files; do
    if [ ! -f "$file" ]; then
        log_error "Required file missing: $file"
        exit 1
    fi
done

log_success "All required files found"

# Test nginx configuration
log_info "Testing nginx configuration..."
if nginx -t; then
    log_success "Nginx configuration is valid"
else
    log_error "Nginx configuration test failed"
    exit 1
fi

# Create necessary directories if they don't exist
log_info "Creating runtime directories..."
mkdir -p /var/log/nginx /var/cache/nginx /var/run

# Set proper permissions (already done in Dockerfile, but double-check)
if [ -w /var/log/nginx ] && [ -w /var/cache/nginx ]; then
    log_success "Directory permissions are correct"
else
    log_warning "Some directory permissions may be incorrect"
fi

# Display container information
log_info "Container Information:"
echo "  - User: $(id)"
echo "  - Working Directory: $(pwd)"
echo "  - Nginx Version: $(nginx -v 2>&1)"
echo "  - Process ID: $"

# Check if website files exist and display some stats
if [ -f "/usr/share/nginx/html/index.html" ]; then
    file_size=$(wc -c < /usr/share/nginx/html/index.html)
    log_info "Website file size: ${file_size} bytes"
fi

# Environment variable handling
log_info "Environment Configuration:"
echo "  - Timezone: ${TZ:-Not set}"
echo "  - Worker Processes: ${NGINX_WORKER_PROCESSES:-auto}"
echo "  - Worker Connections: ${NGINX_WORKER_CONNECTIONS:-1024}"

# Final startup message
log_success "Container initialization complete!"
log_info "Starting nginx server on port 8080..."
echo "=================================================="
echo "🚀 Cute Website is ready! 🚀"
echo "Health check: http://localhost:8080/health"
echo "Website: http://localhost:8080"
echo "=================================================="

# Execute the main command (nginx)
exec "$@"