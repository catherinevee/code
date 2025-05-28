# Architecture Overview

## System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │────│  Docker Container│────│     Nginx       │
│   (Optional)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Static Files   │
                       │  (HTML/CSS/JS)  │
                       └─────────────────┘
```

## Key Features

1. **Container-based Deployment**: Uses Docker for consistent deployment
2. **Nginx Web Server**: High-performance static file serving
3. **Security Hardening**: Read-only filesystem, non-root user
4. **Health Monitoring**: Built-in health checks and monitoring
5. **Resource Optimization**: Memory and CPU limits

## Performance Characteristics

- **Image Size**: ~50MB (Alpine Linux base)
- **Memory Usage**: ~64MB typical, 128MB limit
- **CPU Usage**: Minimal, burst capable
- **Response Time**: <100ms for static content
- **Throughput**: 1000+ requests/second (single container)

## Security Features

- Non-root container execution
- Read-only root filesystem
- Security headers (CSP, HSTS, etc.)
- Rate limiting
- No unnecessary privileges
