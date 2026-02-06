# Notion Access Guide - Bulk Sharing Strategy

## The Problem

Notion doesn't provide a CLI or API method to bulk-grant integration access to all pages. This is intentional for security - integrations must be explicitly granted access.

## The Solution: Hierarchical Access

Instead of sharing hundreds of individual pages, share your **top-level workspace pages**. The integration automatically gets access to all nested child pages.

## Strategy: Share Top-Level Pages Only

### Step 1: Identify Your Top-Level Pages

Your top-level pages are the ones at the root of your Notion sidebar. Typical workspaces have 3-10 of these:

- 📋 Projects
- 📚 Documentation  
- 👥 Team
- 📝 Meeting Notes
- 🎯 Goals & OKRs
- 🗂️ Resources
- etc.

### Step 2: Share Each Top-Level Page

For **each** top-level page:

1. **Open the page** in Notion
2. **Click `•••` menu** (top right)
3. **Select "Connections"**
4. **Add "Drafted Brain"**

✅ Done! All child pages underneath are now accessible.

### Step 3: Verify Access

Run the helper script to see what's now accessible:

```bash
cd drafted-agents
source .venv/bin/activate
python scripts/notion_access_helper.py
```

You should see:
```
📊 Currently Accessible Items: 50+
✅ Good access level
```

## Why This Works

Notion's permission model is hierarchical:
- Grant access to parent page → child pages inherit access
- Share 5 top-level pages → potentially 100+ nested pages accessible
- No need to share each page individually

## Example Workspace Structure

```
Notion Workspace
├── 📋 Projects (SHARE THIS) ← Share once
│   ├── Project A
│   ├── Project B
│   └── Project C
├── 📚 Documentation (SHARE THIS) ← Share once
│   ├── API Docs
│   ├── Architecture
│   └── Runbooks
└── 👥 Team (SHARE THIS) ← Share once
    ├── Onboarding
    ├── Processes
    └── Team Directory
```

By sharing 3 top-level pages, you've given access to 9+ nested pages.

## What Gets Shared

When you share a page with "Drafted Brain":
- ✅ The page itself
- ✅ All child pages (nested underneath)
- ✅ All databases on those pages
- ✅ Content and properties

What stays private:
- ❌ Pages you don't explicitly share
- ❌ Private pages in your workspace
- ❌ Other users' private pages

## Security Best Practices

### Do Share:
- ✅ Project documentation
- ✅ Technical runbooks
- ✅ Architecture decisions
- ✅ Public team resources
- ✅ Process documentation

### Don't Share:
- ❌ Personal notes
- ❌ Sensitive HR information
- ❌ Financial data
- ❌ Private conversations
- ❌ Confidential strategy docs

## Helper Script

Use `scripts/notion_access_helper.py` to:
- See what's currently accessible
- Test search functionality
- Get recommendations
- Verify your setup

```bash
python scripts/notion_access_helper.py
```

## Alternative: Workspace-Level Access (Not Recommended)

Notion does support workspace-level integrations, but:
- ⚠️ Requires workspace admin
- ⚠️ Gives access to ALL pages (too broad)
- ⚠️ Less secure
- ⚠️ Not recommended for AI agents

**Recommendation**: Stick with page-level sharing for better security.

## Troubleshooting

### "Still showing 0 pages accessible"

**Solution**: Make sure you're sharing pages, not just viewing them. Look for the "Connections" option in the `•••` menu.

### "Can't find Drafted Brain in Connections"

**Solution**: The integration might not be visible yet. Try:
1. Refresh Notion
2. Check Settings → Integrations
3. Verify the integration is active

### "Some pages not showing up"

**Solution**: 
- Check if those pages are nested under a shared parent
- If not, share their parent page
- Run `notion_access_helper.py` to verify

## Quick Reference

```bash
# Check current access
python scripts/notion_access_helper.py

# Test Notion connection
python scripts/test_notion.py

# Test all integrations
python scripts/test_all_keys.py
```

## Summary

✅ **No CLI bulk-sharing** - Notion doesn't support this  
✅ **Solution**: Share top-level pages (3-10 pages typically)  
✅ **Result**: Access to all nested child pages  
✅ **Security**: Only share what agents need  
✅ **Verify**: Use `notion_access_helper.py`  

**Time investment**: 2-5 minutes to share top-level pages  
**Result**: Access to entire workspace structure
