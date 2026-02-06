# Claude Code Setup for Drafted Brain

This document explains how to set up Claude Code with all required MCP servers and integrations for the Drafted Brain project.

## Prerequisites

- [Claude Code CLI](https://code.claude.com) installed
- Node.js and npm installed
- Firebase CLI installed and authenticated
- Docker (optional, for local Firebase MCP)

## Quick Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd drafted-brain
```

### 2. Set Up Environment Variables

```bash
# Copy the example file
cp .env.mcp.example .env.mcp

# Edit .env.mcp and add your actual API keys
nano .env.mcp  # or use your preferred editor

# Load the environment variables
source .env.mcp
```

### 3. MCP Servers Are Auto-Configured!

The `.mcp.json` file in this repo automatically configures:
- ✅ GitHub MCP Server
- ✅ Firebase MCP Server
- ✅ Perplexity MCP Server
- ✅ Netlify MCP Server

When you start Claude Code from this directory, these servers will be automatically loaded.

### 4. Authenticate Additional Services

#### Notion
```bash
# In Claude Code, type:
/mcp

# Select Notion and authenticate via OAuth
```

#### Firebase CLI
```bash
firebase login
firebase projects:list  # Verify access to drafted-6c302
```

### 5. Verify Setup

```bash
claude mcp list
```

You should see:
```
✓ github: Connected
✓ firebase: Connected
✓ perplexity: Connected
✓ claude.ai Notion: Connected
```

## MCP Server Details

### GitHub MCP
- **Type**: HTTP
- **URL**: https://api.githubcopilot.com/mcp
- **Auth**: GitHub Personal Access Token (via GITHUB_TOKEN env var)
- **Scopes Required**: `repo`

### Firebase MCP
- **Type**: stdio
- **Command**: `npx -y firebase-tools@latest mcp`
- **Auth**: Firebase CLI authentication
- **Project**: drafted-6c302

### Perplexity MCP
- **Type**: stdio
- **Command**: `npx -y @perplexity-ai/mcp-server`
- **Auth**: API key via PERPLEXITY_API_KEY env var
- **Features**: Web search, research, reasoning

### Notion MCP
- **Type**: Official claude.ai integration
- **Auth**: OAuth (configured via `/mcp` command)
- **Workspace**: Join Drafted.

## Getting API Keys

### GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`
4. Copy token to `.env.mcp`

### Perplexity API Key
1. Go to https://www.perplexity.ai/account/api/group
2. Create new API key
3. Copy to `.env.mcp`

### Netlify Access Token
1. Go to https://app.netlify.com/user/applications
2. Create new access token
3. Copy to `.env.mcp`

## Project Structure

```
drafted-brain/
├── .mcp.json                 # MCP server configuration (committed to Git)
├── .env.mcp.example          # Example environment variables (committed)
├── .env.mcp                  # Your actual keys (NOT committed, in .gitignore)
├── CLAUDE_SETUP.md           # This file (committed)
├── src/                      # Application code
└── ...
```

## Troubleshooting

### MCP Server Won't Connect

```bash
# Check environment variables are loaded
echo $GITHUB_TOKEN
echo $PERPLEXITY_API_KEY

# Restart Claude Code
exit  # Exit current session
claude  # Start new session
```

### Firebase Authentication Issues

```bash
firebase login
firebase projects:list
```

### GitHub Token Invalid

```bash
# Test the token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

## Sharing with Team

When onboarding a new team member:

1. They clone the repo
2. They copy `.env.mcp.example` to `.env.mcp`
3. They add their own API keys to `.env.mcp`
4. They run `source .env.mcp`
5. They start `claude` and everything works!

## Security Notes

⚠️ **Never commit these files:**
- `.env.mcp` (contains actual secrets)
- Any file with real API keys

✅ **Safe to commit:**
- `.mcp.json` (uses environment variable references)
- `.env.mcp.example` (only has placeholders)
- `CLAUDE_SETUP.md` (documentation)

## What Gets Auto-Loaded?

When you run `claude` from this directory, Claude Code will:
1. Read `.mcp.json`
2. Substitute environment variables (from your shell)
3. Start all configured MCP servers
4. Make tools available automatically

No manual `claude mcp add` commands needed!

## Additional Resources

- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp.md)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Firebase MCP Server](https://firebase.google.com/docs/ai-assistance/mcp-server)
- [Perplexity MCP Server](https://github.com/perplexityai/modelcontextprotocol)
