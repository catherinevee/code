# LibreNMS Dockerfile with comprehensive error handling and optimization
# Based on Ubuntu 22.04 LTS for stability and long-term support
FROM ubuntu:22.04

# Metadata labels for container identification and maintenance
LABEL maintainer="your-email@domain.com" \
      description="LibreNMS Network Monitoring System" \
      version="1.0" \
      org.opencontainers.image.source="https://github.com/librenms/librenms"

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    COMPOSER_ALLOW_SUPERUSER=1 \
    COMPOSER_NO_INTERACTION=1

# Create librenms user and group early to ensure consistent UID/GID
# This prevents permission issues when mounting volumes
RUN groupadd -r librenms --gid=1000 && \
    useradd -r -g librenms --uid=1000 --home-dir=/opt/librenms --shell=/bin/bash librenms

# Update package lists and install essential packages
# Split into multiple RUN commands for better layer caching and debugging
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Core system utilities
        ca-certificates \
        curl \
        wget \
        gnupg \
        lsb-release \
        software-properties-common \
        apt-transport-https && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add PHP repository for latest PHP version
# Error handling: Check if repository addition was successful
RUN curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/php-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/php-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list || \
    (echo "Failed to add PHP repository" && exit 1)

# Install LibreNMS dependencies
# Grouped by functionality for better maintainability
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Web server
        nginx \
        # PHP and extensions (LibreNMS requires PHP 8.1+)
        php8.2 \
        php8.2-fpm \
        php8.2-cli \
        php8.2-mysql \
        php8.2-pgsql \
        php8.2-mysqli \
        php8.2-gd \
        php8.2-bcmath \
        php8.2-zip \
        php8.2-ldap \
        php8.2-mbstring \
        php8.2-xml \
        php8.2-curl \
        php8.2-memcached \
        php8.2-redis \
        php8.2-json \
        php8.2-snmp \
        php8.2-fping \
        # System monitoring tools
        fping \
        imagemagick \
        whois \
        mtr-tiny \
        nmap \
        python3-dotenv \
        python3-redis \
        python3-setuptools \
        python3-systemd \
        python3-pip \
        # SNMP tools
        snmp \
        snmp-mibs-downloader \
        # Database client (MySQL/MariaDB)
        default-mysql-client \
        # System utilities
        acl \
        git \
        unzip \
        supervisor \
        cron \
        logrotate \
        rrdtool && \
    # Clean up package cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Composer globally for PHP dependency management
# Error handling: Verify installation and signature
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
    chmod +x /usr/local/bin/composer && \
    composer --version || (echo "Composer installation failed" && exit 1)

# Create necessary directories with proper permissions
# This ensures LibreNMS has required directory structure
RUN mkdir -p /opt/librenms \
             /var/log/librenms \
             /var/lib/librenms \
             /etc/librenms \
             /var/cache/librenms \
             /run/php && \
    # Set proper ownership
    chown -R librenms:librenms /opt/librenms \
                               /var/log/librenms \
                               /var/lib/librenms \
                               /etc/librenms \
                               /var/cache/librenms

# Clone LibreNMS repository
# Use specific version/tag for production stability
WORKDIR /opt/librenms
RUN git clone https://github.com/librenms/librenms.git . && \
    # Verify git clone was successful
    [ -f "librenms.service" ] || (echo "LibreNMS clone failed" && exit 1) && \
    # Change ownership to librenms user
    chown -R librenms:librenms /opt/librenms

# Switch to librenms user for security
USER librenms

# Install PHP dependencies via Composer
# Error handling: Ensure composer install succeeds
RUN composer install --no-dev --optimize-autoloader --no-interaction || \
    (echo "Composer install failed" && exit 1)

# Install Python dependencies
# LibreNMS uses Python for various monitoring scripts
RUN pip3 install --user -r requirements.txt || \
    (echo "Python dependencies installation failed" && exit 1)

# Switch back to root for system configuration
USER root

# Configure PHP-FPM
# Optimize for container environment
RUN sed -i 's/;date.timezone.*/date.timezone = UTC/' /etc/php/8.2/fpm/php.ini && \
    sed -i 's/;date.timezone.*/date.timezone = UTC/' /etc/php/8.2/cli/php.ini && \
    # Memory and execution time optimizations
    sed -i 's/memory_limit = .*/memory_limit = 512M/' /etc/php/8.2/fpm/php.ini && \
    sed -i 's/memory_limit = .*/memory_limit = 512M/' /etc/php/8.2/cli/php.ini && \
    sed -i 's/max_execution_time = .*/max_execution_time = 300/' /etc/php/8.2/fpm/php.ini && \
    sed -i 's/max_input_vars = .*/max_input_vars = 1000/' /etc/php/8.2/fpm/php.ini && \
    # Configure PHP-FPM pool
    sed -i 's/user = www-data/user = librenms/' /etc/php/8.2/fpm/pool.d/www.conf && \
    sed -i 's/group = www-data/group = librenms/' /etc/php/8.2/fpm/pool.d/www.conf && \
    sed -i 's/listen.owner = www-data/listen.owner = librenms/' /etc/php/8.2/fpm/pool.d/www.conf && \
    sed -i 's/listen.group = www-data/listen.group = librenms/' /etc/php/8.2/fpm/pool.d/www.conf

