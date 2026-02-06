#!/usr/bin/env python3
"""Test GitHub API token"""

import os
import sys
from dotenv import load_dotenv
from github import Github, GithubException

# Load environment variables
load_dotenv()

def test_github():
    """Test GitHub API token"""
    print("🧪 Testing GitHub Token...")
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found in environment")
        return False
    
    print(f"   Token: {token[:20]}...")
    
    try:
        client = Github(token)
        
        # Get authenticated user
        user = client.get_user()
        print(f"   Authenticated as: {user.login}")
        
        # Try to access drafted org
        org = os.getenv("GITHUB_ORG", "drafted")
        try:
            org_obj = client.get_organization(org)
            print(f"   Organization: {org_obj.name or org}")
            
            # List a few repos
            repos = list(org_obj.get_repos()[:3])
            print(f"   Accessible repos: {len(repos)}")
            for repo in repos:
                print(f"     - {repo.name}")
            
        except GithubException as e:
            print(f"   ⚠️  Cannot access org '{org}': {e.data.get('message', str(e))}")
            print("   (This is OK if you're using a personal token)")
        
        # Check rate limit
        try:
            rate = client.get_rate_limit()
            core_rate = rate.core if hasattr(rate, 'core') else rate
            remaining = core_rate.remaining if hasattr(core_rate, 'remaining') else 'unknown'
            limit = core_rate.limit if hasattr(core_rate, 'limit') else 'unknown'
            print(f"   Rate limit: {remaining}/{limit}")
        except Exception as e:
            print(f"   Rate limit: (unable to check - {str(e)[:50]})")
        
        print("✅ GitHub token is VALID")
        return True
        
    except Exception as e:
        print(f"❌ GitHub API test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_github()
    sys.exit(0 if success else 1)
