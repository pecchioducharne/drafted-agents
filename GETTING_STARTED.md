# Getting Started with Drafted Agents

## Prerequisites

✅ Docker Desktop installed and running  
✅ Python 3.11+ installed  
✅ API keys configured in `.env`

## Step-by-Step Startup

### 1. Navigate to Project

```bash
cd "/Users/rodrigopecchio/Drafted/Drafted Apps/drafted-agents"
```

### 2. Verify Environment

Check that your `.env` file has all keys:

```bash
cat .env | grep -E "ANTHROPIC|GITHUB|NETLIFY|FIREBASE|NOTION"
```

You should see:
- ✅ ANTHROPIC_API_KEY
- ✅ GITHUB_TOKEN
- ✅ NETLIFY_AUTH_TOKEN
- ✅ FIREBASE_PROJECT_ID
- ✅ NOTION_TOKEN

### 3. Start Docker Services

```bash
docker compose -f docker-compose.simple.yml up -d
```

This starts:
- Redis (job queue)
- OpenHands (code execution sandbox)
- API server (port 7001)
- Worker (2 replicas)

### 4. Verify Services Are Running

```bash
docker compose -f docker-compose.simple.yml ps
```

Expected output:
```
NAME                          STATUS
drafted-agents-api-1          Up (healthy)
drafted-agents-openhands-1    Up (healthy)
drafted-agents-redis-1        Up (healthy)
drafted-agents-worker-1       Up
drafted-agents-worker-2       Up
```

### 5. Check Logs (Optional)

```bash
# Watch all services
docker compose -f docker-compose.simple.yml logs -f

# Watch specific service
docker compose -f docker-compose.simple.yml logs -f api
docker compose -f docker-compose.simple.yml logs -f worker
```

Press `Ctrl+C` to stop watching logs.

### 6. Set Up Python Virtual Environment (for CLI)

```bash
# Activate existing venv
source .venv/bin/activate

# Verify CLI works
./scripts/cli.py --help
```

## Interacting with the System

### Method 1: CLI Tool (Recommended)

The CLI tool (`scripts/cli.py`) is the easiest way to interact with agents.

#### Submit a Job

```bash
# Simple request
./scripts/cli.py submit --request "Hello, test the system"

# With GitHub context
./scripts/cli.py submit \
  --request "Analyze the authentication flow" \
  --repo drafted-web

# Fix an issue
./scripts/cli.py submit \
  --request "Fix issue #123: mobile layout bug" \
  --repo drafted-web \
  --issue 123

# Create a PR
./scripts/cli.py submit \
  --job-type issue_to_pr \
  --request "Add dark mode toggle to settings" \
  --repo drafted-web
```

#### Check Job Status

```bash
# Get job ID from submit command, then:
./scripts/cli.py status <job_id>

# Example:
./scripts/cli.py status abc123def456
```

#### List All Jobs

```bash
./scripts/cli.py list

# Or with limit
./scripts/cli.py list --limit 10
```

#### Watch Job Logs

```bash
./scripts/cli.py logs <job_id>

# Follow logs in real-time
./scripts/cli.py logs <job_id> --follow
```

### Method 2: HTTP API

You can also interact directly with the API.

#### Submit a Job

```bash
curl -X POST http://localhost:7001/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Fix mobile layout bug",
    "repo": "drafted-web",
    "issue": "123"
  }'
```

Response:
```json
{
  "job_id": "abc123def456",
  "status": "queued"
}
```

#### Check Status

```bash
curl http://localhost:7001/jobs/abc123def456
```

#### List Jobs

```bash
curl http://localhost:7001/jobs
```

#### Health Check

```bash
curl http://localhost:7001/health
```

### Method 3: Python Script

Create custom scripts using the API:

```python
import httpx

# Submit job
response = httpx.post(
    "http://localhost:7001/jobs",
    json={
        "request": "Create a login page component",
        "repo": "drafted-web"
    }
)

job_id = response.json()["job_id"]
print(f"Job submitted: {job_id}")

# Check status
status = httpx.get(f"http://localhost:7001/jobs/{job_id}")
print(status.json())
```

## Example Workflows

### Example 1: Simple Test

```bash
# Submit a simple job
./scripts/cli.py submit --request "Hello, what can you do?"

# Get the job ID from output (e.g., abc123)
# Check status
./scripts/cli.py status abc123

# Watch logs
./scripts/cli.py logs abc123
```

### Example 2: GitHub Issue to PR

```bash
# Submit issue-to-PR job
./scripts/cli.py submit \
  --job-type issue_to_pr \
  --request "Fix issue #123: mobile layout breaks on small screens" \
  --repo drafted-web \
  --issue 123

# Monitor progress
./scripts/cli.py logs <job_id> --follow
```

