# Notion Integration

## Overview

The Drafted Agents system now includes full Notion integration, allowing agents to:

- **Search** documentation and knowledge base
- **Read** pages and databases
- **Create** summaries and reports
- **Link** agent outputs to Notion pages

## Components Added

### 1. Notion Tool Client

**File**: `src/tools/notion_client.py`

Provides direct access to Notion API:

- `search(query)` - Search workspace
- `get_page(page_id)` - Fetch page details
- `get_page_content(page_id)` - Get page content as text
- `create_page(parent_id, title, content)` - Create new pages
- `append_blocks(page_id, blocks)` - Add content to pages
- `list_databases()` - List accessible databases
- `query_database(database_id, filter)` - Query database entries

### 2. Notion Skills

#### NotionReadSkill (`src/skills/notion_read.py`)

Search and read Notion pages for context:

```python
# Use cases:
- Find relevant runbooks
- Get project documentation
- Search for prior decisions
```

**Inputs**:
- `query`: Search query
- `page_id`: Specific page to fetch
- `include_content`: Whether to fetch full content

**Outputs**:
- `pages`: List of matching pages
- `content`: Page content as text

#### NotionWriteSkill (`src/skills/notion_write.py`)

Create pages and summaries:

```python
# Use cases:
- Create research memos
- Document decisions
- Write project summaries
- Link PRs and tickets
```

**Inputs**:
- `parent_id`: Parent page ID
- `title`: Page title
- `content`: Page content

**Outputs**:
- `page_id`: Created page ID
- `page_url`: Page URL

### 3. Configuration

**Environment Variables** (`.env`):

```bash
# Notion (documentation and knowledge base)
NOTION_TOKEN=ntn_m75769718089oem2yJNHhiKImP2nIeEGYYOBxiA3hs98UX
NOTION_ROOT_PAGE_ID=  # Optional: default parent for new pages
```

**Dependencies** (`requirements.txt`):

```
notion-client>=2.2.0
```

## Setup Instructions

### 1. Notion Integration Already Created

Your "Drafted Brain" integration is already set up with:
- Integration name: `Drafted Brain`
- Token: `ntn_m75769718089oem2yJNHhiKImP2nIeEGYYOBxiA3hs98UX`
- Capabilities: Read, Update, Insert content and comments

### 2. Grant Page Access

To allow agents to access Notion pages:

1. **Open any Notion page** you want agents to access
2. **Click the `•••` menu** (top right)
3. **Select "Connections"**
4. **Add "Drafted Brain"** integration

Repeat for each page/database you want to share.

### 3. Set Root Page (Optional)

If you want agents to create new pages in a specific location:

1. Share a parent page with the integration
2. Copy the page ID from the URL:
   ```
   https://notion.so/Your-Page-Title-abc123def456
                                      ^^^^^^^^^^^^
                                      This is the page ID
   ```
3. Add to `.env`:
   ```bash
   NOTION_ROOT_PAGE_ID=abc123def456
   ```

## Testing

### Test Notion Token

```bash
cd drafted-agents
source .venv/bin/activate
python scripts/test_notion.py
```

**Expected Output**:
```
🧪 Testing Notion Token...
   Token: ntn_m75769718089oem2...
   Testing search...
   Accessible pages/databases: 0

⚠️  Notion token is VALID but no pages are shared with the integration
   To grant access:
   1. Open a Notion page
   2. Click '•••' menu → 'Connections'
   3. Add 'Drafted Brain' integration

✅ Notion token authentication is VALID
   (Just needs page access to be useful)
```

Once you share pages, you'll see:
```
✅ Notion token is VALID
   Total accessible items: 5
   Sample pages:
     - Project Docs (page)
     - Tasks (database)
     - Meeting Notes (page)
```

### Test All Keys

```bash
python scripts/test_all_keys.py
```

## Usage Examples

### Example 1: Search Documentation

