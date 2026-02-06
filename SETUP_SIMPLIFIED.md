# Drafted Agent Brain - Simplified Setup

**Version**: 0.2.0 (Simplified)  
**Date**: February 5, 2026

This is a **simplified, production-ready** agentic system for Drafted with:
- **Anthropic Claude** as the primary AI brain
- **Redis + RQ** for async job processing (replaces Temporal)
- **OpenHands** for sandboxed code execution
- **Direct tool clients** (GitHub, Netlify, Firebase) - no separate MCP servers
- **Extensible architecture** with three key seams

## 🎯 What Changed from Complex Setup

### Removed (Simplified)
- ❌ Temporal (replaced with Redis + RQ)
- ❌ PostgreSQL (no longer needed)
- ❌ Qdrant vector store (optional, add later)
- ❌ 5 separate MCP servers (now direct tool clients)
- ❌ LangGraph (using simpler LangChain)
- ❌ Separate UI app (CLI first)
- ❌ Linear, Slack, Notion integrations (focusing on core: GitHub, Netlify, Firebase)

### Added (Improved)
- ✅ **Extensibility interfaces** (Skill, Executor, JobType)
- ✅ **Skill registry** - add capabilities without rewiring
- ✅ **Executor registry** - swap backends easily
- ✅ **Job type templates** - define workflows as config
- ✅ **Standard TaskContext** - consistent contract
- ✅ **CLI tool** for easy interaction
- ✅ **Simplified deployment** (4 services vs 10+)

## 🚀 Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.simple .env
# Edit .env with your actual keys
```

### 3. Start infrastructure

```bash
docker compose -f docker-compose.simple.yml up -d --build
```

This starts:
- Redis (job queue)
- OpenHands (code executor)
- API (port 7000)
- Worker (2 replicas)

### 4. Verify services

```bash
# Check health
curl http://localhost:7000/health

# Or use CLI
python scripts/cli.py health
```

## 📋 Required API Keys

### Core (Required)
```bash
ANTHROPIC_API_KEY=sk-ant-...        # Claude API key
GITHUB_TOKEN=ghp_...                # GitHub fine-grained token
NETLIFY_AUTH_TOKEN=nfp_...          # Netlify personal access token
NETLIFY_SITE_ID=...                 # Your Netlify site ID
FIREBASE_SERVICE_ACCOUNT_JSON=...   # Firebase Admin SDK JSON
```

### Optional
```bash
OPENAI_API_KEY=sk-...               # Fallback model
```

## 🎭 Architecture

### Services (4 total)
1. **Redis** - Job queue and caching
2. **OpenHands** - Sandboxed code execution
3. **API** - Job submission and status (FastAPI)
4. **Worker** - Async job processing (RQ)

### Core Concepts

#### 1. Personas (Behavioral Wrappers)
- `researcher` - Evidence-first, no code changes
- `debugger` - Reproduce and analyze bugs
- `coder` - Implement features with tests
- `breaker` - Adversarial testing
- `communicator` - Summaries and updates

#### 2. Skills (Modular Capabilities)
- `github_context` - Fetch issue/PR/file context
- `netlify_deploy` - Get deploy preview URL
- `openhands_pr` - Execute code changes

**Adding new skills:**
```python
# src/skills/my_skill.py
from src.interfaces import Skill

class MySkill(Skill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    async def run(self, context: TaskContext) -> SkillResult:
        # Implementation
        pass

# Register in worker/processor.py
skill_registry.register(MySkill())
```

#### 3. Executors (Execution Backends)
- `openhands` - Default (sandboxed execution)
- `claude_code` - Can add later
- `codex` - Can add later

**Switching executors:**
Just change routing rules - no code changes needed.

#### 4. Job Types (Workflow Templates)
- `issue_to_pr` - Convert issue to PR
- `debug_explain` - Investigate without code changes
- `firebase_task` - Safe Firebase operations

**Adding new workflows:**
Create a YAML file in `src/job_types/` with skill sequence and gates.

## 📖 Usage

### CLI (Recommended)

```bash
# Submit a job
python scripts/cli.py run "Fix issue #123: mobile layout" --repo drafted-web --issue 123

# Check status
python scripts/cli.py status <job_id>

# Follow logs
python scripts/cli.py logs <job_id> --follow

# Check health
python scripts/cli.py health
```

### HTTP API

```bash
# Submit job
curl -X POST http://localhost:7000/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Fix mobile layout bug",
    "repo": "drafted-web",
    "issue": 123,
    "job_type": "issue_to_pr"
  }'

