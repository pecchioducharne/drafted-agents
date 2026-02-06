#!/usr/bin/env python3
"""Test Notion API token"""

import os
import sys
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError

# Load environment variables
load_dotenv()

def test_notion():
    """Test Notion API token"""
    print("🧪 Testing Notion Token...")
    
    token = os.getenv("NOTION_TOKEN")
    if not token:
        print("❌ NOTION_TOKEN not found in environment")
        return False
    
    print(f"   Token: {token[:20]}...")
    
    try:
        client = Client(auth=token)
        
        # Test 1: Search workspace
        print("   Testing search...")
        response = client.search(query="", page_size=5)
        
        results = response.get("results", [])
        print(f"   Accessible pages/databases: {len(results)}")
        
        if results:
            print("   Sample pages:")
            for item in results[:3]:
                title = "Untitled"
                if "properties" in item:
                    props = item["properties"]
                    for key in ["title", "Title", "Name", "name"]:
                        if key in props and props[key].get("title"):
                            title = props[key]["title"][0].get("plain_text", "Untitled")
                            break
                
                print(f"     - {title} ({item['object']})")
        
        # Check if we have access to any pages
        if len(results) == 0:
            print("\n⚠️  Notion token is VALID but no pages are shared with the integration")
            print("   To grant access:")
            print("   1. Open a Notion page")
            print("   2. Click '•••' menu → 'Connections'")
            print("   3. Add 'Drafted Brain' integration")
            print("\n✅ Notion token authentication is VALID")
            print("   (Just needs page access to be useful)")
            return True
        
        print("\n✅ Notion token is VALID")
        print(f"   Total accessible items: {len(results)}")
        return True
        
    except APIResponseError as e:
        error_msg = str(e)
        print(f"❌ Notion API test FAILED: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ Notion API test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_notion()
    sys.exit(0 if success else 1)
