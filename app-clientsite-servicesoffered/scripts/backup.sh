#!/bin/bash
# Backup script for webapp data

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup..."

# Backup logs
if [[ -d "./logs" ]]; then
    tar -czf "$BACKUP_DIR/logs_$TIMESTAMP.tar.gz" ./logs/
    echo "✅ Logs backed up"
fi

# Backup container if running
CONTAINER_NAME="modern-webapp-prod"
if docker ps -q -f name=$CONTAINER_NAME > /dev/null; then
    docker export $CONTAINER_NAME > "$BACKUP_DIR/container_$TIMESTAMP.tar"
    echo "✅ Container backed up"
fi

echo "🎉 Backup completed: $BACKUP_DIR/"
ls -la "$BACKUP_DIR/"
