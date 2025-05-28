#!/bin/bash
# deploy.sh - Production deployment script

set -e  # Exit on any error

echo "🚀 Starting deployment of Modern Webapp..."

# Configuration
IMAGE_NAME="modern-webapp"
CONTAINER_NAME="modern-webapp-prod"
HOST_PORT="80"
VERSION=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    log_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create logs directory
mkdir -p ./logs
chmod 755 ./logs

# Build the image
log_info "Building Docker image..."
docker build \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VERSION=$VERSION \
    -t $IMAGE_NAME:$VERSION \
    -t $IMAGE_NAME:latest \
    .

# Stop existing container if running
if docker ps -q -f name=$CONTAINER_NAME > /dev/null; then
    log_warn "Stopping existing container..."
    docker stop $CONTAINER_NAME
fi

# Remove existing container
if docker ps -aq -f name=$CONTAINER_NAME > /dev/null; then
    log_warn "Removing existing container..."
    docker rm $CONTAINER_NAME
fi

# Run new container
log_info "Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    -p $HOST_PORT:80 \
    --restart unless-stopped \
    --memory=128m \
    --cpus=0.5 \
    -v $(pwd)/logs:/var/log/nginx \
    --read-only \
    --tmpfs /tmp \
    --tmpfs /var/run \
    --tmpfs /var/cache/nginx \
    --security-opt no-new-privileges:true \
    $IMAGE_NAME:latest

# Wait for container to be healthy
log_info "Waiting for container to be healthy..."
timeout=60
counter=0

while [ $counter -lt $timeout ]; do
    if docker exec $CONTAINER_NAME /usr/local/bin/healthcheck.sh > /dev/null 2>&1; then
        log_info "Container is healthy!"
        break
    fi
    
    sleep 2
    counter=$((counter + 2))
    
    if [ $counter -ge $timeout ]; then
        log_error "Container failed to become healthy within $timeout seconds"
        docker logs $CONTAINER_NAME
        exit 1
    fi
done

# Display status
log_info "Deployment completed successfully!"
echo ""
echo "📊 Container Status:"
docker ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "🌐 Application URL: http://localhost:$HOST_PORT"
echo "📝 Logs: docker logs $CONTAINER_NAME"
echo "🔍 Monitor: docker stats $CONTAINER_NAME"

# Optional: Clean up old images
read -p "Do you want to clean up old Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Cleaning up old images..."
    docker image prune -f
fi

echo "✅ Deployment complete!"
```

### Health Monitoring

```bash
# Check container health
docker exec modern-webapp /usr/local/bin/healthcheck.sh

# View logs
docker logs modern-webapp -f

# Monitor resource usage
docker stats modern-webapp
```

## 🔒 Security Features

- **CSP Headers**: Content Security Policy protection
- **Rate Limiting**: DDoS protection with nginx
- **Security Headers**: XSS, CSRF, and clickjacking protection
- **Non-root User**: Container runs as nginx user
- **Read-only Filesystem**: Immutable container filesystem
- **No New Privileges**: Prevents privilege escalation

## 📊 Performance Optimizations

- **Gzip Compression**: Reduces bandwidth usage by ~70%
- **Static File Caching**: Browser caching for 1 year
- **HTTP/2 Ready**: Nginx configured for HTTP/2
- **Resource Limits**: Container memory and CPU limits
- **Efficient File Serving**: sendfile and tcp_nopush enabled

## 🧪 Testing

### Manual Testing

```bash
# Test main page
curl -I http://localhost:8080/

# Test health endpoint
curl http://localhost:8080/health

# Test 404 handling
curl -I http://localhost:8080/nonexistent

# Test compression
curl -H "Accept-Encoding: gzip" -I http://localhost:8080/
```

### Load Testing

```bash
# Using Apache Bench (install with: apt-get install apache2-utils)
ab -n 1000 -c 10 http://localhost:8080/

# Using curl for simple test
for i in {1..100}; do
    curl -s http://localhost:8080/ > /dev/null
    echo "Request $i completed"
done
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8080
   
   # Use different port
   docker run -p 8081:80 modern-webapp
   ```

2. **Container won't start**
   ```bash
   # Check logs
   docker logs modern-webapp
   
   # Test nginx config
   docker run --rm modern-webapp nginx -t
   ```

3. **Health check failing**
   ```bash
   # Check container status
   docker inspect modern-webapp --format='{{.State.Health.Status}}'
   
   # Manual health check
   docker exec modern-webapp curl -f http://localhost/health
   ```

### Log Locations

- **Access logs**: `./logs/access.log`
- **Error logs**: `./logs/error.log`
- **Container logs**: `docker logs modern-webapp`

## 📈 Monitoring & Metrics

### Basic Monitoring

```bash
# Real-time container stats
docker stats modern-webapp

# Resource usage over time
docker exec modern-webapp top

# Disk usage
docker exec modern-webapp df -h
```

### Advanced Monitoring (Optional)

Uncomment monitoring services in `docker-compose.yml`:

- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization  
- **Fluentd**: Log aggregation

## 🔄 Updates & Maintenance

### Rolling Updates

```bash
# Build new version
docker build -t modern-webapp:v2 .

# Test new version
docker run -d --name webapp-test -p 8081:80 modern-webapp:v2

# Switch to new version (zero-downtime)
./deploy.sh
```

### Backup & Restore

```bash
# Backup logs
tar -czf webapp-logs-$(date +%Y%m%d).tar.gz logs/

# Export container
docker export modern-webapp > webapp-backup.tar
```

## 📄 License

MIT License - feel free to use this in your projects!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- **Issues**: Create an issue in the repository
- **Documentation**: Check this README
- **Logs**: Always check `docker logs modern-webapp` first

---

**Built with ❤️ for performance, security, and accessibility**