const express = require('express');
const { Client } = require('@notionhq/client');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3002;

app.use(express.json());

// Initialize Notion client
const notionClient = new Client({
  auth: process.env.NOTION_TOKEN
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mcp-notion' });
});

// MCP tool: get_page
app.post('/tools/get_page', async (req, res) => {
  try {
    const { page_id } = req.body;
    const page = await notionClient.pages.retrieve({ page_id });
    res.json({ success: true, data: page });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: get_blocks
app.post('/tools/get_blocks', async (req, res) => {
  try {
    const { block_id } = req.body;
    const blocks = await notionClient.blocks.children.list({ block_id });
    res.json({ success: true, data: blocks });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: create_page
app.post('/tools/create_page', async (req, res) => {
  try {
    const { parent, properties, children } = req.body;
    const page = await notionClient.pages.create({
      parent,
      properties,
      children
    });
    res.json({ success: true, data: page });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: search
app.post('/tools/search', async (req, res) => {
  try {
    const { query } = req.body;
    const results = await notionClient.search({ query });
    res.json({ success: true, data: results });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// List available tools
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { name: 'get_page', description: 'Get a Notion page by ID' },
      { name: 'get_blocks', description: 'Get blocks from a Notion page' },
      { name: 'create_page', description: 'Create a new Notion page' },
      { name: 'search', description: 'Search Notion workspace' }
    ]
  });
});

app.listen(port, () => {
  console.log(`MCP Notion server listening on port ${port}`);
});
