"""Notion read skill - search and fetch documentation"""

from typing import Dict, Any, List
from src.interfaces import Skill, SkillResult, SkillStatus, TaskContext
from src.tools.notion_client import NotionClient


class NotionReadSkill(Skill):
    """
    Search and read Notion pages for context and documentation.
    
    Use cases:
    - Find relevant runbooks
    - Get project documentation
    - Search for prior decisions
    """
    
    def __init__(self):
        self.notion = NotionClient()
    
    @property
    def name(self) -> str:
        return "notion_read"
    
    @property
    def description(self) -> str:
        return "Search and read Notion pages for documentation and context"
    
    @property
    def inputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "page_id": {"type": "string"},
                "include_content": {"type": "boolean", "default": True}
            }
        }
    
    @property
    def outputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pages": {"type": "array"},
                "content": {"type": "string"}
            }
        }
    
    @property
    def allowed_tools(self) -> List[str]:
        return ["notion"]
    
    @property
    def success_checks(self) -> List[str]:
        return ["pages_found_or_fetched"]
    
    async def run(self, context: TaskContext) -> SkillResult:
        """Search or read Notion pages"""
        logs = []
        outputs = {}
        artifacts = {}
        
        try:
            # If page_id provided, fetch specific page
            if context.outputs.get("notion_page_id"):
                page_id = context.outputs["notion_page_id"]
                logs.append(f"Fetching Notion page {page_id}...")
                
                page = await self.notion.get_page(page_id)
                content = await self.notion.get_page_content(page_id)
                
                outputs["page"] = page
                outputs["content"] = content
                
                logs.append(f"✓ Page: {page['title']}")
                logs.append(f"  Content length: {len(content)} chars")
                
            # Otherwise, search
            elif context.request:
                query = context.request
                logs.append(f"Searching Notion for: {query}")
                
                results = await self.notion.search(query, limit=5)
                outputs["pages"] = results
                
                logs.append(f"✓ Found {len(results)} pages")
                for page in results:
                    logs.append(f"  - {page['title']} ({page['type']})")
                
                # Optionally fetch content of first result
                if results and context.outputs.get("include_content", True):
                    first_page = results[0]
                    logs.append(f"\nFetching content of: {first_page['title']}")
                    
                    content = await self.notion.get_page_content(first_page["id"])
                    outputs["content"] = content
                    
                    logs.append(f"✓ Content length: {len(content)} chars")
            
            # Update task context
            if not context.metadata:
                context.metadata = {}
            context.metadata["notion_context"] = outputs
            
            return SkillResult(
                status=SkillStatus.SUCCESS,
                outputs=outputs,
                artifacts=artifacts,
                logs=logs
            )
            
        except Exception as e:
            logs.append(f"✗ Error: {str(e)}")
            return SkillResult(
                status=SkillStatus.FAILED,
                outputs=outputs,
                artifacts=artifacts,
                logs=logs,
                error=str(e)
            )
