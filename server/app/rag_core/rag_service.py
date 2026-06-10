"""
High-level RAG service API.
Provides convenient functions for RAG-enhanced analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from app.rag_core.chroma_client import get_chroma_manager
from app.rag_core.embeddings import get_embedding_generator
from app.rag_core.retrieval import get_rag_retriever, RetrievalResult
from app.rag_core.langgraph_workflow import AnalysisState, get_rag_workflow


logger = logging.getLogger(__name__)


class RAGService:
    """High-level RAG service for knowledge base operations."""
    
    def __init__(self):
        self.chroma = get_chroma_manager()
        self.embeddings = get_embedding_generator()
        self.retriever = get_rag_retriever()
        self.workflow = get_rag_workflow()
    
    # ==================== Knowledge Base Management ====================
    
    def seed_knowledge_base(self, data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """
        Seed knowledge base with disease, treatment, and care data.
        
        Args:
            data: Dictionary with 'diseases', 'treatments', 'care_guides' keys
        """
        print("Seeding knowledge base...")
        
        self.chroma.get_or_create_collection("knowledge_base")
        
        all_docs = []
        all_ids = []
        all_metadata = []
        all_embeddings = []
        
        # Process diseases
        diseases = data.get("diseases", [])
        for disease in diseases:
            doc_id = f"disease_{disease.get('id', 'unknown')}"
            content = disease.get("description", "")
            
            all_docs.append(content)
            all_ids.append(doc_id)
            all_metadata.append({
                "type": "disease",
                "name": disease.get("name", ""),
                "plant": disease.get("plant", ""),
                "severity": disease.get("severity", ""),
                "symptoms": disease.get("symptoms", "")
            })
            
            embedding = self.embeddings.generate_embedding(content)
            all_embeddings.append(embedding)
        
        # Process treatments
        treatments = data.get("treatments", [])
        for treatment in treatments:
            doc_id = f"treatment_{treatment.get('id', 'unknown')}"
            content = treatment.get("description", "")
            
            all_docs.append(content)
            all_ids.append(doc_id)
            all_metadata.append({
                "type": "treatment",
                "disease": treatment.get("disease", ""),
                "method": treatment.get("method", ""),
                "effectiveness": treatment.get("effectiveness", ""),
                "organic": treatment.get("organic", False)
            })
            
            embedding = self.embeddings.generate_embedding(content)
            all_embeddings.append(embedding)
        
        # Process care guides
        care_guides = data.get("care_guides", [])
        for guide in care_guides:
            doc_id = f"care_{guide.get('id', 'unknown')}"
            content = guide.get("description", "")
            
            all_docs.append(content)
            all_ids.append(doc_id)
            all_metadata.append({
                "type": "care",
                "plant": guide.get("plant", ""),
                "difficulty": guide.get("difficulty", ""),
                "season": guide.get("season", "")
            })
            
            embedding = self.embeddings.generate_embedding(content)
            all_embeddings.append(embedding)
        
        # Add all to Chroma
        if all_docs:
            self.chroma.add_documents(
                collection_name="knowledge_base",
                documents=all_docs,
                metadatas=all_metadata,
                embeddings=all_embeddings,
                ids=all_ids
            )
            
            logger.info(f"Seeded {len(all_docs)} documents to knowledge base")

        return {
            "diseases": len(diseases),
            "treatments": len(treatments),
            "care_guides": len(care_guides),
        }

    def add_disease(self, disease: Dict[str, Any]) -> None:
        """Add a disease document to the knowledge base."""
        content = str(disease.get("description", "")).strip()
        if not content:
            return

        doc_id = f"disease_{disease.get('id', 'custom')}"
        embedding = self.embeddings.generate_embedding(content)
        self.chroma.add_documents(
            collection_name="knowledge_base",
            documents=[content],
            metadatas=[{
                "type": "disease",
                "name": disease.get("name", ""),
                "plant": disease.get("plant", ""),
                "severity": disease.get("severity", ""),
                "symptoms": disease.get("symptoms", ""),
            }],
            embeddings=[embedding],
            ids=[doc_id],
        )

    def add_treatment(self, treatment: Dict[str, Any]) -> None:
        """Add a treatment document to the knowledge base."""
        content = str(treatment.get("description", "")).strip()
        if not content:
            return

        doc_id = f"treatment_{treatment.get('id', 'custom')}"
        embedding = self.embeddings.generate_embedding(content)
        self.chroma.add_documents(
            collection_name="knowledge_base",
            documents=[content],
            metadatas=[{
                "type": "treatment",
                "disease": treatment.get("disease", ""),
                "method": treatment.get("method", ""),
                "effectiveness": treatment.get("effectiveness", ""),
                "organic": treatment.get("organic", False),
            }],
            embeddings=[embedding],
            ids=[doc_id],
        )

    def add_care_guide(self, care: Dict[str, Any]) -> None:
        """Add a care guide document to the knowledge base."""
        content = str(care.get("description", "")).strip()
        if not content:
            return

        doc_id = f"care_{care.get('id', 'custom')}"
        embedding = self.embeddings.generate_embedding(content)
        self.chroma.add_documents(
            collection_name="knowledge_base",
            documents=[content],
            metadatas=[{
                "type": "care",
                "plant": care.get("plant", ""),
                "difficulty": care.get("difficulty", ""),
                "season": care.get("season", ""),
            }],
            embeddings=[embedding],
            ids=[doc_id],
        )
    
    def add_analysis_case(
        self,
        disease: str,
        plant: str,
        symptoms: str,
        treatment_used: str,
        effectiveness: str,
        severity: str
    ) -> None:
        """
        Add a new analysis case to knowledge base for future reference.
        
        Args:
            disease: Disease name
            plant: Plant type
            symptoms: Symptom description
            treatment_used: Treatment applied
            effectiveness: Treatment effectiveness
            severity: Disease severity
        """
        content = f"Case: {disease} on {plant}. Symptoms: {symptoms}. Treatment: {treatment_used} (Effectiveness: {effectiveness})"
        
        embedding = self.embeddings.generate_embedding(content)
        
        self.chroma.add_documents(
            collection_name="knowledge_base",
            documents=[content],
            metadatas=[{
                "type": "case",
                "disease": disease,
                "plant": plant,
                "treatment": treatment_used,
                "effectiveness": effectiveness,
                "severity": severity
            }],
            embeddings=[embedding],
            ids=[f"case_{disease}_{plant}_{severity}"]
        )
        
        print(f"Added case: {disease} on {plant}")
        
    
    # ==================== Retrieval ====================
    
    def search_knowledge_base(
        self,
        query: str,
        limit: int = 5,
        min_similarity: float = 0.3,
        filter_plant: Optional[str] = None,
        include_diseases: bool = True,
        include_treatments: bool = True,
        include_care: bool = True,
    ) -> List[RetrievalResult]:
        """
        Search knowledge base.
        
        Args:
            query: Search query
            limit: Number of results
            min_similarity: Similarity threshold
            filter_plant: Optional plant filter
            include_diseases: Include disease documents
            include_treatments: Include treatment documents
            include_care: Include care documents
            
        Returns:
            List of relevant documents
        """
        allowed_types = set()
        if include_diseases:
            allowed_types.add("disease")
        if include_treatments:
            allowed_types.add("treatment")
        if include_care:
            allowed_types.add("care")

        if not allowed_types:
            return []

        raw_results = self.retriever.retrieve(
            query=query,
            collection_name="knowledge_base",
            top_k=max(limit * 3, limit),
            min_similarity=min_similarity,
        )

        filtered: List[RetrievalResult] = []
        normalized_plant = (filter_plant or "").strip().lower()

        for item in raw_results:
            item_type = str(item.metadata.get("type", "")).lower()
            if item_type not in allowed_types:
                continue

            if normalized_plant:
                item_plant = str(item.metadata.get("plant", "")).lower()
                if normalized_plant not in item_plant and item_plant not in normalized_plant:
                    continue

            filtered.append(item)
            if len(filtered) >= limit:
                break

        return filtered
    
    def search_diseases(self, plant: str) -> List[RetrievalResult]:
        """Search for diseases affecting a plant."""
        return self.retriever.retrieve_by_metadata(
            metadata_filters={"type": "disease", "plant": plant},
            collection_name="knowledge_base",
            top_k=10
        )
    
    def search_treatments(self, disease: str) -> List[RetrievalResult]:
        """Search for treatments for a disease."""
        return self.retriever.retrieve_by_metadata(
            metadata_filters={"type": "treatment", "disease": disease},
            collection_name="knowledge_base",
            top_k=10
        )
    
    def search_care_guides(self, plant: str) -> List[RetrievalResult]:
        """Search for care guides for a plant."""
        return self.retriever.retrieve_by_metadata(
            metadata_filters={"type": "care", "plant": plant},
            collection_name="knowledge_base",
            top_k=10
        )
    
    # ==================== Workflow Execution ====================
    
    async def analyze_with_rag(
        self,
        disease_description: str,
        plant_type: Optional[str] = None,
        severity_level: Optional[str] = None,
        analysis_type: str = "symptoms",
        use_context: bool = True,
    ) -> Dict[str, Any]:
        """
        Perform disease analysis enhanced with RAG.
        
        Args:
            disease_description: Disease or symptoms description
            plant_type: Type of plant
            severity_level: Estimated severity
            analysis_type: Type of analysis (symptoms, care, etc)
            
        Returns:
            Enhanced analysis result
        """
        print(f"Starting RAG-enhanced analysis: {analysis_type}")
        
        if not use_context:
            from app.llm_core import get_leaf_analysis

            leaf_analysis = get_leaf_analysis()
            direct = leaf_analysis.analyze_leaf_symptoms(
                symptoms_description=disease_description,
                plant_type=plant_type or "",
            )
            payload = direct.model_dump()
            payload["rag_enhanced"] = False
            payload["referenced_cases"] = 0
            payload["retrieved_documents"] = []
            payload["confidence"] = None
            return payload

        # Create state
        state = AnalysisState(
            disease_description=disease_description,
            plant_type=plant_type,
            severity_level=severity_level,
            analysis_type=analysis_type
        )
        
        # Execute workflow
        result = await self.workflow.execute(state)
        
        return result.final_response or {}
    
    # ==================== Knowledge Base Management ====================
    
    def get_kb_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        stats = self.chroma.get_collection_stats("knowledge_base")
        docs = self.chroma.get_collection_documents("knowledge_base")
        metadatas = docs.get("metadatas") or []

        disease_count = 0
        treatment_count = 0
        care_count = 0
        case_count = 0

        for meta in metadatas:
            doc_type = str((meta or {}).get("type", "")).lower()
            if doc_type == "disease":
                disease_count += 1
            elif doc_type == "treatment":
                treatment_count += 1
            elif doc_type == "care":
                care_count += 1
            elif doc_type == "case":
                case_count += 1

        return {
            "disease_count": disease_count,
            "treatment_count": treatment_count,
            "care_guide_count": care_count,
            "case_history_count": case_count,
            "total_vectors": stats.get("count", 0),
            "collections": [stats.get("name", "knowledge_base")],
        }
    
    def clear_knowledge_base(self) -> None:
        """Clear all documents from knowledge base."""
        self.chroma.delete_collection("knowledge_base")
        print("Knowledge base cleared")


# Global instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get global RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