# Get status
curl http://localhost:7000/jobs/{job_id}

# List jobs
curl http://localhost:7000/jobs
```

## 🔧 Development

### Project Structure

```
src/
  api/              # FastAPI application
  worker/           # RQ worker and job processor
  skills/           # Skill implementations
  personas/         # Persona configs (YAML)
  tools/            # GitHub, Netlify, Firebase clients
  openhands/        # OpenHands executor adapter
  job_types/        # Job type templates (YAML)
  interfaces.py     # Core extensibility interfaces
```

### Adding a New Integration

1. **Create tool client** (`src/tools/new_service_client.py`)
2. **Create skill** (`src/skills/new_service_skill.py`) implementing `Skill` interface
3. **Register skill** in `src/worker/processor.py`
4. **Test** with a simple job

### Adding a New Executor

1. **Implement `Executor` interface** (`src/executors/my_executor.py`)
2. **Register** in `src/worker/processor.py`
3. **Update routing logic** to use new executor

## 🔒 Security

### Collection Allowlists (Firebase)
Only specific collections are accessible:
- **Read**: candidates, jobs, matches
- **Write**: analytics, agent_logs

### Command Allowlists (OpenHands)
Only safe commands allowed in sandbox:
- npm/pnpm/yarn commands
- git operations
- test runners
- linters

### Secret Redaction
All logs automatically redact:
- API keys
- Tokens
- Passwords
- Private keys

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:7000/health
```

### Queue Status
```bash
# Check Redis
docker exec -it drafted-agents-redis-1 redis-cli INFO
docker exec -it drafted-agents-redis-1 redis-cli LLEN rq:queue:agent-jobs
```

### Logs
```bash
# API logs
docker logs -f drafted-agents-api-1

# Worker logs
docker logs -f drafted-agents-worker-1

# All logs
docker compose -f docker-compose.simple.yml logs -f
```

## 🚀 Deployment

### Docker Compose (Recommended for MVP)
Already configured in `docker-compose.simple.yml`

### Environment Variables (Production)
Use a secrets manager:
- AWS Secrets Manager
- GCP Secret Manager
- HashiCorp Vault

### Scaling
```yaml
# Increase workers in docker-compose.simple.yml
worker:
  deploy:
    replicas: 4  # More workers for parallel processing
```

## 🔄 Upgrade Path

When you need more capability:

1. **Add vector memory** - Just add Qdrant, update context gathering
2. **Add LangGraph** - For complex multi-agent workflows
3. **Swap to Temporal** - If you need stronger durability
4. **Add UI** - Build approval dashboard later

No major refactor needed - the extensibility seams support growth.

## 📝 Example Flow

```
1. User: "Fix issue #123"
   ↓
2. API receives request → enqueues job
   ↓
3. Worker picks up job
   ↓
4. Router (Claude) decides: persona=coder, skills=[github_context, openhands_pr, netlify_deploy]
   ↓
5. Execute github_context skill
   - Fetch issue details
   - Find related code
   ↓
6. Execute openhands_pr skill
   - OpenHands clones repo
   - Makes code changes
   - Runs tests
   - Opens PR
   ↓
7. Execute netlify_deploy skill
   - Find deploy preview URL
   ↓
8. Return result with PR link + deploy URL
```

## 🐛 Troubleshooting

### Services won't start
```bash
docker compose -f docker-compose.simple.yml logs
docker compose -f docker-compose.simple.yml ps
```

### Jobs stuck in queue
```bash
# Check worker logs
docker logs drafted-agents-worker-1

# Check Redis
docker exec -it drafted-agents-redis-1 redis-cli
> LLEN rq:queue:agent-jobs
> LRANGE rq:queue:agent-jobs 0 -1
```

### OpenHands not responding
```bash
docker logs drafted-agents-openhands-1
curl http://localhost:8000/health
```

## 🎯 Next Steps

1. ✅ Infrastructure running (you are here)
2. ⏭️ Add real API keys to `.env`
3. ⏭️ Test first job: `python scripts/cli.py run "test" --repo drafted-web`
4. ⏭️ Add more skills as needed
5. ⏭️ Deploy to production

---

**Status**: ✨ Simplified and Ready!  
**Compared to complex setup**: ~70% fewer services, same capability, easier to extend
