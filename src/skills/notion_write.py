"""Notion write skill - create pages and summaries"""

from typing import Dict, Any, List
from src.interfaces import Skill, SkillResult, SkillStatus, TaskContext
from src.tools.notion_client import NotionClient


class NotionWriteSkill(Skill):
    """
    Create pages and write summaries to Notion.
    
    Use cases:
    - Create research memos
    - Document decisions
    - Write project summaries
    - Link PRs and tickets
    """
    
    def __init__(self):
        self.notion = NotionClient()
    
    @property
    def name(self) -> str:
        return "notion_write"
    
    @property
    def description(self) -> str:
        return "Create pages and write summaries to Notion"
    
    @property
    def inputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "parent_id": {"type": "string"},
                "title": {"type": "string"},
                "content": {"type": "string"},
                "append_to": {"type": "string"}
            }
        }
    
    @property
    def outputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "page_id": {"type": "string"},
                "page_url": {"type": "string"}
            }
        }
    
    @property
    def allowed_tools(self) -> List[str]:
        return ["notion"]
    
    @property
    def success_checks(self) -> List[str]:
        return ["page_created_or_updated"]
    
    async def run(self, context: TaskContext) -> SkillResult:
        """Create or update Notion pages"""
        logs = []
        outputs = {}
        artifacts = {}
        
        try:
            # Get parent page (use root if not specified)
            parent_id = context.outputs.get("notion_parent_id") or self.notion.root_page_id
            
            if not parent_id:
                raise ValueError("No parent page ID specified and NOTION_ROOT_PAGE_ID not set")
            
            # Generate title from context
            title = context.outputs.get("notion_title") or f"Agent Summary: {context.task_id}"
            
            # Generate content from task outputs
            content_blocks = self._build_content_blocks(context)
            
            logs.append(f"Creating Notion page: {title}")
            logs.append(f"Parent: {parent_id}")
            
            # Create page
            page = await self.notion.create_page(
                parent_id=parent_id,
                title=title,
                content=content_blocks
            )
            
            outputs["page_id"] = page["id"]
            outputs["page_url"] = page["url"]
            artifacts["notion_page"] = page["url"]
            
            logs.append(f"✓ Page created: {page['url']}")
            
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
    
    def _build_content_blocks(self, context: TaskContext) -> List[Dict[str, Any]]:
        """Build Notion blocks from task context"""
        blocks = []
        
        # Add request
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Request"}}]
            }
        })
        
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": context.request}}]
            }
        })
        
        # Add outputs if available
        if context.outputs:
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Results"}}]
                }
            })
            
            # Add PR link if available
            if context.outputs.get("pr_url"):
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"PR: {context.outputs['pr_url']}"}
                        }]
                    }
                })
            
            # Add deploy URL if available
            if context.outputs.get("deploy_url"):
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"Deploy: {context.outputs['deploy_url']}"}
                        }]
                    }
                })
        
        return blocks
