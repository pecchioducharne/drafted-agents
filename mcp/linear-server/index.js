const express = require('express');
const { LinearClient } = require('@linear/sdk');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3001;

app.use(express.json());

// Initialize Linear client
const linearClient = new LinearClient({
  apiKey: process.env.LINEAR_TOKEN
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mcp-linear' });
});

// MCP tool: get_issue
app.post('/tools/get_issue', async (req, res) => {
  try {
    const { issue_id } = req.body;
    const issue = await linearClient.issue(issue_id);
    res.json({ success: true, data: issue });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: update_issue
app.post('/tools/update_issue', async (req, res) => {
  try {
    const { issue_id, title, description, state } = req.body;
    const issue = await linearClient.updateIssue(issue_id, {
      title,
      description,
      stateId: state
    });
    res.json({ success: true, data: issue });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: add_comment
app.post('/tools/add_comment', async (req, res) => {
  try {
    const { issue_id, body } = req.body;
    const comment = await linearClient.createComment({
      issueId: issue_id,
      body
    });
    res.json({ success: true, data: comment });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// List available tools
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { name: 'get_issue', description: 'Get a Linear issue by ID' },
      { name: 'update_issue', description: 'Update a Linear issue' },
      { name: 'add_comment', description: 'Add a comment to a Linear issue' }
    ]
  });
});

app.listen(port, () => {
  console.log(`MCP Linear server listening on port ${port}`);
});
