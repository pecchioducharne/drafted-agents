"""
Router - determines persona + skills for a task using LLM
"""

import os
from typing import Dict, Any
from anthropic import Anthropic
from src.interfaces import TaskContext


class Router:
    """
    Routes tasks to appropriate persona + skills using Claude.
    
    This is where the "brain" decides what to do.
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
    
    async def route(self, context: TaskContext) -> Dict[str, Any]:
        """
        Determine routing for a task.
        
        Returns:
            {
                "persona": "coder",
                "skills": ["github_context", "openhands_pr", "netlify_deploy"],
                "executor": "openhands",
                "reasoning": "..."
            }
        """
        
        # Build routing prompt
        prompt = self._build_routing_prompt(context)
        
        # Call Claude for routing decision
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response
        response_text = message.content[0].text
        
        # Simple parsing (in production, use structured output)
        routing = self._parse_routing_response(response_text, context)
        
        return routing
    
    def _build_routing_prompt(self, context: TaskContext) -> str:
        """Build the routing prompt for Claude"""
        return f"""You are the routing brain for an agent system. Given a task, decide:
1. Which persona should handle it
2. Which skills are needed
3. Which executor to use (if code changes needed)

Task: {context.request}
Repo: {context.repo}
Issue: #{context.issue} (if applicable)
Constraints: {', '.join(context.constraints) if context.constraints else 'none'}

Available personas:
- researcher: Evidence-first investigation, no code changes
- debugger: Reproduce bugs, identify root cause
- coder: Implement features/fixes with tests
- breaker: Adversarial testing, security checks
- communicator: Summaries, PR descriptions

Available skills:
- github_context: Fetch issue/PR/file context
- netlify_deploy: Get deploy preview URL
- openhands_pr: Execute code changes (uses OpenHands)

Respond in this format:
PERSONA: <persona_name>
SKILLS: <skill1>, <skill2>, <skill3>
EXECUTOR: <executor_name> (or "none" if no code changes)
REASONING: <why these choices>"""
    
    def _parse_routing_response(self, response: str, context: TaskContext) -> Dict[str, Any]:
        """Parse Claude's routing response"""
        lines = response.strip().split('\n')
        
        routing = {
            "persona": "coder",  # default
            "skills": ["github_context"],  # default
            "executor": "openhands",  # default
            "reasoning": ""
        }
        
        for line in lines:
            if line.startswith("PERSONA:"):
                routing["persona"] = line.split(":", 1)[1].strip().lower()
            elif line.startswith("SKILLS:"):
                skills_str = line.split(":", 1)[1].strip()
                routing["skills"] = [s.strip() for s in skills_str.split(",")]
            elif line.startswith("EXECUTOR:"):
                executor = line.split(":", 1)[1].strip().lower()
                routing["executor"] = executor if executor != "none" else None
            elif line.startswith("REASONING:"):
                routing["reasoning"] = line.split(":", 1)[1].strip()
        
        return routing
