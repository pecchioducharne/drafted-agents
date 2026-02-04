"""
Indexer Service - Knowledge layer for Drafted Agents
Ingests repos, docs, tickets into vector store
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import schedule
import time

load_dotenv()


class DraftedIndexer:
    """Main indexer service"""
    
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=self.qdrant_url)
        self.setup_collections()
    
    def setup_collections(self):
        """Initialize Qdrant collections"""
        collections = [
            ("repos", 1536),      # Code and repository content
            ("docs", 1536),       # Documentation
            ("tickets", 1536),    # Linear/Jira tickets
            ("conversations", 1536)  # Slack/chat history
        ]
        
        for collection_name, vector_size in collections:
            try:
                self.client.get_collection(collection_name)
                print(f"Collection '{collection_name}' already exists")
            except Exception:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created collection '{collection_name}'")
    
    def index_repos(self):
        """Index GitHub repositories"""
        print("Indexing repositories...")
        # TODO: Implement GitHub repo indexing
        pass
    
    def index_docs(self):
        """Index documentation"""
        print("Indexing documentation...")
        # TODO: Implement doc indexing (Notion, etc.)
        pass
    
    def index_tickets(self):
        """Index Linear/Jira tickets"""
        print("Indexing tickets...")
        # TODO: Implement ticket indexing
        pass
    
    def run_nightly_index(self):
        """Run full indexing job"""
        print("Starting nightly indexing job...")
        self.index_repos()
        self.index_docs()
        self.index_tickets()
        print("Nightly indexing complete")


def main():
    """Main entry point"""
    indexer = DraftedIndexer()
    
    # Schedule nightly indexing at 2 AM
    schedule.every().day.at("02:00").do(indexer.run_nightly_index)
    
    print("Indexer service started")
    print("Scheduled nightly indexing at 02:00")
    
    # Run once on startup
    indexer.run_nightly_index()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