```bash
./scripts/cli.py submit \
  --job-type issue_to_pr \
  --request "Search Notion for deployment runbook"
```

The router will automatically select `notion_read` skill.

### Example 2: Create Summary

```bash
./scripts/cli.py submit \
  --job-type issue_to_pr \
  --request "Create PR for #123 and document in Notion"
```

The agent will:
1. Fetch issue context (GitHub)
2. Create PR (OpenHands)
3. Create Notion page (Notion Write) with PR link

### Example 3: Manual Skill Execution

```python
from src.skills.notion_read import NotionReadSkill
from src.interfaces import TaskContext

skill = NotionReadSkill()
context = TaskContext(
    task_id="test",
    job_type="manual",
    request="authentication best practices"
)

result = await skill.run(context)
print(result.outputs["content"])
```

## Architecture

### Extensibility Seams

Notion integration follows the three extensibility seams:

1. **Skill Registry**: New Notion skills can be added without modifying core
2. **Executor Interface**: Notion operations don't require executor changes
3. **Job Type Templates**: New workflows can combine Notion with other skills

### Skill Registration

Skills are registered in `src/worker/processor.py`:

```python
skill_registry.register(NotionReadSkill())
skill_registry.register(NotionWriteSkill())
```

### Router Integration

The router knows about Notion skills:

```python
Available skills:
- notion_read: Search and read Notion documentation
- notion_write: Create pages and summaries in Notion
```

## Security

### Token Storage

- **Current**: Hardcoded in `.env` for testing
- **Production**: Move to secrets manager (AWS Secrets Manager, GCP Secret Manager)

### Access Control

- Integration only accesses explicitly shared pages
- No access to private pages by default
- Workspace-level permissions managed in Notion

### Audit Trail

All agent actions are logged:
- Firebase: `agent_actions` collection
- Notion: Page history shows integration edits

## Common Workflows

### 1. Issue → PR → Notion Summary

```yaml
job_type: issue_to_pr_with_docs
skills:
  - github_context    # Fetch issue
  - openhands_pr      # Create PR
  - netlify_deploy    # Get preview
  - notion_write      # Document result
```

### 2. Research Task → Notion Memo

```yaml
job_type: research_memo
skills:
  - github_context    # Get repo context
  - notion_read       # Find related docs
  - notion_write      # Create memo
```

### 3. Bug Triage → Notion Runbook

```yaml
job_type: bug_triage
skills:
  - github_context    # Get issue/error
  - notion_read       # Search runbooks
  - notion_write      # Update runbook if needed
```

## Next Steps

1. **Share Pages**: Grant "Drafted Brain" access to relevant pages
2. **Set Root Page**: Configure `NOTION_ROOT_PAGE_ID` for new pages
3. **Test Integration**: Run `python scripts/test_notion.py` again
4. **Create Workflows**: Add Notion skills to job type templates

## Troubleshooting

### "No pages are shared"

**Solution**: Share pages with the integration (see Setup Instructions)

### "Invalid token"

**Solution**: Regenerate token in Notion integrations settings

### "Page not found"

**Solution**: Ensure the page is shared with "Drafted Brain" integration

### "Permission denied"

**Solution**: Check integration capabilities in Notion settings

## API Reference

### NotionClient Methods

```python
# Search
results = await client.search("query", limit=10)

# Get page
page = await client.get_page("page_id")
content = await client.get_page_content("page_id")

# Create page
page = await client.create_page(
    parent_id="parent_id",
    title="Page Title",
    content=[block_objects]
)

# Append content
await client.append_blocks("page_id", [block_objects])

# Databases
databases = await client.list_databases()
entries = await client.query_database("db_id", filter_obj)
```

### Block Objects

```python
# Heading
{
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "Title"}}]
    }
}

# Paragraph
{
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Text"}}]
    }
}
```

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [notion-client Python Library](https://github.com/ramnes/notion-sdk-py)
- [Drafted Agents Setup](./SETUP_SIMPLIFIED.md)