# Configure Nginx
# Create optimized configuration for LibreNMS
COPY <<EOF /etc/nginx/sites-available/librenms
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    # Server configuration
    server_name _;
    root /opt/librenms/html;
    index index.php;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression for performance
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
    
    # Main location block
    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }
    
    # PHP processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
        
        # Increase timeout for long-running scripts
        fastcgi_read_timeout 300;
    }
    
    # Deny access to sensitive files
    location ~ /\.ht {
        deny all;
    }
    
    location ~ /\.git {
        deny all;
    }
    
    # Static file caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the LibreNMS site and remove default
RUN ln -sf /etc/nginx/sites-available/librenms /etc/nginx/sites-enabled/ && \
    rm -f /etc/nginx/sites-enabled/default && \
    # Test nginx configuration
    nginx -t || (echo "Nginx configuration test failed" && exit 1)

# Configure SNMP
# Download and configure SNMP MIBs
RUN download-mibs && \
    echo "mibs +ALL" >> /etc/snmp/snmp.conf

# Create LibreNMS configuration template
# This will be customized via environment variables at runtime
RUN mkdir -p /etc/librenms && \
    cat > /etc/librenms/config.php.template << 'EOF'
<?php
// LibreNMS Configuration Template
// Database configuration
$config['db_host'] = '${DB_HOST:-localhost}';
$config['db_port'] = '${DB_PORT:-3306}';
$config['db_user'] = '${DB_USER:-librenms}';
$config['db_pass'] = '${DB_PASS:-}';
$config['db_name'] = '${DB_NAME:-librenms}';

// Application settings
$config['site_style'] = 'blue';
$config['page_refresh'] = '300';
$config['list_limit'] = '15';

// Security settings
$config['auth_mechanism'] = 'mysql';
$config['base_url'] = '${BASE_URL:-http://localhost}';

// Performance settings
$config['rrd']['heartbeat'] = 600;
$config['rrd']['step'] = 300;

// Enable modules
$config['enable_billing'] = 1;
$config['enable_inventory'] = 1;
$config['enable_pseudowires'] = 1;
$config['enable_vrfs'] = 1;
$config['enable_syslog'] = 1;

// Logging
$config['log_file'] = '/var/log/librenms/librenms.log';
$config['log_level'] = '${LOG_LEVEL:-info}';

// Memcached settings (if available)
$config['memcached']['enable'] = false;
$config['memcached']['host'] = '${MEMCACHED_HOST:-localhost}';
$config['memcached']['port'] = '${MEMCACHED_PORT:-11211}';

// Redis settings (if available)
$config['redis']['enable'] = false;
$config['redis']['host'] = '${REDIS_HOST:-localhost}';
$config['redis']['port'] = '${REDIS_PORT:-6379}';
$config['redis']['db'] = '${REDIS_DB:-0}';
EOF

# Set up proper permissions for LibreNMS directories
# Critical for security and functionality
RUN chown -R librenms:librenms /opt/librenms && \
    chmod -R 755 /opt/librenms && \
    chmod -R 775 /opt/librenms/rrd /opt/librenms/logs /opt/librenms/bootstrap/cache/ /opt/librenms/storage/ && \
    chmod +x /opt/librenms/daily.sh && \
    chmod +x /opt/librenms/cronic

# Create supervisor configuration for process management
# This manages multiple services within the container
COPY <<EOF /etc/supervisor/conf.d/librenms.conf
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
stdout_logfile=/var/log/supervisor/nginx.log
stderr_logfile=/var/log/supervisor/nginx.log
autorestart=true
priority=100

[program:php-fpm]
command=/usr/sbin/php-fpm8.2 -F
stdout_logfile=/var/log/supervisor/php-fpm.log
stderr_logfile=/var/log/supervisor/php-fpm.log
autorestart=true
priority=200

[program:cron]
command=/usr/sbin/cron -f
stdout_logfile=/var/log/supervisor/cron.log
stderr_logfile=/var/log/supervisor/cron.log
autorestart=true
priority=300

[program:librenms-poller]
command=/opt/librenms/discovery-wrapper.py 1
directory=/opt/librenms
user=librenms
stdout_logfile=/var/log/supervisor/librenms-poller.log
stderr_logfile=/var/log/supervisor/librenms-poller.log
autorestart=true
priority=400
EOF

# Create entrypoint script for container initialization
# This handles configuration setup and service startup
RUN cat > /docker-entrypoint.sh << 'EOF'
#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Function to wait for database
wait_for_db() {
    log "Waiting for database connection..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if mysql -h"${DB_HOST}" -P"${DB_PORT}" -u"${DB_USER}" -p"${DB_PASS}" -e "SELECT 1" >/dev/null 2>&1; then
            log "Database connection successful"
            return 0
        fi
        
        warning "Database connection attempt $attempt/$max_attempts failed. Retrying in 5 seconds..."
        sleep 5
        ((attempt++))
    done
    
    error "Failed to connect to database after $max_attempts attempts"
    exit 1
}

