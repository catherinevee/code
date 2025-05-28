#!/bin/bash
# Quick start script for development

echo "🚀 Quick Start - Modern Webapp"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "Building and starting the application..."
docker-compose up -d --build

echo ""
echo "✅ Application started!"
echo "🌐 URL: http://localhost:8080"
echo "📝 Logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
