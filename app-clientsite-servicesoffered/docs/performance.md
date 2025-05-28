# Performance Tuning Guide

## Nginx Optimizations

### Worker Process Configuration
```nginx
worker_processes auto;
worker_connections 1024;
```

### Caching Strategy
- Static files: 1 year cache
- HTML files: 1 hour cache
- API responses: No cache or short TTL

### Compression
- Gzip enabled for text files
- Compression level 6 (optimal balance)
- Minimum file size: 1KB

## Docker Optimizations

### Resource Limits
```yaml
services:
  webapp:
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: '0.5'
        reservations:
          memory: 64M
          cpus: '0.25'
```

### Multi-stage Builds
- Build stage: Process assets
- Production stage: Minimal runtime

## Monitoring Metrics

### Key Performance Indicators
- Response time < 100ms
- Memory usage < 128MB
- CPU usage < 50%
- Error rate < 0.1%

### Monitoring Commands
```bash
# Real-time stats
docker stats modern-webapp-prod

# Response time test
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/

# Load testing
ab -n 1000 -c 10 http://localhost:8080/
```

## Optimization Checklist

- [ ] Gzip compression enabled
- [ ] Static file caching configured
- [ ] Resource limits set
- [ ] Health checks working
- [ ] Logs rotated
- [ ] Security headers present
- [ ] SSL/TLS configured (production)
- [ ] CDN configured (if applicable)
