const express = require('express');
const { Octokit } = require('@octokit/rest');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Initialize Octokit with token
const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mcp-github' });
});

// MCP tool: search_code
app.post('/tools/search_code', async (req, res) => {
  try {
    const { query, repo, org } = req.body;
    const q = repo ? `${query} repo:${org}/${repo}` : query;
    
    const result = await octokit.rest.search.code({ q });
    res.json({ success: true, data: result.data });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: get_file
app.post('/tools/get_file', async (req, res) => {
  try {
    const { owner, repo, path, ref } = req.body;
    const result = await octokit.rest.repos.getContent({ owner, repo, path, ref });
    res.json({ success: true, data: result.data });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: create_branch
app.post('/tools/create_branch', async (req, res) => {
  try {
    const { owner, repo, branch, from_branch } = req.body;
    
    // Get the SHA of the from_branch
    const refData = await octokit.rest.git.getRef({
      owner,
      repo,
      ref: `heads/${from_branch || 'main'}`
    });
    
    // Create new branch
    const result = await octokit.rest.git.createRef({
      owner,
      repo,
      ref: `refs/heads/${branch}`,
      sha: refData.data.object.sha
    });
    
    res.json({ success: true, data: result.data });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: open_pr
app.post('/tools/open_pr', async (req, res) => {
  try {
    const { owner, repo, title, body, head, base } = req.body;
    
    const result = await octokit.rest.pulls.create({
      owner,
      repo,
      title,
      body,
      head,
      base: base || 'main'
    });
    
    res.json({ success: true, data: result.data });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// List available tools
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { name: 'search_code', description: 'Search code in GitHub repositories' },
      { name: 'get_file', description: 'Get file contents from a repository' },
      { name: 'create_branch', description: 'Create a new branch' },
      { name: 'open_pr', description: 'Open a pull request' }
    ]
  });
});

app.listen(port, () => {
  console.log(`MCP GitHub server listening on port ${port}`);
});
