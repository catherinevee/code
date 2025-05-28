# Oxidized Network Configuration Backup Dockerfile
# Based on Alpine Linux for minimal footprint and security
FROM alpine:3.19

# Metadata labels for container identification and maintenance
LABEL maintainer="your-email@domain.com" \
      description="Oxidized Network Device Configuration Backup Tool" \
      version="1.0" \
      org.opencontainers.image.source="https://github.com/ytti/oxidized"

# Set environment variables
ENV OXIDIZED_HOME=/home/oxidized \
    OXIDIZED_LOGS=/home/oxidized/.config/oxidized/logs \
    OXIDIZED_CONFIG=/home/oxidized/.config/oxidized \
    PATH="$PATH:/home/oxidized/.local/bin" \
    GEM_HOME="/home/oxidized/.local/share/gem" \
    GEM_PATH="/home/oxidized/.local/share/gem"

# Create oxidized user and group for security
# Use consistent UID/GID to prevent permission issues with volumes
RUN addgroup -g 1000 -S oxidized && \
    adduser -u 1000 -S oxidized -G oxidized -h /home/oxidized -s /bin/bash

# Install system dependencies and build tools
# Split into logical groups for better layer caching
RUN apk update && \
    apk add --no-cache \
        # Core system utilities
        bash \
        ca-certificates \
        curl \
        wget \
        git \
        openssh-client \
        # Ruby and build dependencies
        ruby \
        ruby-dev \
        ruby-bundler \
        ruby-json \
        # Build tools for native gems
        build-base \
        libffi-dev \
        openssl-dev \
        cmake \
        # Network tools for device communication
        net-snmp-tools \
        sshpass \
        expect \
        telnet \
        # Process management
        supervisor \
        # Log rotation
        logrotate && \
    # Clean up package cache to reduce image size
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/*

# Create necessary directories with proper structure
RUN mkdir -p /home/oxidized/.config/oxidized \
             /home/oxidized/.config/oxidized/logs \
             /home/oxidized/.config/oxidized/configs \
             /home/oxidized/.local/bin \
             /home/oxidized/.local/share/gem \
             /var/log/oxidized \
             /var/run/oxidized && \
    # Set proper ownership
    chown -R oxidized:oxidized /home/oxidized \
                               /var/log/oxidized \
                               /var/run/oxidized

# Switch to oxidized user for gem installation (security best practice)
USER oxidized
WORKDIR /home/oxidized

# Create Gemfile for dependency management
# This allows for better control over gem versions and dependencies
RUN cat > Gemfile << 'EOF'
source 'https://rubygems.org'

# Core Oxidized gem
gem 'oxidized', '~> 0.28'

# Web interface
gem 'oxidized-web', '~> 0.13'

# Git support for configuration storage
gem 'rugged', '~> 1.0'

# Additional input/output methods
gem 'net-ssh', '~> 7.0'
gem 'net-telnet', '~> 0.2'

# HTTP API support
gem 'sinatra', '~> 3.0'
gem 'sinatra-contrib', '~> 3.0'

# Logging and utilities
gem 'logger', '~> 1.5'
gem 'chronic', '~> 0.10'

# Performance and reliability
gem 'concurrent-ruby', '~> 1.2'
EOF

# Install Ruby gems with error handling and optimization
RUN gem install bundler --user-install --no-document && \
    # Verify bundler installation
    bundle --version || (echo "Bundler installation failed" && exit 1) && \
    # Install gems with optimization flags
    bundle config set --local without 'development test' && \
    bundle config set --local deployment 'true' && \
    bundle config set --local jobs $(nproc) && \
    bundle install --retry=3 || (echo "Bundle install failed" && exit 1) && \
    # Clean up gem cache to reduce image size
    bundle clean --force && \
    rm -rf ~/.bundle/cache

# Switch back to root for system configuration
USER root

# Create default Oxidized configuration with comprehensive settings
RUN cat > /home/oxidized/.config/oxidized/config << 'EOF'
---
# Oxidized Configuration File
# This file contains the main configuration for Oxidized

# Username and password for device authentication
# These can be overridden by environment variables
username: ${OXIDIZED_USERNAME:-admin}
password: ${OXIDIZED_PASSWORD:-admin}

# Model definitions - specify which models to use for different device types
model_map:
  cisco: ios
  juniper: junos
  arista: eos
  cumulus: cumulus
  fortinet: fortios
  paloalto: panos
  checkpoint: gaia

# Interval between backups (in seconds)
interval: ${OXIDIZED_INTERVAL:-3600}

# Use syslog for logging
use_syslog: false

# Debug mode - set to true for verbose logging
debug: ${OXIDIZED_DEBUG:-false}

# Threads - number of concurrent backup threads
threads: ${OXIDIZED_THREADS:-30}

# Timeout settings
timeout: ${OXIDIZED_TIMEOUT:-20}
retries: ${OXIDIZED_RETRIES:-3}

# Prompt detection timeout
prompt: !ruby/regexp /^([\w.@-]+[#>]\s?)$/

# Next adds/removes
next_adds_job: false
next_removes_job: false

# Pidfile location
pid: /var/run/oxidized/oxidized.pid

# Crash directory for debugging
crash:
  directory: /home/oxidized/.config/oxidized/crashes
  hostnames: false

# Statistics
stats:
  history_size: 10

# Input method configuration
input:
  default: ssh, telnet
  debug: ${OXIDIZED_INPUT_DEBUG:-false}
  ssh:
    secure: false
    passive: ${OXIDIZED_SSH_PASSIVE:-true}
  ftp:
    passive: true
  utf8_encoded: true

# Output method - file system storage
output:
  default: file
  file:
    directory: /home/oxidized/.config/oxidized/configs

# Source configuration - where to get device list
source:
  default: csv
  csv:
    file: /home/oxidized/.config/oxidized/router.db
    delimiter: !ruby/regexp /[,;]/
    map:
      name: 0
      model: 1
      username: 2
      password: 3
    vars_map:
      enable: 4

# Web interface configuration
rest: ${OXIDIZED_WEB_HOST:-127.0.0.1}:${OXIDIZED_WEB_PORT:-8888}

# Logging configuration
log: /home/oxidized/.config/oxidized/logs/oxidized.log

# Model-specific configurations
models:
  ios:
    # Cisco IOS specific settings
    cmd: 'show version'
    cmd: 'show running-config'
    cfg: 'terminal length 0'
    cfg: 'terminal width 0'
  
  junos:
    # Juniper JunOS specific settings
    cmd: 'show version'
    cmd: 'show configuration | display set'
  
  eos:
    # Arista EOS specific settings
    cmd: 'show version'
    cmd: 'show running-config'

# Hooks for custom actions
hooks:
  # exec hook example - uncomment to enable
  # exec:
  #   type: exec
  #   events: [post_store]
  #   cmd: 'echo "Configuration backup completed for $OX_NODE_NAME"'
  
  # gitcrypt hook for encrypted git storage
  # gitcrypt:
  #   type: gitcrypt
  #   events: [post_store]
  #   repo: /home/oxidized/.config/oxidized/configs.git
EOF

# Create default router database template
RUN cat > /home/oxidized/.config/oxidized/router.db.template << 'EOF'
# Oxidized Router Database
# Format: hostname,model,username,password,enable_password
# Example entries (customize these for your environment):
# router1.example.com,ios,admin,password,enable_secret
# switch1.example.com,ios,admin,password,enable_secret
# firewall1.example.com,fortios,admin,password,
# Example with environment variable substitution:
${EXAMPLE_ROUTER_1:-router1.example.com,ios,admin,admin,enable}
${EXAMPLE_ROUTER_2:-switch1.example.com,ios,admin,admin,enable}
EOF

# Create logrotate configuration for log management
RUN cat > /etc/logrotate.d/oxidized << 'EOF'
/home/oxidized/.config/oxidized/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    su oxidized oxidized
}

/var/log/oxidized/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    su oxidized oxidized
}
EOF

# Create supervisor configuration for process management
RUN cat > /etc/supervisor/conf.d/oxidized.conf << 'EOF'
[supervisord]
nodaemon=true
user=root
logfile=/var/log/oxidized/supervisord.log
pidfile=/var/run/supervisord.pid
loglevel=info

[program:oxidized]
command=/home/oxidized/.local/bin/oxidized
directory=/home/oxidized
user=oxidized
group=oxidized
stdout_logfile=/var/log/oxidized/oxidized.log
stderr_logfile=/var/log/oxidized/oxidized-error.log
autorestart=true
priority=100
environment=HOME="/home/oxidized",GEM_HOME="/home/oxidized/.local/share/gem",GEM_PATH="/home/oxidized/.local/share/gem"

[program:oxidized-web]
command=/home/oxidized/.local/bin/oxidized-web
directory=/home/oxidized
user=oxidized
group=oxidized
stdout_logfile=/var/log/oxidized/oxidized-web.log
stderr_logfile=/var/log/oxidized/oxidized-web-error.log
autorestart=true
priority=200
environment=HOME="/home/oxidized",GEM_HOME="/home/oxidized/.local/share/gem",GEM_PATH="/home/oxidized/.local/share/gem"

[program:logrotate]
command=/usr/sbin/crond -f
stdout_logfile=/var/log/oxidized/cron.log
stderr_logfile=/var/log/oxidized/cron.log
autorestart=true
priority=300
EOF

# Create comprehensive entrypoint script
RUN cat > /docker-entrypoint.sh << 'EOF'
#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Function to validate configuration
validate_config() {
    log "Validating Oxidized configuration..."
    
    # Check if config file exists and is readable
    if [[ ! -r /home/oxidized/.config/oxidized/config ]]; then
        error "Configuration file not found or not readable"
        return 1
    fi
    
    # Check if router database exists
    if [[ ! -f /home/oxidized/.config/oxidized/router.db ]]; then
        warning "Router database not found, creating from template"
        envsubst < /home/oxidized/.config/oxidized/router.db.template > /home/oxidized/.config/oxidized/router.db
        chown oxidized:oxidized /home/oxidized/.config/oxidized/router.db
    fi
    
    # Validate that we have at least one router configured
    if [[ ! -s /home/oxidized/.config/oxidized/router.db ]] || ! grep -v '^#' /home/oxidized/.config/oxidized/router.db | grep -q '^[^[:space:]]'; then
        warning "No routers configured in router.db. Add devices to start backing up configurations."
    fi
    
    log "Configuration validation completed"
}

# Function to initialize directory structure
init_directories() {
    log "Initializing directory structure..."
    
    # Ensure all required directories exist with proper permissions
    local dirs=(
        "/home/oxidized/.config/oxidized"
        "/home/oxidized/.config/oxidized/logs"
        "/home/oxidized/.config/oxidized/configs"
        "/home/oxidized/.config/oxidized/crashes"
        "/var/log/oxidized"
        "/var/run/oxidized"
    )
    
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            info "Created directory: $dir"
        fi
    done
    
    # Set proper ownership
    chown -R oxidized:oxidized /home/oxidized /var/log/oxidized /var/run/oxidized
    
    log "Directory initialization completed"
}

# Function to process configuration template
process_config() {
    log "Processing configuration template..."
    
    # Create temporary config with environment variable substitution
    local temp_config="/tmp/oxidized_config"
    envsubst < /home/oxidized/.config/oxidized/config > "$temp_config"
    
    # Move processed config to final location
    mv "$temp_config" /home/oxidized/.config/oxidized/config
    chown oxidized:oxidized /home/oxidized/.config/oxidized/config
    
    log "Configuration processing completed"
}

# Function to setup SSH client configuration
setup_ssh() {
    log "Setting up SSH client configuration..."
    
    # Create SSH directory
    mkdir -p /home/oxidized/.ssh
    
    # Create SSH client configuration for better compatibility
    cat > /home/oxidized/.ssh/config << 'SSH_EOF'
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ConnectTimeout 10
    # Support for older devices
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc
    HostKeyAlgorithms +ssh-rsa,ssh-dss
    PubkeyAcceptedKeyTypes +ssh-rsa
SSH_EOF
    
    # Set proper permissions
    chown -R oxidized:oxidized /home/oxidized/.ssh
    chmod 700 /home/oxidized/.ssh
    chmod 600 /home/oxidized/.ssh/config
    
    log "SSH configuration completed"
}

# Function to perform pre-flight checks
preflight_checks() {
    log "Performing pre-flight checks..."
    
    # Check if oxidized binary is available
    if ! su -s /bin/bash oxidized -c "oxidized --version" >/dev/null 2>&1; then
        error "Oxidized binary not found or not executable"
        return 1
    fi
    
    # Check if required gems are installed
    local required_gems=("oxidized" "oxidized-web")
    for gem in "${required_gems[@]}"; do
        if ! su -s /bin/bash oxidized -c "gem list | grep -q $gem"; then
            error "Required gem '$gem' not found"
            return 1
        fi
    done
    
    # Test configuration syntax
    if ! su -s /bin/bash oxidized -c "oxidized --dry-run" >/dev/null 2>&1; then
        warning "Configuration validation failed, but continuing..."
    fi
    
    log "Pre-flight checks completed"
}

# Function to setup git repository (if requested)
setup_git_repo() {
    if [[ "${OXIDIZED_GIT_REPO}" == "true" ]]; then
        log "Setting up Git repository for configuration storage..."
        
        local git_dir="/home/oxidized/.config/oxidized/configs.git"
        
        if [[ ! -d "$git_dir" ]]; then
            su -s /bin/bash oxidized -c "git init --bare $git_dir" || {
                warning "Failed to initialize Git repository"
                return 1
            }
        fi
        
        # Update configuration to use Git output
        sed -i 's/default: file/default: git/' /home/oxidized/.config/oxidized/config
        
        log "Git repository setup completed"
    fi
}

# Function to display startup information
show_startup_info() {
    info "=========================================="
    info "Oxidized Network Configuration Backup"
    info "=========================================="
    info "Configuration: /home/oxidized/.config/oxidized/config"
    info "Router DB: /home/oxidized/.config/oxidized/router.db"
    info "Logs: /home/oxidized/.config/oxidized/logs/"
    info "Configs: /home/oxidized/.config/oxidized/configs/"
    info "Web Interface: http://localhost:${OXIDIZED_WEB_PORT:-8888}"
    info "=========================================="
    
    # Show configured devices count
    local device_count=0
    if [[ -f /home/oxidized/.config/oxidized/router.db ]]; then
        device_count=$(grep -c '^[^#]' /home/oxidized/.config/oxidized/router.db 2>/dev/null || echo "0")
    fi
    info "Configured devices: $device_count"
    info "=========================================="
}

# Function to handle graceful shutdown
graceful_shutdown() {
    log "Received shutdown signal, stopping services gracefully..."
    
    # Stop supervisor and all managed processes
    if command -v supervisorctl >/dev/null 2>&1; then
        supervisorctl stop all >/dev/null 2>&1 || true
    fi
    
    # Kill any remaining oxidized processes
    pkill -f oxidized >/dev/null 2>&1 || true
    
    log "Graceful shutdown completed"
    exit 0
}

# Main initialization function
main() {
    log "Starting Oxidized container initialization..."
    
    # Set up signal handlers for graceful shutdown
    trap graceful_shutdown SIGTERM SIGINT SIGQUIT
    
    # Initialize directory structure
    init_directories
    
    # Process configuration template
    process_config
    
    # Setup SSH configuration
    setup_ssh
    
    # Validate configuration
    validate_config || {
        error "Configuration validation failed"
        exit 1
    }
    
    # Setup git repository if requested
    setup_git_repo
    
    # Perform pre-flight checks
    preflight_checks || {
        error "Pre-flight checks failed"
        exit 1
    }
    
    # Show startup information
    show_startup_info
    
    log "Oxidized initialization completed successfully"
    
    # Check if we should run in daemon mode or one-shot
    if [[ "$1" == "once" ]]; then
        log "Running Oxidized in one-shot mode..."
        exec su -s /bin/bash oxidized -c "oxidized"
    elif [[ "$1" == "bash" ]]; then
        log "Starting interactive shell..."
        exec /bin/bash
    else
        log "Starting Oxidized services via supervisor..."
        exec /usr/bin/supervisord -c /etc/supervisor/conf.d/oxidized.conf
    fi
}

# Handle different run modes
case "$1" in
    "help"|"--help"|"-h")
        echo "Oxidized Docker Container"
        echo "Usage: docker run [options] oxidized [command]"
        echo ""
        echo "Commands:"
        echo "  (default)  Start Oxidized daemon with web interface"
        echo "  once       Run backup once and exit"
        echo "  bash       Start interactive shell"
        echo "  help       Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  OXIDIZED_USERNAME     - Default username for device login"
        echo "  OXIDIZED_PASSWORD     - Default password for device login"
        echo "  OXIDIZED_INTERVAL     - Backup interval in seconds (default: 3600)"
        echo "  OXIDIZED_THREADS      - Number of concurrent threads (default: 30)"
        echo "  OXIDIZED_TIMEOUT      - Connection timeout (default: 20)"
        echo "  OXIDIZED_WEB_HOST     - Web interface host (default: 127.0.0.1)"
        echo "  OXIDIZED_WEB_PORT     - Web interface port (default: 8888)"
        echo "  OXIDIZED_GIT_REPO     - Enable Git repository (true/false)"
        echo "  OXIDIZED_DEBUG        - Enable debug mode (true/false)"
        exit 0
        ;;
    *)
        # Run main initialization
        main "$@"
        ;;
esac
EOF

# Make entrypoint script executable
RUN chmod +x /docker-entrypoint.sh

# Create health check script
RUN cat > /health-check.sh << 'EOF'
#!/bin/bash
# Health check script for Oxidized container

set -e

# Function to check if a process is running
check_process() {
    local process_name="$1"
    if ! pgrep -f "$process_name" > /dev/null; then
        echo "$process_name is not running"
        return 1
    fi
    return 0
}

# Function to check web interface
check_web_interface() {
    local port="${OXIDIZED_WEB_PORT:-8888}"
    local host="${OXIDIZED_WEB_HOST:-127.0.0.1}"
    
    if ! curl -f -s "http://${host}:${port}/" > /dev/null 2>&1; then
        echo "Web interface is not accessible on ${host}:${port}"
        return 1
    fi
    return 0
}

# Function to check log files for errors
check_logs() {
    local log_file="/home/oxidized/.config/oxidized/logs/oxidized.log"
    
    if [[ -f "$log_file" ]]; then
        # Check for recent critical errors (last 10 lines)
        if tail -n 10 "$log_file" | grep -qi "fatal\|critical\|error.*failed"; then
            echo "Recent critical errors found in log file"
            return 1
        fi
    fi
    return 0
}

# Main health check
main() {
    echo "Performing Oxidized health check..."
    
    # Check if supervisor is running
    check_process "supervisord" || exit 1
    
    # Check if oxidized process is running
    check_process "oxidized" || exit 1
    
    # Check web interface (if enabled)
    if [[ "${OXIDIZED_WEB_DISABLE}" != "true" ]]; then
        check_web_interface || exit 1
    fi
    
    # Check for critical log errors
    check_logs || exit 1
    
    echo "All health checks passed"
    exit 0
}

# Run health check
main "$@"
EOF

RUN chmod +x /health-check.sh

# Set final ownership for all oxidized files
RUN chown -R oxidized:oxidized /home/oxidized

# Expose web interface port
EXPOSE 8888

# Define volumes for persistent data
# These should be mounted to preserve configurations and backups
VOLUME ["/home/oxidized/.config/oxidized/configs", "/home/oxidized/.config/oxidized/logs"]

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /health-check.sh

# Set working directory
WORKDIR /home/oxidized

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command
CMD ["supervisord"]