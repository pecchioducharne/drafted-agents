"""GitHub context gathering skill"""

from typing import Dict, Any, List
from src.interfaces import Skill, SkillResult, SkillStatus, TaskContext
from src.tools.github_client import GitHubClient


class GitHubContextSkill(Skill):
    """
    Fetch GitHub context: issues, PRs, files, related code.
    
    Example of extensibility: just implement the Skill interface.
    """
    
    def __init__(self):
        self.github = GitHubClient()
    
    @property
    def name(self) -> str:
        return "github_context"
    
    @property
    def description(self) -> str:
        return "Fetch issue/PR details, related code, and context from GitHub"
    
    @property
    def inputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "issue": {"type": "integer"},
                "search_related": {"type": "boolean", "default": True}
            },
            "required": ["repo"]
        }
    
    @property
    def outputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "issue_data": {"type": "object"},
                "related_files": {"type": "array"},
                "recent_prs": {"type": "array"}
            }
        }
    
    @property
    def allowed_tools(self) -> List[str]:
        return ["github"]
    
    @property
    def success_checks(self) -> List[str]:
        return [
            "issue_data_fetched",
            "context_gathered"
        ]
    
    async def run(self, context: TaskContext) -> SkillResult:
        """Gather GitHub context"""
        logs = []
        outputs = {}
        artifacts = {}
        
        try:
            # Fetch issue if specified
            if context.issue:
                logs.append(f"Fetching issue #{context.issue}...")
                issue_data = await self.github.get_issue(context.repo, int(context.issue))
                outputs["issue_data"] = issue_data
                logs.append(f"✓ Issue: {issue_data['title']}")
                
                # Search for related code
                if issue_data.get("title"):
                    logs.append("Searching for related code...")
                    results = await self.github.search_code(
                        issue_data["title"],
                        repo=context.repo
                    )
                    outputs["related_files"] = results
                    logs.append(f"✓ Found {len(results)} related files")
            
            # Fetch recent PRs for context
            logs.append("Fetching recent PRs...")
            recent_prs = await self.github.list_prs(context.repo, limit=5)
            outputs["recent_prs"] = recent_prs
            logs.append(f"✓ Found {len(recent_prs)} recent PRs")
            
            # Update task context
            context.github_context = outputs
            
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
