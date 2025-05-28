# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 128MB available RAM
- 100MB available disk space

## Production Deployment

### Method 1: Automated Script
```bash
./deploy.sh --env production --port 80
```

### Method 2: Docker Compose
```bash
docker-compose up -d --build
```

### Method 3: Manual Docker
```bash
docker build -t modern-webapp .
docker run -d --name webapp -p 80:80 modern-webapp
```

## Environment-Specific Configurations

### Development
```bash
# Start development environment
./scripts/dev.sh

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Staging
```bash
# Deploy to staging
HOST_PORT=8080 ENVIRONMENT=staging ./deploy.sh
```

### Production
```bash
# Full production deployment with monitoring
ENABLE_MONITORING=true ./deploy.sh --env production
```

## Scaling

### Horizontal Scaling
```bash
# Scale to 3 instances
docker-compose up -d --scale webapp=3

# With load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Vertical Scaling
```bash
# Increase resource limits
docker update --memory=256m --cpus=1.0 modern-webapp-prod
```

## Monitoring

### Health Checks
```bash
curl http://localhost:8080/health
```

### Metrics
```bash
./monitor.sh metrics
```

### Logs
```bash
./monitor.sh logs
docker logs -f modern-webapp-prod
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find what's using the port
   lsof -i :8080
   
   # Use different port
   HOST_PORT=8081 ./deploy.sh
   ```

2. **Container won't start**
   ```bash
   # Check logs
   docker logs modern-webapp-prod
   
   # Validate nginx config
   docker run --rm modern-webapp nginx -t
   ```

3. **Performance issues**
   ```bash
   # Check resource usage
   docker stats modern-webapp-prod
   
   # Increase limits
   docker update --memory=256m modern-webapp-prod
   ```
