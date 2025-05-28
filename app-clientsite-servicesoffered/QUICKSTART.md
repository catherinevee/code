# 🚀 Quick Start Guide

## One-Command Setup

```bash
# Download and run setup
curl -sSL https://your-repo.com/setup.sh | bash

# Or if you have the files locally
./setup.sh
```

## Immediate Start

```bash
# Quick start (development)
./scripts/quickstart.sh

# Production deployment
./deploy.sh
```

## Access Your Application

- **Development**: http://localhost:3000
- **Production**: http://localhost:8080
- **Health Check**: /health endpoint

## Management Commands

```bash
# Monitor status
./monitor.sh

# View logs
./monitor.sh logs

# Run tests
./tests/test_webapp.sh

# Backup data
./scripts/backup.sh
```

## File Structure

```
modern-webapp/
├── index.html              # Main application
├── nginx.conf             # Web server config
├── Dockerfile             # Container definition
├── docker-compose.yml     # Orchestration
├── deploy.sh              # Deployment script
├── monitor.sh             # Monitoring tools
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
├── logs/                  # Application logs
└── backups/               # Backup storage
```

## Next Steps

1. **Customize**: Edit `index.html` for your content
2. **Configure**: Modify `nginx.conf` for your needs
3. **Deploy**: Use `./deploy.sh` for production
4. **Monitor**: Set up monitoring with `./monitor.sh monitor`
5. **Scale**: Use `docker-compose up --scale webapp=3`

## Support

- 📖 Full docs: See `docs/` directory
- 🐛 Issues: Check logs with `./monitor.sh logs`
- 🔧 Config: All settings in config files
- 📊 Metrics: Use `./monitor.sh metrics`

**Ready to go in under 2 minutes!** 🎉
