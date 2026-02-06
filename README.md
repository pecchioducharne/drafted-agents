# 🧠 Drafted Brain

**AI-Powered Agent System for Automated Development**

```
    ___            __ _           _   
   /   \_ __ __ _ / _| |_ ___  __| |  
  / /\ / '__/ _` | |_| __/ _ \/ _` |  
 / /_//| | | (_| |  _| ||  __/ (_| |_ 
/___,' |_|  \__,_|_|  \__\___|\__,_(_)
```

## 🚀 Quick Start

```bash
# Navigate to project
cd "/Users/rodrigopecchio/Drafted/Drafted Apps/drafted-brain"

# Start the system
./start.sh

# Activate Python environment
source .venv/bin/activate

# Test the system
./drafted health

# Submit your first job
./drafted run "Hello, test the system"
```

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed instructions
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - All commands and tips

## 💻 CLI Commands

```bash
# Health check
./drafted health

# Submit a job
./drafted run "Your task here"

# Check job status
./drafted status <job_id>

# View logs
./drafted logs <job_id>

# List all jobs
./drafted list

# Show version
./drafted version
```

## 🎯 Example Tasks

```bash
# Simple test
./drafted run "What can you do?"

# Analyze repository
./drafted run "Analyze the authentication flow" --repo drafted-web

# Fix an issue
./drafted run "Fix issue #123" --repo drafted-web --issue 123

# Create a feature
./drafted run "Add dark mode toggle" --repo drafted-web
```

## 🔧 System Architecture

- **Anthropic Claude** - AI reasoning engine
- **Redis + RQ** - Async job queue
- **OpenHands** - Sandboxed code execution
- **FastAPI** - REST API server
- **Typer + Rich** - Beautiful CLI

## 🌐 Services

- **API**: http://localhost:7001
- **OpenHands**: http://localhost:8000
- **Redis**: localhost:6379

## 🔑 Integrations

- ✅ Anthropic Claude (AI)
- ✅ GitHub (code repository)
- ✅ Netlify (deploy previews)
- ✅ Firebase (database)
- ✅ Notion (documentation)

## 🛑 Stop System

```bash
./stop.sh
```

## 📚 Learn More

See [START_HERE.md](START_HERE.md) for complete documentation.

---

**Version**: 1.0.0  
**Status**: Production Ready ✅
