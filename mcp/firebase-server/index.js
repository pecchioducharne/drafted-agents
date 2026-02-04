const express = require('express');
const admin = require('firebase-admin');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3004;

app.use(express.json());

// Initialize Firebase Admin
const serviceAccount = require(process.env.FIREBASE_SERVICE_ACCOUNT_PATH || '/secrets/firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: process.env.FIREBASE_PROJECT_ID
});

const db = admin.firestore();

// Allowed collections (enforce scoping)
const ALLOWED_COLLECTIONS = ['candidates', 'jobs', 'matches', 'analytics', 'agent_logs'];

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mcp-firebase' });
});

// MCP tool: read_collection
app.post('/tools/read_collection', async (req, res) => {
  try {
    const { collection, limit = 100, where } = req.body;
    
    if (!ALLOWED_COLLECTIONS.includes(collection)) {
      return res.status(403).json({ 
        success: false, 
        error: `Access to collection '${collection}' is not allowed` 
      });
    }
    
    let query = db.collection(collection);
    
    if (where) {
      query = query.where(where.field, where.operator, where.value);
    }
    
    const snapshot = await query.limit(limit).get();
    const docs = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    
    res.json({ success: true, data: docs });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: read_document
app.post('/tools/read_document', async (req, res) => {
  try {
    const { collection, document_id } = req.body;
    
    if (!ALLOWED_COLLECTIONS.includes(collection)) {
      return res.status(403).json({ 
        success: false, 
        error: `Access to collection '${collection}' is not allowed` 
      });
    }
    
    const doc = await db.collection(collection).doc(document_id).get();
    
    if (!doc.exists) {
      return res.status(404).json({ success: false, error: 'Document not found' });
    }
    
    res.json({ success: true, data: { id: doc.id, ...doc.data() } });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// MCP tool: write_document (restricted to agent_logs and analytics)
app.post('/tools/write_document', async (req, res) => {
  try {
    const { collection, document_id, data } = req.body;
    
    const WRITE_ALLOWED = ['analytics', 'agent_logs'];
    
    if (!WRITE_ALLOWED.includes(collection)) {
      return res.status(403).json({ 
        success: false, 
        error: `Write access to collection '${collection}' is not allowed` 
      });
    }
    
    const docRef = document_id 
      ? db.collection(collection).doc(document_id)
      : db.collection(collection).doc();
    
    await docRef.set(data, { merge: true });
    
    res.json({ success: true, data: { id: docRef.id } });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// List available tools
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { name: 'read_collection', description: 'Read documents from a Firestore collection' },
      { name: 'read_document', description: 'Read a specific Firestore document' },
      { name: 'write_document', description: 'Write to agent_logs or analytics collections' }
    ],
    allowed_collections: ALLOWED_COLLECTIONS
  });
});

app.listen(port, () => {
  console.log(`MCP Firebase server listening on port ${port}`);
});
