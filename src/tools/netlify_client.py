"""Netlify API client for deploy operations"""

import os
import httpx
from typing import Dict, Optional, Any
import asyncio


class NetlifyClient:
    """
    Netlify operations for agents.
    
    Handles deploy previews and build status.
    """
    
    def __init__(self, token: Optional[str] = None, site_id: Optional[str] = None):
        self.token = token or os.getenv("NETLIFY_AUTH_TOKEN")
        self.site_id = site_id or os.getenv("NETLIFY_SITE_ID")
        self.base_url = "https://api.netlify.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
    
    async def get_site(self) -> Dict[str, Any]:
        """Get site information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sites/{self.site_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def list_deploys(self, limit: int = 10) -> list[Dict[str, Any]]:
        """List recent deploys"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sites/{self.site_id}/deploys",
                headers=self.headers,
                params={"per_page": limit}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_deploy(self, deploy_id: str) -> Dict[str, Any]:
        """Get deploy details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/deploys/{deploy_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_deploy_for_pr(self, pr_number: int, max_wait: int = 60) -> Optional[Dict[str, Any]]:
        """
        Find deploy preview for a PR.
        
        Polls for up to max_wait seconds.
        """
        for _ in range(max_wait // 5):
            deploys = await self.list_deploys(limit=50)
            
            # Look for deploy with PR context
            for deploy in deploys:
                context = deploy.get("context", "")
                deploy_pr = deploy.get("branch", "")
                
                if f"pr-{pr_number}" in context.lower() or f"pull/{pr_number}" in deploy_pr:
                    return {
                        "id": deploy["id"],
                        "url": deploy.get("deploy_ssl_url") or deploy.get("ssl_url"),
                        "state": deploy["state"],
                        "created_at": deploy["created_at"],
                        "published_at": deploy.get("published_at"),
                    }
            
            await asyncio.sleep(5)
        
        return None
    
    async def trigger_build(self) -> Dict[str, Any]:
        """Trigger a new build"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sites/{self.site_id}/builds",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def wait_for_deploy(self, deploy_id: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Wait for deploy to complete.
        
        Args:
            deploy_id: Deploy ID to watch
            timeout: Maximum seconds to wait
            
        Returns:
            Final deploy status
        """
        start_time = asyncio.get_event_loop().time()
        
        while True:
            deploy = await self.get_deploy(deploy_id)
            state = deploy["state"]
            
            if state in ["ready", "error"]:
                return deploy
            
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Deploy {deploy_id} did not complete within {timeout}s")
            
            await asyncio.sleep(10)
