"""
RAG retrieval logic for semantic search in Chroma.
Handles document retrieval and ranking.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.rag_core.chroma_client import get_chroma_manager
from app.rag_core.embeddings import get_embedding_generator


@dataclass
class RetrievalResult:
    """Retrieved document w
    ith metadata."""
    id: str
    content: str
    metadata: Dict[str, Any]
    distance: float
    similarity_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "distance": self.distance,
            "similarity_score": self.similarity_score
        }


class RAGRetriever:
    """Retrieves relevant documents from Chroma for RAG."""
    
    def __init__(self):
        self.chroma = get_chroma_manager()
        self.embeddings = get_embedding_generator()
    
    def retrieve(
        self,
        query: str,
        collection_name: str = "knowledge_base",
        top_k: int = 5,
        min_similarity: float = 0.3
    ) -> List[RetrievalResult]:
        """
        Retrieve most relevant documents for a query.
        
        Args:
            query: Search query
            collection_name: Chroma collection to search
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of relevant documents
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.generate_query_embedding(query)
            
            # Query Chroma
            results = self.chroma.query(
                collection_name=collection_name,
                query_texts=[query],
                n_results=top_k * 2  # Get more to filter by threshold
            )
            
            # Parse results
            retrieved = []
            
            if results and results.get("documents"):
                documents = results["documents"][0]
                distances = results.get("distances", [[]])[0]
                metadatas = results.get("metadatas", [[]])[0]
                ids = results.get("ids", [[]])[0]
                
                for doc, distance, metadata, doc_id in zip(
                    documents, distances, metadatas, ids
                ):
                    # Convert distance to similarity (0-1 range)
                    # Chroma uses Euclidean distance, smaller is better
                    similarity = 1 / (1 + distance) if distance >= 0 else 0
                    
                    if similarity >= min_similarity:
                        retrieved.append(
                            RetrievalResult(
                                id=doc_id,
                                content=doc,
                                metadata=metadata,
                                distance=distance,
                                similarity_score=similarity
                            )
                        )
            
            print(f"Retrieved {len(retrieved)} documents for query")
            return retrieved[:top_k]
            
        except Exception as e:
            print(f"Retrieval failed: {str(e)}")
            return []
    
    def retrieve_by_filter(
        self,
        query: str,
        collection_name: str = "knowledge_base",
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[RetrievalResult]:
        """
        Retrieve documents with filtering.
        
        Args:
            query: Search query
            collection_name: Chroma collection
            filters: Filter conditions (e.g., {"disease": "powdery_mildew"})
            top_k: Number of results
            
        Returns:
            Filtered retrieval results
        """
        try:
            # Query with filters
            results = self.chroma.query(
                collection_name=collection_name,
                query_texts=[query],
                n_results=top_k,
                where=filters
            )
            
            # Parse results
            retrieved = []
            
            if results and results.get("documents"):
                documents = results["documents"][0]
                distances = results.get("distances", [[]])[0]
                metadatas = results.get("metadatas", [[]])[0]
                ids = results.get("ids", [[]])[0]
                
                for doc, distance, metadata, doc_id in zip(
                    documents, distances, metadatas, ids
                ):
                    similarity = 1 / (1 + distance) if distance >= 0 else 0
                    retrieved.append(
                        RetrievalResult(
                            id=doc_id,
                            content=doc,
                            metadata=metadata,
                            distance=distance,
                            similarity_score=similarity
                        )
                    )
            
            return retrieved
            
        except Exception as e:
            print(f"Filtered retrieval failed: {str(e)}")
            return []
    
    def retrieve_by_metadata(
        self,
        metadata_filters: Dict[str, Any],
        collection_name: str = "knowledge_base",
        top_k: int = 10
    ) -> List[RetrievalResult]:
        """
        Retrieve documents by metadata only (no semantic search).
        
        Args:
            metadata_filters: Metadata filter conditions
            collection_name: Chroma collection
            top_k: Number of results
            
        Returns:
            Filtered documents
        """
        try:
            results = self.chroma.query(
                collection_name=collection_name,
                query_texts=[""],  # Empty query for metadata-only search
                n_results=top_k,
                where=metadata_filters
            )
            
            # Parse results
            retrieved = []
            
            if results and results.get("documents"):
                documents = results["documents"][0]
                metadatas = results.get("metadatas", [[]])[0]
                ids = results.get("ids", [[]])[0]
                
                for doc, metadata, doc_id in zip(documents, metadatas, ids):
                    retrieved.append(
                        RetrievalResult(
                            id=doc_id,
                            content=doc,
                            metadata=metadata,
                            distance=0.0,
                            similarity_score=1.0
                        )
                    )
            
            return retrieved
            
        except Exception as e:
            print(f"Metadata retrieval failed: {str(e)}")
            return []
    
    def format_context(self, results: List[RetrievalResult]) -> str:
        """
        Format retrieval results as context for prompts.
        
        Args:
            results: Retrieved documents
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Reference {i}] ({result.similarity_score:.0%} relevant)\n"
                f"{result.content}\n"
                f"Tags: {', '.join(str(v) for v in result.metadata.values())}\n"
            )
        
        return "\n".join(context_parts)


def get_rag_retriever() -> RAGRetriever:
    """Get RAG retriever instance."""
    return RAGRetriever()
