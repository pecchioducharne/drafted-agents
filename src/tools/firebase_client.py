"""Firebase Admin client for restricted operations"""

import os
import json
from typing import Dict, List, Optional, Any
import firebase_admin
from firebase_admin import credentials, firestore


# Allowlists for safety
ALLOWED_COLLECTIONS = [
    "candidates",
    "jobs",
    "matches",
    "analytics",
    "agent_logs"
]

READ_ONLY_COLLECTIONS = [
    "candidates",
    "jobs",
    "matches"
]

WRITE_ALLOWED_COLLECTIONS = [
    "analytics",
    "agent_logs"
]


class FirebaseClient:
    """
    Firebase Admin client with restricted access.
    
    Enforces collection-level allowlists for safety.
    """
    
    def __init__(self):
        if not firebase_admin._apps:
            # Initialize Firebase Admin
            service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            
            if service_account:
                if service_account.startswith("{"):
                    # JSON string
                    cred_dict = json.loads(service_account)
                    cred = credentials.Certificate(cred_dict)
                else:
                    # File path
                    cred = credentials.Certificate(service_account)
                
                firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    def _check_collection_access(self, collection: str, write: bool = False):
        """Verify collection access is allowed"""
        if collection not in ALLOWED_COLLECTIONS:
            raise PermissionError(f"Collection '{collection}' not in allowlist")
        
        if write and collection not in WRITE_ALLOWED_COLLECTIONS:
            raise PermissionError(f"Write access to '{collection}' not allowed")
    
    async def read_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Read a single document"""
        self._check_collection_access(collection, write=False)
        
        doc_ref = self.db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None
    
    async def read_collection(
        self,
        collection: str,
        limit: int = 100,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Read documents from a collection"""
        self._check_collection_access(collection, write=False)
        
        query = self.db.collection(collection)
        
        if where:
            query = query.where(
                where.get("field"),
                where.get("operator", "=="),
                where.get("value")
            )
        
        query = query.limit(limit)
        docs = query.stream()
        
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    
    async def write_document(
        self,
        collection: str,
        data: Dict[str, Any],
        doc_id: Optional[str] = None
    ) -> str:
        """Write a document (only to allowed collections)"""
        self._check_collection_access(collection, write=True)
        
        if doc_id:
            doc_ref = self.db.collection(collection).document(doc_id)
        else:
            doc_ref = self.db.collection(collection).document()
        
        doc_ref.set(data, merge=True)
        return doc_ref.id
    
    async def log_agent_action(self, action: Dict[str, Any]) -> str:
        """Log agent action for audit trail"""
        return await self.write_document("agent_logs", action)
