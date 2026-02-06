"""Notion API client for documentation and knowledge base operations"""

import os
from typing import Dict, List, Optional, Any
from notion_client import Client
from notion_client.errors import APIResponseError


class NotionClient:
    """
    Notion operations for agents.
    
    Provides access to pages, databases, and blocks.
    """
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("NOTION_TOKEN")
        self.client = Client(auth=self.token)
        self.root_page_id = os.getenv("NOTION_ROOT_PAGE_ID")
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search across Notion workspace.
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of matching pages/databases
        """
        try:
            response = self.client.search(
                query=query,
                page_size=limit
            )
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "id": item["id"],
                    "type": item["object"],
                    "title": self._extract_title(item),
                    "url": item.get("url"),
                    "last_edited": item.get("last_edited_time"),
                })
            
            return results
            
        except APIResponseError as e:
            raise Exception(f"Notion search failed: {e.message}")
    
    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Get page details.
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Page object with properties
        """
        try:
            page = self.client.pages.retrieve(page_id=page_id)
            
            return {
                "id": page["id"],
                "title": self._extract_title(page),
                "url": page.get("url"),
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time"),
                "properties": page.get("properties", {}),
            }
            
        except APIResponseError as e:
            raise Exception(f"Failed to get page: {e.message}")
    
    async def get_page_content(self, page_id: str) -> str:
        """
        Get page content as text.
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Page content as markdown-like text
        """
        try:
            blocks = self.client.blocks.children.list(block_id=page_id)
            
            content_parts = []
            for block in blocks.get("results", []):
                text = self._extract_block_text(block)
                if text:
                    content_parts.append(text)
            
            return "\n\n".join(content_parts)
            
        except APIResponseError as e:
            raise Exception(f"Failed to get page content: {e.message}")
    
    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new page.
        
        Args:
            parent_id: Parent page or database ID
            title: Page title
            content: Optional list of block objects
            
        Returns:
            Created page object
        """
        try:
            page_data = {
                "parent": {"page_id": parent_id},
                "properties": {
                    "title": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            }
            
            if content:
                page_data["children"] = content
            
            page = self.client.pages.create(**page_data)
            
            return {
                "id": page["id"],
                "title": title,
                "url": page.get("url"),
            }
            
        except APIResponseError as e:
            raise Exception(f"Failed to create page: {e.message}")
    
    async def append_blocks(self, page_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """
        Append blocks to a page.
        
        Args:
            page_id: Page to append to
            blocks: List of block objects
            
        Returns:
            True if successful
        """
        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            return True
            
        except APIResponseError as e:
            raise Exception(f"Failed to append blocks: {e.message}")
    
    async def list_databases(self) -> List[Dict[str, Any]]:
        """
        List databases in the workspace.
        
        Returns:
            List of database objects
        """
        try:
            response = self.client.search(
                filter={"property": "object", "value": "database"}
            )
            
            databases = []
            for db in response.get("results", []):
                databases.append({
                    "id": db["id"],
                    "title": self._extract_title(db),
                    "url": db.get("url"),
                })
            
            return databases
            
        except APIResponseError as e:
            raise Exception(f"Failed to list databases: {e.message}")
    
    async def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query a database.
        
        Args:
            database_id: Database ID
            filter_obj: Optional filter object
            limit: Maximum results
            
        Returns:
            List of database entries
        """
        try:
            query_params = {"database_id": database_id, "page_size": limit}
            
            if filter_obj:
                query_params["filter"] = filter_obj
            
            response = self.client.databases.query(**query_params)
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "id": item["id"],
                    "properties": item.get("properties", {}),
                    "url": item.get("url"),
                })
            
            return results
            
        except APIResponseError as e:
            raise Exception(f"Failed to query database: {e.message}")
    
    def _extract_title(self, obj: Dict[str, Any]) -> str:
        """Extract title from a Notion object"""
        properties = obj.get("properties", {})
        
        # Try different title property names
        for key in ["title", "Title", "Name", "name"]:
            if key in properties:
                title_prop = properties[key]
                if title_prop.get("type") == "title" and title_prop.get("title"):
                    return title_prop["title"][0].get("plain_text", "")
        
        return "Untitled"
    
    def _extract_block_text(self, block: Dict[str, Any]) -> str:
        """Extract text from a block"""
        block_type = block.get("type")
        
        if not block_type:
            return ""
        
        block_data = block.get(block_type, {})
        
        # Handle different block types
        if "rich_text" in block_data:
            texts = [rt.get("plain_text", "") for rt in block_data["rich_text"]]
            return "".join(texts)
        
        return ""
