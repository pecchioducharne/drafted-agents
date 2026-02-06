# 🚀 START HERE - Drafted Agents System

## ✅ System Status

Your Drafted Agents system is **fully configured and ready to use**!

- ✅ All API keys configured (Anthropic, GitHub, Netlify, Firebase, Notion)
- ✅ Docker Compose setup complete
- ✅ CLI tool ready
- ✅ All tests passing

## 🎯 Quick Start (5 Minutes)

### Step 1: Navigate to Project

```bash
cd "/Users/rodrigopecchio/Drafted/Drafted Apps/drafted-agents"
```

### Step 2: Start the System

```bash
./start.sh
```

This starts all services (Redis, OpenHands, API, Workers).

### Step 3: Activate Python Environment

```bash
source .venv/bin/activate
```

### Step 4: Test the System

```bash
# Check health
./scripts/cli.py health

# Submit a test job
./scripts/cli.py run "Hello, test the system"
```

You'll get a job ID back (e.g., `abc123def456`).

### Step 5: Check Job Status

```bash
./scripts/cli.py status <job_id>
```

### Step 6: View Job Logs

```bash
./scripts/cli.py logs <job_id>
```

## 🎓 Example Tasks

### Simple Test
```bash
./scripts/cli.py run "What can you do?"
```

### Analyze Repository
```bash
./scripts/cli.py run "Analyze the authentication flow in drafted-web" --repo drafted-web
```

### Fix an Issue
```bash
./scripts/cli.py run "Fix issue #123: mobile layout breaks on small screens" \
  --repo drafted-web \
  --issue 123
```

### Research Task
```bash
./scripts/cli.py run "Research React authentication best practices"
```

### Create Feature
```bash
./scripts/cli.py run "Add a dark mode toggle to the settings page" \
  --repo drafted-web
```

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `./start.sh` | Start all services |
| `./stop.sh` | Stop all services |
| `./scripts/cli.py health` | Check system health |
| `./scripts/cli.py run "task"` | Submit a job |
| `./scripts/cli.py status <id>` | Check job status |
| `./scripts/cli.py logs <id>` | View job logs |

## 🌐 Service URLs

- **API**: http://localhost:7001
- **OpenHands**: http://localhost:8000
- **Redis**: localhost:6379

## 📊 Monitoring

### View All Service Logs
```bash
docker compose -f docker-compose.simple.yml logs -f
```

### View Specific Service
```bash
docker compose -f docker-compose.simple.yml logs -f api
docker compose -f docker-compose.simple.yml logs -f worker
```

### Check Service Status
```bash
docker compose -f docker-compose.simple.yml ps
```

## 🛑 Stopping the System

```bash
./stop.sh
```

Or manually:
```bash
docker compose -f docker-compose.simple.yml down
```

## 🔧 What the System Can Do

### Available Skills

1. **GitHub Context** - Fetch issues, PRs, files from GitHub
2. **Netlify Deploy** - Get deploy preview URLs
3. **Notion Read** - Search and read Notion documentation
4. **Notion Write** - Create pages and summaries
5. **OpenHands PR** - Execute code changes and create PRs

### Job Types

1. **issue_to_pr** - Convert GitHub issue to PR
2. **debug_explain** - Investigate without making changes
3. **firebase_task** - Safe Firebase operations

### Integrations

- ✅ **Anthropic Claude** - AI reasoning
- ✅ **GitHub** - Code repository access
- ✅ **Netlify** - Deploy previews
- ✅ **Firebase** - Database operations
- ✅ **Notion** - Documentation (needs page access)

## 📝 Optional: Grant Notion Access

To enable Notion features:

1. Open Notion in browser
2. Find your top-level workspace pages
3. For each page:
   - Click `•••` → "Connections"
   - Add "Drafted Brain"

See `NOTION_ACCESS_GUIDE.md` for details.

## 📚 Documentation

| File | Purpose |
|------|---------|
| **START_HERE.md** | This file - quick start |
| **GETTING_STARTED.md** | Detailed startup guide |
| **QUICK_REFERENCE.md** | All commands and tips |
| **SETUP_SIMPLIFIED.md** | Full system documentation |
| **NOTION_INTEGRATION.md** | Notion setup and usage |
| **NOTION_ACCESS_GUIDE.md** | How to share Notion pages |
| **EXTENSION_SUMMARY.md** | How to add new skills |

## 🚨 Troubleshooting

### Services Won't Start
```bash
# Check Docker is running
docker ps

# View logs
docker compose -f docker-compose.simple.yml logs

# Rebuild
docker compose -f docker-compose.simple.yml up -d --build
```

### Job Stuck or Failed
```bash
# Check worker logs
docker compose -f docker-compose.simple.yml logs worker

# Check job status
./scripts/cli.py status <job_id>
```

### API Not Responding
```bash
# Check health
curl http://localhost:7001/health

# Restart API
docker compose -f docker-compose.simple.yml restart api
```

## 🎯 Next Steps

1. **Test the system** with a simple job
2. **Grant Notion access** (optional but recommended)
3. **Try a real task** (fix an issue, create a feature)
4. **Explore skills** and job types
5. **Add custom workflows** (see EXTENSION_SUMMARY.md)

## 💡 Tips

- Start with simple tasks to understand the system
- Use `--repo` flag to give GitHub context
- Use `--issue` flag to link to specific issues
- Check logs if jobs seem stuck
- Grant Notion access for documentation features

## 🎉 You're Ready!

The system is fully configured and ready to use. Start with:

```bash
./start.sh
source .venv/bin/activate
./scripts/cli.py run "Hello, test the system"
```

Then check the job status and logs to see it in action!

---

**Need help?** Check the documentation files or run `./scripts/cli.py --help`
