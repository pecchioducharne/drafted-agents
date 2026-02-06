#!/usr/bin/env python3
"""Test Netlify API token"""

import os
import sys
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

def test_netlify():
    """Test Netlify API token"""
    print("🧪 Testing Netlify Token...")
    
    token = os.getenv("NETLIFY_AUTH_TOKEN")
    site_id = os.getenv("NETLIFY_SITE_ID")
    
    if not token:
        print("❌ NETLIFY_AUTH_TOKEN not found in environment")
        return False
    
    if not site_id:
        print("❌ NETLIFY_SITE_ID not found in environment")
        return False
    
    print(f"   Token: {token[:20]}...")
    print(f"   Site ID: {site_id}")
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test 1: Get account info
        response = httpx.get(
            "https://api.netlify.com/api/v1/accounts",
            headers=headers,
            timeout=10.0
        )
        response.raise_for_status()
        accounts = response.json()
        
        if accounts:
            print(f"   Account: {accounts[0].get('name', 'Unknown')}")
        
        # Test 2: Get site info
        response = httpx.get(
            f"https://api.netlify.com/api/v1/sites/{site_id}",
            headers=headers,
            timeout=10.0
        )
        response.raise_for_status()
        site = response.json()
        
        print(f"   Site name: {site.get('name', 'Unknown')}")
        print(f"   Site URL: {site.get('url', 'Unknown')}")
        print(f"   State: {site.get('state', 'Unknown')}")
        
        # Test 3: List recent deploys
        response = httpx.get(
            f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
            headers=headers,
            params={"per_page": 3},
            timeout=10.0
        )
        response.raise_for_status()
        deploys = response.json()
        
        print(f"   Recent deploys: {len(deploys)}")
        if deploys:
            latest = deploys[0]
            print(f"     Latest: {latest.get('state')} - {latest.get('created_at', 'Unknown')[:10]}")
        
        print("✅ Netlify token is VALID")
        return True
        
    except httpx.HTTPStatusError as e:
        print(f"❌ Netlify API test FAILED: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Netlify API test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_netlify()
    sys.exit(0 if success else 1)