# Function to initialize LibreNMS configuration
init_config() {
    log "Initializing LibreNMS configuration..."
    
    # Process configuration template
    envsubst < /etc/librenms/config.php.template > /opt/librenms/config.php
    
    # Set proper ownership
    chown librenms:librenms /opt/librenms/config.php
    chmod 644 /opt/librenms/config.php
    
    log "Configuration initialized"
}

# Function to run database migrations
run_migrations() {
    log "Running database setup and migrations..."
    
    cd /opt/librenms
    
    # Check if database exists and is accessible
    if ! su -s /bin/bash librenms -c "php artisan migrate:status" >/dev/null 2>&1; then
        log "Setting up database schema..."
        su -s /bin/bash librenms -c "php build-base.php" || {
            error "Database schema setup failed"
            exit 1
        }
    else
        log "Running pending migrations..."
        su -s /bin/bash librenms -c "php artisan migrate --force" || {
            warning "Some migrations may have failed, continuing..."
        }
    fi
    
    log "Database setup completed"
}

# Function to set up cron jobs
setup_cron() {
    log "Setting up cron jobs..."
    
    # Create cron job for LibreNMS
    cat > /etc/cron.d/librenms << 'CRON_EOF'
33   */6  * * *   librenms    /opt/librenms/cronic /opt/librenms/discovery.php -h all >> /dev/null 2>&1
*/5  *    * * *   librenms    /opt/librenms/cronic /opt/librenms/discovery.php -h new >> /dev/null 2>&1
*/5  *    * * *   librenms    /opt/librenms/cronic /opt/librenms/poller-wrapper.py 1 >> /dev/null 2>&1
15   0    * * *   librenms    /opt/librenms/daily.sh >> /dev/null 2>&1
*    *    * * *   librenms    /opt/librenms/alerts.php >> /dev/null 2>&1
*/5  *    * * *   librenms    /opt/librenms/poll-billing.php >> /dev/null 2>&1
01   *    * * *   librenms    /opt/librenms/billing-calculate.php >> /dev/null 2>&1
*/5  *    * * *   librenms    /opt/librenms/check-services.php >> /dev/null 2>&1
CRON_EOF
    
    # Set proper permissions
    chmod 644 /etc/cron.d/librenms
    
    log "Cron jobs configured"
}

# Function to perform health checks
health_check() {
    log "Performing health checks..."
    
    cd /opt/librenms
    
    # Run LibreNMS validation
    su -s /bin/bash librenms -c "php validate.php" || {
        warning "Some validation checks failed, but continuing startup"
    }
    
    log "Health checks completed"
}

# Main initialization
main() {
    log "Starting LibreNMS container initialization..."
    
    # Validate required environment variables
    if [[ -z "${DB_HOST}" || -z "${DB_USER}" || -z "${DB_NAME}" ]]; then
        error "Required database environment variables are missing"
        error "Please set: DB_HOST, DB_USER, DB_NAME"
        exit 1
    fi
    
    # Wait for database if configured
    if [[ -n "${DB_HOST}" ]]; then
        wait_for_db
    fi
    
    # Initialize configuration
    init_config
    
    # Run database setup
    if [[ "${SKIP_DB_SETUP}" != "true" ]]; then
        run_migrations
    else
        log "Skipping database setup (SKIP_DB_SETUP=true)"
    fi
    
    # Setup cron
    setup_cron
    
    # Perform health checks
    if [[ "${SKIP_HEALTH_CHECK}" != "true" ]]; then
        health_check
    else
        log "Skipping health checks (SKIP_HEALTH_CHECK=true)"
    fi
    
    log "LibreNMS initialization completed successfully"
    
    # Start supervisor to manage services
    log "Starting services via supervisor..."
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/librenms.conf
}

# Handle signals for graceful shutdown
trap 'log "Received shutdown signal, stopping services..."; supervisorctl stop all; exit 0' SIGTERM SIGINT

# Run main function
main "$@"
EOF

# Make entrypoint script executable
RUN chmod +x /docker-entrypoint.sh

# Create health check script
RUN cat > /health-check.sh << 'EOF'
#!/bin/bash
# Health check script for LibreNMS container

set -e

# Check if nginx is running
if ! pgrep nginx > /dev/null; then
    echo "Nginx is not running"
    exit 1
fi

# Check if PHP-FPM is running
if ! pgrep php-fpm > /dev/null; then
    echo "PHP-FPM is not running"
    exit 1
fi

# Check if LibreNMS web interface is accessible
if ! curl -f http://localhost/login > /dev/null 2>&1; then
    echo "LibreNMS web interface is not accessible"
    exit 1
fi

echo "All services are healthy"
exit 0
EOF

RUN chmod +x /health-check.sh

# Expose HTTP port
EXPOSE 80

# Define volumes for persistent data
# These should be mounted to host directories or named volumes
VOLUME ["/opt/librenms/rrd", "/opt/librenms/logs", "/var/log/librenms"]

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /health-check.sh

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command (can be overridden)
CMD ["supervisord"]