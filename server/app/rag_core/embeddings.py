"""
Embedding generation using Gemini embeddings via LangChain.
Converts text to vector embeddings for semantic search.
"""

import logging
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings using Google Gemini via LangChain."""
    
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        # Initialize LangChain embeddings with document task type (default)
        self.document_embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key,
            task_type="RETRIEVAL_DOCUMENT"
        )
        
        # Initialize LangChain embeddings with query task type
        self.query_embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key,
            task_type="RETRIEVAL_QUERY"
        )
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text (document).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.document_embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.document_embeddings.embed_documents(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {str(e)}")
            # Fallback to one-by-one generation with error handling
            embeddings = []
            for text in texts:
                try:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)
                except Exception as text_error:
                    logger.error(f"Failed to embed text: {str(text_error)}")
                    embeddings.append([0.0] * 768)  # Fallback embedding
            return embeddings
    
    def generate_query_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a query (optimized for search).
        
        Args:
            text: Query text
            
        Returns:
            Query embedding vector
        """
        try:
            embedding = self.query_embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Query embedding generation failed: {str(e)}")
            raise


# Global instance
_embedding_generator = None


def get_embedding_generator() -> EmbeddingGenerator:
    """Get global embedding generator instance."""
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator
