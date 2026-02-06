"""
Job processor - executes agent tasks asynchronously
"""

import asyncio
from typing import Dict, Any
from src.interfaces import TaskContext, SkillRegistry, ExecutorRegistry
from src.skills.github_context import GitHubContextSkill
from src.skills.netlify_deploy import NetlifyDeploySkill
from src.skills.notion_read import NotionReadSkill
from src.skills.notion_write import NotionWriteSkill
from src.openhands.executor import OpenHandsExecutor
from src.worker.router import Router


# Initialize registries
skill_registry = SkillRegistry()
executor_registry = ExecutorRegistry()

# Register skills
skill_registry.register(GitHubContextSkill())
skill_registry.register(NetlifyDeploySkill())
skill_registry.register(NotionReadSkill())
skill_registry.register(NotionWriteSkill())
# TODO: Add more skills as needed

# Register executors
executor_registry.register(OpenHandsExecutor(), is_default=True)
# TODO: Add ClaudeCodeExecutor, CodexExecutor later


def process_job(context_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a job synchronously (called by RQ worker).
    
    This wraps the async processing logic.
    """
    # Convert dict back to TaskContext
    context = TaskContext(**context_dict)
    
    # Run async processing
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_process_job_async(context))
    
    return result


async def _process_job_async(context: TaskContext) -> Dict[str, Any]:
    """
    Async job processing logic.
    
    1. Route to persona + skills
    2. Execute skills in sequence
    3. Return results
    """
    logs = []
    
    try:
        logs.append(f"Processing job {context.task_id}")
        logs.append(f"Request: {context.request}")
        
        # Step 1: Route to persona + skills
        router = Router()
        routing = await router.route(context)
        
        context.persona = routing["persona"]
        context.skills = routing["skills"]
        context.executor = routing.get("executor", "openhands")
        
        logs.append(f"✓ Routed to persona: {context.persona}")
        logs.append(f"✓ Skills: {', '.join(context.skills)}")
        
        # Step 2: Execute skills in sequence
        for skill_name in context.skills:
            logs.append(f"\n→ Executing skill: {skill_name}")
            
            skill = skill_registry.get(skill_name)
            if not skill:
                logs.append(f"✗ Skill '{skill_name}' not found")
                continue
            
            result = await skill.run(context)
            
            # Add skill logs
            logs.extend([f"  {log}" for log in result.logs])
            
            # Update context with outputs
            context.outputs.update(result.outputs)
            context.artifacts.update(result.artifacts)
            
            if result.status.value != "success":
                logs.append(f"✗ Skill failed: {result.error}")
                break
        
        # Step 3: Return final result
        logs.append(f"\n✓ Job completed successfully")
        
        return {
            "status": "completed",
            "task_id": context.task_id,
            "persona": context.persona,
            "skills_executed": context.skills,
            "outputs": context.outputs,
            "artifacts": context.artifacts,
            "logs": logs
        }
        
    except Exception as e:
        logs.append(f"\n✗ Job failed with error: {str(e)}")
        
        return {
            "status": "failed",
            "task_id": context.task_id,
            "error": str(e),
            "logs": logs
        }
