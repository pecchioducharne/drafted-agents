#!/usr/bin/env python3
"""Helper script to understand Notion access and suggest what to share"""

import os
from dotenv import load_dotenv
from notion_client import Client
from collections import defaultdict

load_dotenv()

def analyze_notion_access():
    """Analyze current Notion access and provide recommendations"""
    
    token = os.getenv("NOTION_TOKEN")
    if not token:
        print("❌ NOTION_TOKEN not found in .env")
        return
    
    client = Client(auth=token)
    
    print("🔍 Analyzing Notion Access...")
    print("=" * 60)
    
    # Search for all accessible content
    try:
        response = client.search(query="", page_size=100)
        results = response.get("results", [])
        
        print(f"\n📊 Currently Accessible Items: {len(results)}")
        
        if len(results) == 0:
            print("\n⚠️  NO PAGES ARE CURRENTLY SHARED")
            print("\n💡 RECOMMENDATION:")
            print("   Grant access to your top-level workspace pages.")
            print("   This will give access to all nested pages underneath.")
            print("\n📝 HOW TO SHARE:")
            print("   1. Open Notion in browser")
            print("   2. Find your main workspace pages (top of sidebar)")
            print("   3. For each top-level page:")
            print("      - Click ••• menu → Connections")
            print("      - Add 'Drafted Brain'")
            print("\n   Typical workspaces have 3-10 top-level pages.")
            print("   Sharing these will give access to all child pages.")
            return
        
        # Categorize by type
        by_type = defaultdict(list)
        for item in results:
            item_type = item.get("object")
            title = extract_title(item)
            by_type[item_type].append({
                "id": item["id"],
                "title": title,
                "url": item.get("url", ""),
                "last_edited": item.get("last_edited_time", "")
            })
        
        # Show summary
        print("\n📋 Breakdown by Type:")
        for item_type, items in by_type.items():
            print(f"   {item_type}: {len(items)}")
        
        # Show pages
        if "page" in by_type:
            print(f"\n📄 Accessible Pages ({len(by_type['page'])}):")
            for page in by_type["page"][:20]:  # Show first 20
                print(f"   • {page['title']}")
                print(f"     {page['url']}")
            
            if len(by_type["page"]) > 20:
                print(f"   ... and {len(by_type['page']) - 20} more")
        
        # Show databases
        if "database" in by_type:
            print(f"\n🗄️  Accessible Databases ({len(by_type['database'])}):")
            for db in by_type["database"][:10]:  # Show first 10
                print(f"   • {db['title']}")
                print(f"     {db['url']}")
            
            if len(by_type["database"]) > 10:
                print(f"   ... and {len(by_type['database']) - 10} more")
        
        # Recommendations
        print("\n" + "=" * 60)
        print("💡 RECOMMENDATIONS:")
        print("=" * 60)
        
        if len(results) < 10:
            print("\n⚠️  Limited access detected")
            print("   Consider sharing more top-level pages to give agents")
            print("   broader context about your workspace.")
        else:
            print("\n✅ Good access level")
            print("   Agents can search and read from your shared pages.")
        
        print("\n📝 TO SHARE MORE PAGES:")
        print("   1. Identify top-level pages you want agents to access")
        print("   2. For each page: ••• → Connections → Add 'Drafted Brain'")
        print("   3. Run this script again to verify")
        
        print("\n🔒 SECURITY NOTE:")
        print("   Only share pages that agents should access.")
        print("   Private/sensitive pages will remain private unless shared.")
        
        # Test search functionality
        print("\n" + "=" * 60)
        print("🧪 Testing Search Functionality")
        print("=" * 60)
        
        test_queries = ["project", "doc", "task"]
        for query in test_queries:
            search_results = client.search(query=query, page_size=3)
            count = len(search_results.get("results", []))
            print(f"   '{query}': {count} results")
        
        print("\n✅ Notion integration is working!")
        print("   Agents can search and read shared pages.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def extract_title(obj):
    """Extract title from a Notion object"""
    properties = obj.get("properties", {})
    
    # Try different title property names
    for key in ["title", "Title", "Name", "name"]:
        if key in properties:
            title_prop = properties[key]
            if title_prop.get("type") == "title" and title_prop.get("title"):
                return title_prop["title"][0].get("plain_text", "Untitled")
    
    # Fallback for databases
    if "title" in obj and obj["title"]:
        return obj["title"][0].get("plain_text", "Untitled")
    
    return "Untitled"


if __name__ == "__main__":
    analyze_notion_access()
