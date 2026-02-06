#!/bin/bash
# Drafted Brain - Shutdown Script

# Show ASCII banner
if [ -f wall.txt ]; then
    cat wall.txt
    echo ""
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                   🛑 Drafted Brain Shutdown                    ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "🛑 Stopping services..."
docker compose -f docker-compose.simple.yml down

echo ""
echo "✅ All services stopped"
echo ""
echo "💡 To start again:"
echo "   ./start.sh"
echo ""
