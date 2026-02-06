#!/bin/bash
# Drafted Brain - Startup Script

set -e

# Show ASCII banner
if [ -f wall.txt ]; then
    cat wall.txt
    echo ""
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                   🚀 Drafted Brain Startup                     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is running
echo "🔍 Checking Docker..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✅ Docker is running"
echo ""

# Check .env file
echo "🔍 Checking environment configuration..."
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Please create .env from .env.simple"
    exit 1
fi
echo "✅ .env file found"
echo ""

# Start services
echo "🚀 Starting services..."
docker compose -f docker-compose.simple.yml up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check service status
echo ""
echo "📊 Service Status:"
docker compose -f docker-compose.simple.yml ps

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                    ✅ System is Running!                       ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Services:"
echo "   • API:       http://localhost:7001"
echo "   • OpenHands: http://localhost:8000"
echo "   • Redis:     localhost:6379"
echo ""
echo "📝 Quick Commands:"
echo "   • Check health:  drafted health"
echo "   • Submit job:    drafted run \"Your task\""
echo "   • Check status:  drafted status <job_id>"
echo "   • View logs:     drafted logs <job_id>"
echo "   • List jobs:     drafted list"
echo ""
echo "📚 Documentation:"
echo "   • Getting Started: START_HERE.md"
echo "   • Quick Reference: QUICK_REFERENCE.md"
echo ""
echo "💡 Try a test job:"
echo "   drafted run \"Hello, test the system\""
echo ""
