"""Embedding generation using OpenRouter embeddings via LangChain."""

import logging
from typing import List
from app.llm_core.openrouter_model import get_openrouter_embedding_model

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings using OpenRouter via LangChain."""
    
    def __init__(self):
        # OpenRouter OpenAI-compatible embeddings model handles both documents and queries.
        self.document_embeddings = get_openrouter_embedding_model()
        self.query_embeddings = self.document_embeddings
    
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
