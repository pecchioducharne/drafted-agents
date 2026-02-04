# Drafted Agents - Quick Start Guide

This monorepo implements a production-grade agentic system for Drafted using:
- **LangGraph** for orchestration
- **MCP (Model Context Protocol)** for tool/data connectors
- **OpenHands** for sandboxed code execution
- **Temporal** for durable async workflows
- **Qdrant** for vector storage and knowledge layer

## Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- GitHub access token
- Linear API token
- Slack bot token
- Notion integration token
- Firebase service account JSON

## Quick Setup

### 1. Run the setup script

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Configure environment variables

Edit `.env` and replace placeholder values with your actual credentials:

```bash
# Required
GITHUB_TOKEN=your_github_token_here
LINEAR_TOKEN=your_linear_token_here
SLACK_BOT_TOKEN=your_slack_bot_token_here
NOTION_TOKEN=your_notion_token_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional (for secondary providers)
OPENAI_API_KEY=your_openai_key_here
```

### 3. Start the infrastructure

```bash
cd infra
docker-compose up -d
```

This starts:
- PostgreSQL (Temporal database)
- Temporal server + UI
- Qdrant (vector store)
- MCP servers (GitHub, Linear, Slack, Notion, Firebase)
- OpenHands runtime

### 4. Verify services are running

```bash
# Check all services
docker-compose ps

# Check Temporal UI
open http://localhost:8080

# Check Qdrant
curl http://localhost:6333/health
```

### 5. Start the orchestrator (development)

```bash
cd ../apps/orchestrator
pip install -r requirements.txt
python main.py
```

### 6. Start the UI (development)

```bash
cd ../apps/ui
npm run dev
```

Visit http://localhost:3000 to access the dashboard.

## Architecture Overview

```
drafted-agents/
├── apps/
│   ├── orchestrator/     # LangGraph brain (Python/FastAPI)
│   ├── indexer/          # Knowledge layer ingestion (Python)
│   └── ui/               # Dashboard (Next.js)
├── mcp/
│   ├── github-server/    # GitHub MCP connector
│   ├── linear-server/    # Linear MCP connector
│   ├── slack-server/     # Slack MCP connector
│   ├── notion-server/    # Notion MCP connector
│   └── firebase-server/  # Firebase MCP connector
├── workflows/
│   ├── personas/         # Agent personas (Researcher, Coder, etc.)
│   ├── skills/           # Reusable skill modules
│   └── templates/        # Workflow templates (Ticket→PR, etc.)
├── policies/
│   ├── commands.allowlist.yml
│   ├── data.boundaries.yml
│   └── redaction.yml
├── runtimes/
│   └── openhands/        # Sandbox configuration
└── infra/
    └── docker-compose.yml
```

## Key Concepts

### Personas
Behavioral wrappers that define how agents act:
- **Researcher**: Evidence-first, citations, no code changes
- **Debugger**: Root cause analysis, reproduction
- **Coder-FE/BE**: Implementation with tests
- **Breaker**: Adversarial testing, security
- **Communicator**: PR descriptions, updates

### Skills
Modular capabilities agents can use:
- **GitHubPR**: Create and manage PRs
- **RepoRead**: Read repository code
- **RunTests**: Execute test suites
- **TicketUpdate**: Update Linear/Jira tickets
- **SlackUpdate**: Post to Slack

### Workflows
End-to-end task templates:
- **Ticket → PR**: Convert ticket to pull request
- **Bug Triage**: Reproduce, fix, test bugs
- **Research Memo**: Investigate and document options

## Usage Examples

### Create a task via API

```bash
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Fix bug in candidate page where Safari crashes",
    "repo": "drafted-web",
    "ticket": "LIN-123",
    "risk_level": "medium"
  }'
```

### List available personas

```bash
curl http://localhost:8001/personas
```

### Check task status

```bash
curl http://localhost:8001/tasks/{task_id}
```

## Development Workflow

### Adding a new MCP server

1. Create directory: `mcp/new-server/`
2. Add `package.json`, `index.js`, `Dockerfile`
3. Add service to `infra/docker-compose.yml`
4. Update `.env.example` with required variables

### Adding a new persona

1. Create YAML file in `workflows/personas/`
2. Define: name, goal, risk_posture, output_format, disallowed, required
3. Restart orchestrator to load new persona

### Adding a new skill

1. Create YAML file in `workflows/skills/`
2. Define: name, tools, success_checks, constraints
3. Reference in persona or workflow templates

## Monitoring

- **Temporal UI**: http://localhost:8080 - View workflow executions
- **Qdrant Dashboard**: http://localhost:6333/dashboard - Vector store
- **Orchestrator Health**: http://localhost:8001/health
- **Agent UI**: http://localhost:3000 - Task management

## Security

All agents run with:
- Command allowlists (see `policies/commands.allowlist.yml`)
- Data boundaries (see `policies/data.boundaries.yml`)
- Secret redaction (see `policies/redaction.yml`)
- Sandboxed execution (OpenHands)
- Approval gates for high-risk changes

## Troubleshooting

### Services won't start

```bash
cd infra
docker-compose logs
```

### MCP server errors

```bash
docker-compose logs mcp-github
docker-compose logs mcp-linear
```

### Reset everything

```bash
cd infra
docker-compose down -v
docker-compose up -d
```

## Next Steps

1. ✅ Infrastructure is running
2. ⏭️ Implement the orchestrator routing logic
3. ⏭️ Connect OpenHands executor
4. ⏭️ Add Temporal workflows
5. ⏭️ Implement approval UI
6. ⏭️ Add more MCP connectors (Sentry, Datadog, etc.)

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [OpenHands Documentation](https://docs.all-hands.dev/)
- [Temporal Documentation](https://docs.temporal.io/)
