"""OpenHands executor implementation"""

import os
import httpx
from typing import Dict, Any, AsyncIterator
from src.interfaces import Executor, ExecutorStatus, ExecutorArtifacts


class OpenHandsExecutor(Executor):
    """
    OpenHands executor adapter.
    
    Implements the standard Executor interface.
    Can be swapped with ClaudeCodeExecutor or CodexExecutor later.
    """
    
    def __init__(self, url: str = None):
        self.url = url or os.getenv("OPENHANDS_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient(base_url=self.url, timeout=300.0)
    
    @property
    def name(self) -> str:
        return "openhands"
    
    async def start(self, task: Dict[str, Any]) -> str:
        """
        Start OpenHands execution.
        
        Args:
            task: {
                "repo": "drafted/drafted-web",
                "instruction": "Fix the mobile layout bug",
                "constraints": ["no breaking changes", "add tests"],
                "branch_base": "main"
            }
        
        Returns:
            run_id for tracking
        """
        response = await self.client.post("/api/runs", json={
            "repository": task["repo"],
            "instruction": task["instruction"],
            "constraints": task.get("constraints", []),
            "branch_base": task.get("branch_base", "main"),
        })
        response.raise_for_status()
        
        data = response.json()
        return data["run_id"]
    
    async def get_status(self, run_id: str) -> ExecutorStatus:
        """Get current status"""
        response = await self.client.get(f"/api/runs/{run_id}")
        response.raise_for_status()
        
        data = response.json()
        status = data["status"]
        
        # Map OpenHands status to our ExecutorStatus
        status_map = {
            "queued": ExecutorStatus.QUEUED,
            "running": ExecutorStatus.RUNNING,
            "completed": ExecutorStatus.COMPLETED,
            "failed": ExecutorStatus.FAILED,
            "cancelled": ExecutorStatus.CANCELLED,
        }
        
        return status_map.get(status, ExecutorStatus.RUNNING)
    
    async def stream_logs(self, run_id: str) -> AsyncIterator[str]:
        """Stream logs from the executor"""
        async with self.client.stream("GET", f"/api/runs/{run_id}/logs") as response:
            async for line in response.aiter_lines():
                yield line
    
    async def get_artifacts(self, run_id: str) -> ExecutorArtifacts:
        """Get all artifacts produced by the run"""
        response = await self.client.get(f"/api/runs/{run_id}/artifacts")
        response.raise_for_status()
        
        data = response.json()
        
        return ExecutorArtifacts(
            patch=data.get("patch"),
            pr_url=data.get("pr_url"),
            logs=data.get("logs", []),
            test_report=data.get("test_report"),
            deploy_url=data.get("deploy_url"),
            files_changed=data.get("files_changed", [])
        )
    
    async def cancel(self, run_id: str) -> bool:
        """Cancel a running execution"""
        try:
            response = await self.client.post(f"/api/runs/{run_id}/cancel")
            response.raise_for_status()
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