The agent will:
1. Fetch issue details from GitHub
2. Analyze the code
3. Create a fix
4. Submit a PR
5. Get Netlify deploy preview
6. Report results

### Example 3: Research and Document

```bash
# Research task with Notion output
./scripts/cli.py submit \
  --request "Research authentication best practices and create Notion summary"

# The agent will:
# 1. Search existing Notion docs
# 2. Research the topic
# 3. Create a summary page in Notion
```

### Example 4: Debug Investigation

```bash
# Debug without making changes
./scripts/cli.py submit \
  --job-type debug_explain \
  --request "Why is the login endpoint returning 401 errors?"

# The agent will investigate and explain without modifying code
```

## Monitoring

### Check Service Health

```bash
# API health
curl http://localhost:7001/health

# Redis
docker exec -it drafted-agents-redis-1 redis-cli ping

# OpenHands
curl http://localhost:8000/
```

### View Service Logs

```bash
# All services
docker compose -f docker-compose.simple.yml logs -f

# Specific service
docker compose -f docker-compose.simple.yml logs -f api
docker compose -f docker-compose.simple.yml logs -f worker
docker compose -f docker-compose.simple.yml logs -f openhands
```

### Check Redis Queue

```bash
# Connect to Redis
docker exec -it drafted-agents-redis-1 redis-cli

# Check queue length
> LLEN rq:queue:agent-jobs

# List jobs
> KEYS rq:job:*

# Exit
> exit
```

## Troubleshooting

### Services Won't Start

```bash
# Check Docker is running
docker ps

# Check for port conflicts
lsof -i:7001  # API port
lsof -i:8000  # OpenHands port
lsof -i:6379  # Redis port

# Restart services
docker compose -f docker-compose.simple.yml restart

# Rebuild if needed
docker compose -f docker-compose.simple.yml up -d --build
```

### Job Stuck or Failed

```bash
# Check worker logs
docker compose -f docker-compose.simple.yml logs worker

# Check job status
./scripts/cli.py status <job_id>

# Check Redis queue
docker exec -it drafted-agents-redis-1 redis-cli
> LLEN rq:queue:agent-jobs
```

### API Not Responding

```bash
# Check if API is running
docker compose -f docker-compose.simple.yml ps api

# Check API logs
docker compose -f docker-compose.simple.yml logs api

# Restart API
docker compose -f docker-compose.simple.yml restart api
```

### OpenHands Issues

```bash
# Check OpenHands logs
docker compose -f docker-compose.simple.yml logs openhands

# Restart OpenHands
docker compose -f docker-compose.simple.yml restart openhands

# Check OpenHands health
curl http://localhost:8000/
```

## Stopping the System

### Stop All Services

```bash
docker compose -f docker-compose.simple.yml down
```

### Stop and Remove Volumes

```bash
docker compose -f docker-compose.simple.yml down -v
```

### Stop Specific Service

```bash
docker compose -f docker-compose.simple.yml stop api
docker compose -f docker-compose.simple.yml stop worker
```

## Quick Reference

### Start System
```bash
cd "/Users/rodrigopecchio/Drafted/Drafted Apps/drafted-agents"
docker compose -f docker-compose.simple.yml up -d
```

### Submit Job
```bash
./scripts/cli.py submit --request "Your task here"
```

### Check Status
```bash
./scripts/cli.py status <job_id>
```

### View Logs
```bash
docker compose -f docker-compose.simple.yml logs -f
```

### Stop System
```bash
docker compose -f docker-compose.simple.yml down
```

## Next Steps

1. **Grant Notion Access** (optional but recommended)
   - See `NOTION_ACCESS_GUIDE.md`
   - Share top-level pages with "Drafted Brain"

2. **Try Example Jobs**
   - Start with simple test: `./scripts/cli.py submit --request "Hello"`
   - Try GitHub integration: `./scripts/cli.py submit --request "Analyze repo structure" --repo drafted-web`

3. **Explore Skills**
   - See `SETUP_SIMPLIFIED.md` for available skills
   - Check `QUICK_REFERENCE.md` for commands

4. **Create Custom Workflows**
   - See `EXTENSION_SUMMARY.md` for how to add skills
   - Add job types in `src/job_types/`

## Support

- **Main Setup**: `SETUP_SIMPLIFIED.md`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Notion Setup**: `NOTION_INTEGRATION.md`
- **Notion Access**: `NOTION_ACCESS_GUIDE.md`
- **Extension Guide**: `EXTENSION_SUMMARY.md`
