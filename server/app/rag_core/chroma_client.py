"""
Chroma vector database setup and management.
Handles initialization, collection management, and basic operations.
"""

import os
import logging
from typing import Optional, List, Dict, Any
import chromadb
from chromadb.config import Settings
from pathlib import Path

logger = logging.getLogger(__name__)


class ChromaManager:
    """Manages Chroma vector database initialization and operations."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # SQLite persistence path
        chroma_dir = Path("data/chroma")
        chroma_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client with SQLite
        self.client = chromadb.HttpClient(
            host="localhost",
            port=8000
        ) if os.getenv("CHROMA_SERVER") else chromadb.PersistentClient(
            path=str(chroma_dir)
        )
        
        self.collections = {}
        self._initialized = True
        logger.info("Chroma client initialized")
    
    def get_or_create_collection(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> chromadb.Collection:
        """
        Get or create a collection.
        
        Args:
            name: Collection name
            metadata: Collection metadata
            
        Returns:
            Chroma collection
        """
        if name in self.collections:
            return self.collections[name]
        
        collection = self.client.get_or_create_collection(
            name=name,
            metadata=metadata or {},
            get_or_create=True
        )
        
        self.collections[name] = collection
        logger.info(f"Collection '{name}' ready")
        
        return collection
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add documents to collection.
        
        Args:
            collection_name: Target collection
            documents: Document texts
            metadatas: Document metadata
            embeddings: Pre-computed embeddings (optional)
            ids: Document IDs (optional)
        """
        collection = self.get_or_create_collection(collection_name)
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids,
            upsert=True
        )
        
        logger.info(f"Added {len(documents)} documents to '{collection_name}'")
    
    def query(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query collection.
        
        Args:
            collection_name: Target collection
            query_texts: Query texts
            n_results: Number of results
            where: Filter conditions
            
        Returns:
            Query results with distances
        """
        collection = self.get_or_create_collection(collection_name)
        
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        
        return results
    
    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection."""
        self.client.delete_collection(name=collection_name)
        if collection_name in self.collections:
            del self.collections[collection_name]
        logger.info(f"Deleted collection '{collection_name}'")
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection."""
        collection = self.get_or_create_collection(collection_name)
        
        return {
            "name": collection_name,
            "count": collection.count(),
            "metadata": collection.metadata
        }


def get_chroma_manager() -> ChromaManager:
    """Get global Chroma manager instance."""
    return ChromaManager()
