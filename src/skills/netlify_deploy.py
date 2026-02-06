"""Netlify deploy preview skill"""

from typing import Dict, Any, List
from src.interfaces import Skill, SkillResult, SkillStatus, TaskContext
from src.tools.netlify_client import NetlifyClient


class NetlifyDeploySkill(Skill):
    """
    Get Netlify deploy preview URL for a PR.
    """
    
    def __init__(self):
        self.netlify = NetlifyClient()
    
    @property
    def name(self) -> str:
        return "netlify_deploy"
    
    @property
    def description(self) -> str:
        return "Get or wait for Netlify deploy preview URL"
    
    @property
    def inputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pr_number": {"type": "integer"},
                "wait": {"type": "boolean", "default": True},
                "max_wait": {"type": "integer", "default": 60}
            },
            "required": ["pr_number"]
        }
    
    @property
    def outputs_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "deploy_url": {"type": "string"},
                "deploy_id": {"type": "string"},
                "state": {"type": "string"}
            }
        }
    
    @property
    def allowed_tools(self) -> List[str]:
        return ["netlify"]
    
    @property
    def success_checks(self) -> List[str]:
        return ["deploy_url_found"]
    
    async def run(self, context: TaskContext) -> SkillResult:
        """Find deploy preview for PR"""
        logs = []
        outputs = {}
        artifacts = {}
        
        try:
            pr_number = context.outputs.get("pr_number") or context.pr
            
            if not pr_number:
                raise ValueError("PR number required")
            
            logs.append(f"Looking for deploy preview for PR #{pr_number}...")
            
            deploy = await self.netlify.get_deploy_for_pr(
                int(pr_number),
                max_wait=60
            )
            
            if deploy:
                outputs["deploy_url"] = deploy["url"]
                outputs["deploy_id"] = deploy["id"]
                outputs["state"] = deploy["state"]
                
                artifacts["deploy_url"] = deploy["url"]
                
                logs.append(f"✓ Deploy preview: {deploy['url']}")
                logs.append(f"  State: {deploy['state']}")
                
                # Update task context
                context.netlify_context = outputs
                
                return SkillResult(
                    status=SkillStatus.SUCCESS,
                    outputs=outputs,
                    artifacts=artifacts,
                    logs=logs
                )
            else:
                logs.append("✗ No deploy preview found yet")
                return SkillResult(
                    status=SkillStatus.FAILED,
                    outputs=outputs,
                    artifacts=artifacts,
                    logs=logs,
                    error="Deploy preview not found"
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
