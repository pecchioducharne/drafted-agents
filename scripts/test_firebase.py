#!/usr/bin/env python3
"""Test Firebase Admin SDK"""

import os
import sys
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

def test_firebase():
    """Test Firebase Admin SDK"""
    print("🧪 Testing Firebase Admin SDK...")
    
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    
    if not project_id:
        print("❌ FIREBASE_PROJECT_ID not found in environment")
        return False
    
    if not service_account:
        print("❌ FIREBASE_SERVICE_ACCOUNT_JSON not found in environment")
        return False
    
    print(f"   Project ID: {project_id}")
    
    try:
        # Parse service account JSON
        if service_account.startswith("{"):
            cred_dict = json.loads(service_account)
        else:
            print("❌ FIREBASE_SERVICE_ACCOUNT_JSON should be a JSON string")
            return False
        
        print(f"   Service account: {cred_dict.get('client_email', 'Unknown')}")
        
        # Initialize Firebase Admin
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        
        # Test Firestore connection
        db = firestore.client()
        
        # Try to list collections (this validates access)
        collections = list(db.collections())
        print(f"   Collections accessible: {len(collections)}")
        
        if collections:
            print("   Available collections:")
            for col in collections[:5]:  # Show first 5
                print(f"     - {col.id}")
        
        # Try to read from a collection (if exists)
        if collections:
            test_col = collections[0]
            docs = list(test_col.limit(1).stream())
            print(f"   Test read from '{test_col.id}': {'✓' if docs else 'empty'}")
        
        print("✅ Firebase Admin SDK is VALID")
        return True
        
    except Exception as e:
        print(f"❌ Firebase Admin SDK test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_firebase()
    sys.exit(0 if success else 1)
