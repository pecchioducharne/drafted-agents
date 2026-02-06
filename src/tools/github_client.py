"""GitHub API client for agent operations"""

import os
from typing import Dict, List, Optional, Any
from github import Github, GithubException


class GitHubClient:
    """
    GitHub operations for agents.
    
    Provides safe, scoped access to GitHub resources.
    """
    
    def __init__(self, token: Optional[str] = None, org: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.org = org or os.getenv("GITHUB_ORG", "drafted")
        self.client = Github(self.token)
    
    async def get_issue(self, repo: str, issue_number: int) -> Dict[str, Any]:
        """Fetch issue details"""
        try:
            repo_obj = self.client.get_repo(f"{self.org}/{repo}")
            issue = repo_obj.get_issue(issue_number)
            
            return {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [user.login for user in issue.assignees],
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "url": issue.html_url,
            }
        except GithubException as e:
            raise Exception(f"Failed to fetch issue: {e.data.get('message', str(e))}")
    
    async def search_code(self, query: str, repo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search code in repositories"""
        try:
            search_query = f"{query} repo:{self.org}/{repo}" if repo else f"{query} org:{self.org}"
            results = self.client.search_code(search_query)
            
            return [
                {
                    "path": item.path,
                    "repo": item.repository.name,
                    "url": item.html_url,
                    "sha": item.sha,
                }
                for item in results[:10]  # Limit to 10 results
            ]
        except GithubException as e:
            raise Exception(f"Code search failed: {e.data.get('message', str(e))}")
    
    async def get_file(self, repo: str, path: str, ref: str = "main") -> str:
        """Get file contents"""
        try:
            repo_obj = self.client.get_repo(f"{self.org}/{repo}")
            content = repo_obj.get_contents(path, ref=ref)
            
            if isinstance(content, list):
                raise Exception(f"Path {path} is a directory, not a file")
            
            return content.decoded_content.decode('utf-8')
        except GithubException as e:
            raise Exception(f"Failed to fetch file: {e.data.get('message', str(e))}")
    
    async def list_prs(self, repo: str, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """List pull requests"""
        try:
            repo_obj = self.client.get_repo(f"{self.org}/{repo}")
            prs = repo_obj.get_pulls(state=state)
            
            return [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "url": pr.html_url,
                    "author": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                }
                for pr in list(prs[:limit])
            ]
        except GithubException as e:
            raise Exception(f"Failed to list PRs: {e.data.get('message', str(e))}")
    
    async def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> Dict[str, Any]:
        """Create a pull request"""
        try:
            repo_obj = self.client.get_repo(f"{self.org}/{repo}")
            pr = repo_obj.create_pull(title=title, body=body, head=head, base=base)
            
            return {
                "number": pr.number,
                "title": pr.title,
                "url": pr.html_url,
                "state": pr.state,
            }
        except GithubException as e:
            raise Exception(f"Failed to create PR: {e.data.get('message', str(e))}")
    
    async def add_comment(self, repo: str, issue_number: int, comment: str) -> bool:
        """Add comment to issue or PR"""
        try:
            repo_obj = self.client.get_repo(f"{self.org}/{repo}")
            issue = repo_obj.get_issue(issue_number)
            issue.create_comment(comment)
            return True
        except GithubException as e:
            raise Exception(f"Failed to add comment: {e.data.get('message', str(e))}")
