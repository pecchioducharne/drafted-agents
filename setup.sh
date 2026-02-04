#!/bin/bash

set -e

echo "🚀 Setting up Drafted Agents monorepo..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Prerequisites check passed"

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual API keys and tokens"
else
    echo "✅ .env file already exists"
fi

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install MCP server dependencies
echo "📦 Installing MCP server dependencies..."
for server in mcp/*-server; do
    if [ -f "$server/package.json" ]; then
        echo "  → Installing dependencies for $(basename $server)..."
        (cd "$server" && npm install)
    fi
done

# Install UI dependencies
echo "📦 Installing UI dependencies..."
(cd apps/ui && npm install)

# Build sandbox image
echo "🏗️  Building OpenHands sandbox image..."
docker build -t drafted/agent-sandbox:latest -f runtimes/openhands/Dockerfile.sandbox runtimes/openhands

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your actual API keys and tokens"
echo "2. Run 'cd infra && docker-compose up -d' to start the infrastructure"
echo "3. Access the services:"
echo "   - Temporal UI: http://localhost:8080"
echo "   - Qdrant: http://localhost:6333"
echo "   - OpenHands: http://localhost:8000"
echo "   - Orchestrator API: http://localhost:8001"
echo "   - Agent UI: http://localhost:3000 (run 'cd apps/ui && npm run dev')"
echo ""
