const express = require('express');
const { WebClient } = require('@slack/web-api');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3003;

app.use(express.json());

// Initialize Slack client
const slackClient = new WebClient(process.env.SLACK_BOT_TOKEN);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mcp-slack' });
});

// MCP tool: post_message
app.post('/tools/post_message', async (req, res) => {
  try {
    const { channel, text, blocks } = req.body;
    const result = await slackClient.chat.postMessage({
      channel,
      text,
      blocks
    });
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: post_thread_reply
app.post('/tools/post_thread_reply', async (req, res) => {
  try {
    const { channel, thread_ts, text } = req.body;
    const result = await slackClient.chat.postMessage({
      channel,
      thread_ts,
      text
    });
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: add_reaction
app.post('/tools/add_reaction', async (req, res) => {
  try {
    const { channel, timestamp, name } = req.body;
    const result = await slackClient.reactions.add({
      channel,
      timestamp,
      name
    });
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// List available tools
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { name: 'post_message', description: 'Post a message to a Slack channel' },
      { name: 'post_thread_reply', description: 'Reply to a thread in Slack' },
      { name: 'add_reaction', description: 'Add a reaction to a message' }
    ]
  });
});

app.listen(port, () => {
  console.log(`MCP Slack server listening on port ${port}`);
});
