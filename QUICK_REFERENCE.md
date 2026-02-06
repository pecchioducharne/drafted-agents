# Drafted Agents - Quick Reference

## 🚀 Quick Start

```bash
# Start services
cd drafted-agents
docker compose -f docker-compose.simple.yml up -d

# Check status
docker compose -f docker-compose.simple.yml ps

# Submit a job
./scripts/cli.py submit --request "Fix issue #123"

# Check job status
./scripts/cli.py status <job_id>
```

## 🔑 API Keys (All Configured)

| Service | Status | Token |
|---------|--------|-------|
| Anthropic | ✅ | `sk-ant-api03-6XlXLxC...` |
| GitHub | ✅ | `github_pat_11BA2ZZTQ...` |
| Netlify | ✅ | `nfp_zKqoPrX6gZ8BGzDL...` |
| Firebase | ✅ | Service account JSON |
| Notion | ✅ | `ntn_m75769718089oem2...` |

## 🧪 Testing

```bash
# Test all keys
cd drafted-agents
source .venv/bin/activate
python scripts/test_all_keys.py

# Test individual services
python scripts/test_anthropic.py
python scripts/test_github.py
python scripts/test_netlify.py
python scripts/test_firebase.py
python scripts/test_notion.py
```

## 🛠️ Skills Available

| Skill | Purpose | Use Case |
|-------|---------|----------|
| `github_context` | Fetch issue/PR/file context | Get repo info |
| `netlify_deploy` | Get deploy preview URL | Check deployments |
| `notion_read` | Search/read Notion docs | Find runbooks |
| `notion_write` | Create Notion pages | Document results |
| `openhands_pr` | Execute code changes | Create PRs |

## 📋 Job Types

| Type | Description | Skills Used |
|------|-------------|-------------|
| `issue_to_pr` | Convert issue to PR | github_context, openhands_pr, netlify_deploy |
| `debug_explain` | Investigate without changes | github_context |
| `firebase_task` | Safe Firebase operations | firebase_client |

## 🎯 Common Commands

### Submit Jobs

```bash
# Simple request
./scripts/cli.py submit --request "Fix mobile layout"

# With context
./scripts/cli.py submit \
  --request "Fix issue #123" \
  --repo drafted-web \
  --issue 123

# Specific job type
./scripts/cli.py submit \
  --job-type debug_explain \
  --request "Why is auth failing?"
```

### Check Status

```bash
# Single job
./scripts/cli.py status abc123

# All jobs
./scripts/cli.py list

# Watch logs
./scripts/cli.py logs abc123
```

## 🐳 Docker Commands

```bash
# Start all services
docker compose -f docker-compose.simple.yml up -d

# Stop all services
docker compose -f docker-compose.simple.yml down

# View logs
docker compose -f docker-compose.simple.yml logs -f api
docker compose -f docker-compose.simple.yml logs -f worker

# Restart a service
docker compose -f docker-compose.simple.yml restart api

# Rebuild after code changes
docker compose -f docker-compose.simple.yml up -d --build
```

## 📁 Project Structure

```
drafted-agents/
├── src/
│   ├── api/          # FastAPI server
│   ├── worker/       # RQ job processor
│   ├── skills/       # Skill implementations
│   ├── tools/        # API clients
│   ├── openhands/    # Executor adapter
│   └── interfaces.py # Core contracts
├── scripts/
│   ├── cli.py        # Command-line tool
│   └── test_*.py     # Test scripts
├── docker-compose.simple.yml
├── requirements.txt
└── .env
```

## 🔧 Configuration Files

### `.env`
```bash
# AI Models
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-placeholder-key-here

# GitHub
GITHUB_TOKEN=github_pat_...
GITHUB_ORG=drafted

# Netlify
NETLIFY_AUTH_TOKEN=nfp_...
NETLIFY_SITE_ID=4fd1a1e2-...

# Firebase
FIREBASE_PROJECT_ID=drafted-6c302
FIREBASE_SERVICE_ACCOUNT_JSON={...}

# Notion
NOTION_TOKEN=ntn_m75769718089oem2...
NOTION_ROOT_PAGE_ID=

# Infrastructure
REDIS_URL=redis://redis:6379
OPENHANDS_URL=http://openhands:8000
```

## 🚨 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Check logs
docker compose -f docker-compose.simple.yml logs

# Rebuild
docker compose -f docker-compose.simple.yml up -d --build
```

### API key errors
```bash
# Test keys
python scripts/test_all_keys.py

# Check .env file
cat .env | grep TOKEN
```

### Job stuck
```bash
# Check worker logs
docker compose -f docker-compose.simple.yml logs worker

# Check Redis
docker exec -it drafted-agents-redis-1 redis-cli
> KEYS *
```

### Notion not working
```bash
# Test token
python scripts/test_notion.py

# Grant page access:
# 1. Open Notion page
# 2. Click ••• → Connections
# 3. Add "Drafted Brain"
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| `SETUP_SIMPLIFIED.md` | Main setup guide |
| `NOTION_INTEGRATION.md` | Notion setup and usage |
| `NOTION_COMPLETE.md` | Notion quick start |
| `EXTENSION_SUMMARY.md` | How Notion was added |
| `QUICK_REFERENCE.md` | This file |

## 🎓 Adding New Skills

```python
# 1. Create skill file
# src/skills/my_skill.py
from src.interfaces import Skill, SkillResult, TaskContext

class MySkill(Skill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    async def run(self, context: TaskContext) -> SkillResult:
        # Implementation
        pass

# 2. Register skill
# src/worker/processor.py
skill_registry.register(MySkill())

# 3. Update router
# src/worker/router.py
# Add to skill descriptions
```

## 🔗 Useful URLs

- **API**: http://localhost:7001
- **OpenHands**: http://localhost:8000
- **Redis**: localhost:6379
- **GitHub**: https://github.com/drafted
- **Netlify**: https://app.netlify.com
- **Firebase**: https://console.firebase.google.com
- **Notion**: https://notion.so

## 💡 Tips

1. **Always test keys first**: `python scripts/test_all_keys.py`
2. **Check Docker logs**: `docker compose logs -f`
3. **Use CLI for jobs**: `./scripts/cli.py submit`
4. **Grant Notion access**: Share pages with "Drafted Brain"
5. **Monitor Redis**: `docker exec -it drafted-agents-redis-1 redis-cli`

## 🎯 Next Steps

1. **Grant Notion page access** (see NOTION_INTEGRATION.md)
2. **Test a simple job**: `./scripts/cli.py submit --request "Hello"`
3. **Try issue to PR**: `./scripts/cli.py submit --request "Fix #123"`
4. **Add custom skills** (see EXTENSION_SUMMARY.md)

## 📞 Support

- **Documentation**: See `SETUP_SIMPLIFIED.md`
- **Notion Setup**: See `NOTION_INTEGRATION.md`
- **Extensibility**: See `EXTENSION_SUMMARY.md`
- **Architecture**: See `drafted-agentic-stack-setup-simple.md`
