#!/bin/bash
# Development mode with live reload

echo "🔧 Starting Development Mode"
echo ""

# Use override compose file for development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

