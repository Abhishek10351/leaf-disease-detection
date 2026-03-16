"""
RAG Core Module

Provides Retrieval Augmented Generation (RAG) capabilities with:
- Chroma vector database for semantic search
- OpenRouter embeddings for document encoding
- LangGraph workflow orchestration
- Knowledge base management
- RAG-enhanced disease analysis
"""

from app.rag_core.chroma_client import (
    ChromaManager,
    get_chroma_manager,
)

from app.rag_core.embeddings import (
    EmbeddingGenerator,
    get_embedding_generator,
)

from app.rag_core.retrieval import (
    RAGRetriever,
    RetrievalResult,
    get_rag_retriever,
)

from app.rag_core.langgraph_workflow import (
    RAGWorkflow,
    AnalysisState,
    get_rag_workflow,
)

from app.rag_core.rag_service import (
    RAGService,
    get_rag_service,
)

from app.rag_core.data_seeds import KNOWLEDGE_BASE_SEED

__all__ = [
    "ChromaManager",
    "get_chroma_manager",
    "EmbeddingGenerator",
    "get_embedding_generator",
    "RAGRetriever",
    "RetrievalResult",
    "get_rag_retriever",
    "RAGWorkflow",
    "AnalysisState",
    "get_rag_workflow",
    "RAGService",
    "get_rag_service",
    "KNOWLEDGE_BASE_SEED",
]
