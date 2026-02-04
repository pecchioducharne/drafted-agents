# Drafted Agents - Documentation Index

Welcome to the Drafted Agents monorepo! This index will help you navigate the documentation and get started quickly.

## 🚀 Getting Started (Start Here!)

1. **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Overview of what was created
2. **[QUICK_START.md](QUICK_START.md)** - Step-by-step setup guide
3. **[.env.example](.env.example)** - Copy to `.env` and configure

## 📚 Core Documentation

### Understanding the System
- **[STRUCTURE.md](STRUCTURE.md)** - Repository structure and file organization
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** - Current status and roadmap
- **Original Spec**: `/Users/rodrigopecchio/Desktop/drafted-agentic-stack-setup.md`

### Configuration Files
- **[.env.example](.env.example)** - Environment variables template
- **[docker-compose.yml](infra/docker-compose.yml)** - Infrastructure services
- **[package.json](package.json)** - Root package.json with workspaces

## 🎭 Agent System

### Personas (Agent Behaviors)
Located in `workflows/personas/`:
- **[researcher.yml](workflows/personas/researcher.yml)** - Evidence-first investigation
- **[debugger.yml](workflows/personas/debugger.yml)** - Root cause analysis
- **[coder-fe.yml](workflows/personas/coder-fe.yml)** - Frontend implementation
- **[coder-be.yml](workflows/personas/coder-be.yml)** - Backend implementation
- **[breaker.yml](workflows/personas/breaker.yml)** - Adversarial testing
- **[communicator.yml](workflows/personas/communicator.yml)** - Updates and summaries

### Skills (Agent Capabilities)
Located in `workflows/skills/`:
- **[github_pr.yml](workflows/skills/github_pr.yml)** - PR creation and management
- **[repo_read.yml](workflows/skills/repo_read.yml)** - Repository analysis
- **[run_tests.yml](workflows/skills/run_tests.yml)** - Test execution
- **[ticket_update.yml](workflows/skills/ticket_update.yml)** - Ticket management
- **[slack_update.yml](workflows/skills/slack_update.yml)** - Slack notifications
- **[patch_edit.yml](workflows/skills/patch_edit.yml)** - Code patching

### Workflow Templates
Located in `workflows/templates/`:
- **[ticket-to-pr.yml](workflows/templates/ticket-to-pr.yml)** - Ticket → PR workflow
- **[research-memo.yml](workflows/templates/research-memo.yml)** - Research workflow
- **[bug-triage.yml](workflows/templates/bug-triage.yml)** - Bug fixing workflow

## 🔒 Security & Governance

Located in `policies/`:
- **[commands.allowlist.yml](policies/commands.allowlist.yml)** - Allowed commands
- **[data.boundaries.yml](policies/data.boundaries.yml)** - Access control per persona
- **[redaction.yml](policies/redaction.yml)** - Secret redaction patterns

## 🏗️ Application Services

### Orchestrator (Brain)
- **[main.py](apps/orchestrator/main.py)** - FastAPI application
- **[requirements.txt](apps/orchestrator/requirements.txt)** - Python dependencies
- **[Dockerfile](apps/orchestrator/Dockerfile)** - Container image

### Indexer (Knowledge Layer)
- **[main.py](apps/indexer/main.py)** - Indexing service
- **[requirements.txt](apps/indexer/requirements.txt)** - Python dependencies
- **[Dockerfile](apps/indexer/Dockerfile)** - Container image

### UI (Dashboard)
- **[page.tsx](apps/ui/app/page.tsx)** - Main dashboard
- **[layout.tsx](apps/ui/app/layout.tsx)** - Root layout
- **[package.json](apps/ui/package.json)** - Node dependencies

## 🔌 MCP Servers

### GitHub Server
- **[index.js](mcp/github-server/index.js)** - Server implementation
- **[package.json](mcp/github-server/package.json)** - Dependencies

### Linear Server
- **[index.js](mcp/linear-server/index.js)** - Server implementation
- **[package.json](mcp/linear-server/package.json)** - Dependencies

### Slack Server
- **[index.js](mcp/slack-server/index.js)** - Server implementation
- **[package.json](mcp/slack-server/package.json)** - Dependencies

### Notion Server
- **[index.js](mcp/notion-server/index.js)** - Server implementation
- **[package.json](mcp/notion-server/package.json)** - Dependencies

### Firebase Server
- **[index.js](mcp/firebase-server/index.js)** - Server implementation
- **[package.json](mcp/firebase-server/package.json)** - Dependencies

## 🏃 Runtime Configuration

### OpenHands
- **[config.yml](runtimes/openhands/config.yml)** - Runtime configuration
- **[Dockerfile.sandbox](runtimes/openhands/Dockerfile.sandbox)** - Sandbox image

## 🛠️ Scripts & Utilities

- **[setup.sh](setup.sh)** - Automated setup script
- **[docker-compose.yml](infra/docker-compose.yml)** - Infrastructure orchestration

## 📖 Quick Reference

### Common Commands

```bash
# Setup
./setup.sh

# Start infrastructure
cd infra && docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Development
cd apps/orchestrator && python main.py
cd apps/ui && npm run dev
```

### Service Ports

| Service | Port | URL |
|---------|------|-----|
| Temporal UI | 8080 | http://localhost:8080 |
| Qdrant | 6333 | http://localhost:6333 |
| OpenHands | 8000 | http://localhost:8000 |
| Orchestrator | 8001 | http://localhost:8001 |
| MCP GitHub | 3000 | http://localhost:3000 |
| MCP Linear | 3001 | http://localhost:3001 |
| MCP Notion | 3002 | http://localhost:3002 |
| MCP Slack | 3003 | http://localhost:3003 |
| MCP Firebase | 3004 | http://localhost:3004 |

## 🎯 Implementation Roadmap

See **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** for detailed roadmap.

### Phase 1: Core Orchestration (Next)
- Implement LangGraph state machine
- Add routing logic
- Connect to MCP servers

### Phase 2: Execution Runtime
- Integrate OpenHands executor
- Test code execution in sandbox

### Phase 3: Temporal Workflows
- Create Ticket→PR workflow
- Add retry logic

### Phase 4: Knowledge Layer
- Implement indexing
- Add retrieval API

### Phase 5: Approval & Governance
- Build approval UI
- Add audit logging

## 💡 Need Help?

1. Check **[QUICK_START.md](QUICK_START.md)** for setup issues
2. Review **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** for current status
3. See **[STRUCTURE.md](STRUCTURE.md)** for file organization
4. Refer to original spec at `/Users/rodrigopecchio/Desktop/drafted-agentic-stack-setup.md`

## 🎉 What's Working

- ✅ All infrastructure services
- ✅ MCP server endpoints
- ✅ Orchestrator API
- ✅ UI dashboard
- ✅ Configuration files

## 🚧 What's Next

- ⏳ LangGraph implementation
- ⏳ OpenHands integration
- ⏳ Temporal workflows
- ⏳ Knowledge indexing
- ⏳ Approval UI

---

**Last Updated**: February 3, 2026  
**Status**: Infrastructure Complete, Ready for Development
