# Drafted Agents - Repository Structure

```
drafted-agents/
│
├── 📱 apps/                          # Application services
│   ├── orchestrator/                 # LangGraph brain (Python/FastAPI)
│   │   ├── main.py                   # API endpoints
│   │   ├── requirements.txt          # Python dependencies
│   │   └── Dockerfile                # Container image
│   │
│   ├── indexer/                      # Knowledge layer (Python)
│   │   ├── main.py                   # Indexing service
│   │   ├── requirements.txt          # Python dependencies
│   │   └── Dockerfile                # Container image
│   │
│   └── ui/                           # Dashboard (Next.js)
│       ├── app/
│       │   ├── layout.tsx            # Root layout
│       │   ├── page.tsx              # Home page
│       │   └── globals.css           # Global styles
│       ├── package.json              # Node dependencies
│       ├── tsconfig.json             # TypeScript config
│       ├── tailwind.config.ts        # Tailwind config
│       └── Dockerfile                # Container image
│
├── 🔌 mcp/                           # MCP server connectors
│   ├── github-server/                # GitHub integration
│   │   ├── index.js                  # Server implementation
│   │   ├── package.json              # Dependencies
│   │   └── Dockerfile                # Container image
│   │
│   ├── linear-server/                # Linear integration
│   │   ├── index.js
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   ├── slack-server/                 # Slack integration
│   │   ├── index.js
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   ├── notion-server/                # Notion integration
│   │   ├── index.js
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   └── firebase-server/              # Firebase integration
│       ├── index.js
│       ├── package.json
│       └── Dockerfile
│
├── 🎭 workflows/                     # Agent behaviors and workflows
│   ├── personas/                     # Agent personas (6 total)
│   │   ├── researcher.yml            # Evidence-first investigation
│   │   ├── debugger.yml              # Root cause analysis
│   │   ├── coder-fe.yml              # Frontend implementation
│   │   ├── coder-be.yml              # Backend implementation
│   │   ├── breaker.yml               # Adversarial testing
│   │   └── communicator.yml          # Updates and summaries
│   │
│   ├── skills/                       # Reusable capabilities (6 total)
│   │   ├── github_pr.yml             # PR creation and management
│   │   ├── repo_read.yml             # Repository analysis
│   │   ├── run_tests.yml             # Test execution
│   │   ├── ticket_update.yml         # Ticket management
│   │   ├── slack_update.yml          # Slack notifications
│   │   └── patch_edit.yml            # Code patching
│   │
│   └── templates/                    # Workflow templates (3 total)
│       ├── ticket-to-pr.yml          # Ticket → PR workflow
│       ├── research-memo.yml         # Research workflow
│       └── bug-triage.yml            # Bug fixing workflow
│
├── 🔒 policies/                      # Security and governance
│   ├── commands.allowlist.yml        # Allowed commands
│   ├── data.boundaries.yml           # Access control per persona
│   └── redaction.yml                 # Secret redaction patterns
│
├── 🏃 runtimes/                      # Execution environments
│   └── openhands/                    # OpenHands configuration
│       ├── config.yml                # Runtime configuration
│       └── Dockerfile.sandbox        # Sandbox image definition
│
├── 🏗️ infra/                         # Infrastructure
│   ├── docker-compose.yml            # All services orchestration
│   └── k8s/                          # Kubernetes configs (future)
│
├── 📄 Configuration Files
│   ├── .env.example                  # Environment variables template
│   ├── .gitignore                    # Git ignore patterns
│   ├── package.json                  # Root package.json (workspaces)
│   └── setup.sh                      # Setup script
│
└── 📚 Documentation
    ├── QUICK_START.md                # Getting started guide
    ├── IMPLEMENTATION_STATUS.md      # Current status and roadmap
    └── STRUCTURE.md                  # This file

```

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Temporal | 7233 | Temporal server |
| Temporal UI | 8080 | Temporal web interface |
| PostgreSQL | 5432 | Temporal database |
| Qdrant | 6333 | Vector store API |
| Qdrant gRPC | 6334 | Vector store gRPC |
| MCP GitHub | 3000 | GitHub connector |
| MCP Linear | 3001 | Linear connector |
| MCP Notion | 3002 | Notion connector |
| MCP Slack | 3003 | Slack connector |
| MCP Firebase | 3004 | Firebase connector |
| OpenHands | 8000 | Agent runtime |
| Orchestrator | 8001 | Brain API |
| UI | 3000 | Dashboard (dev) |

## Key Files by Purpose

### Getting Started
- `setup.sh` - Run this first
- `.env.example` - Copy to `.env` and configure
- `QUICK_START.md` - Step-by-step guide

### Infrastructure
- `infra/docker-compose.yml` - Start all services
- `runtimes/openhands/Dockerfile.sandbox` - Agent sandbox

### Configuration
- `workflows/personas/*.yml` - Agent behaviors
- `workflows/skills/*.yml` - Agent capabilities
- `workflows/templates/*.yml` - Workflow definitions
- `policies/*.yml` - Security rules

### Development
- `apps/orchestrator/main.py` - Main orchestration logic
- `apps/indexer/main.py` - Knowledge indexing
- `apps/ui/app/page.tsx` - Dashboard UI
- `mcp/*/index.js` - MCP server implementations

## File Count Summary

- **Personas**: 6 files
- **Skills**: 6 files
- **Workflow Templates**: 3 files
- **MCP Servers**: 5 servers
- **Policy Files**: 3 files
- **Apps**: 3 services
- **Total Configuration Files**: ~50+

## Technology Stack

### Backend
- Python 3.11 (Orchestrator, Indexer)
- FastAPI (API framework)
- LangGraph (Orchestration)
- Temporal (Workflows)

### Frontend
- Next.js 14 (UI)
- React 18
- TypeScript
- Tailwind CSS

### MCP Servers
- Node.js 20
- Express.js

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 15
- Qdrant (vector store)
- OpenHands (agent runtime)

### Integrations
- GitHub (Octokit)
- Linear SDK
- Slack Web API
- Notion Client
- Firebase Admin SDK
