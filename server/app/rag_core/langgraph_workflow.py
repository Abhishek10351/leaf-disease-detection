"""
LangGraph workflow orchestration for RAG-enhanced analysis.
Defines multi-step analysis with branching logic.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from langgraph.graph import StateGraph, END
from langgraph.types import Send


@dataclass
class AnalysisState:
    """State for analysis workflow."""
    # Input
    disease_description: str
    plant_type: Optional[str] = None
    severity_level: Optional[str] = None
    
    # Processing
    analysis_type: str = "image"  # image, symptoms, care
    retrieved_documents: List[Dict[str, Any]] = field(default_factory=list)
    rag_context: str = ""
    
    # Output
    initial_analysis: Optional[Dict[str, Any]] = None
    final_response: Optional[Dict[str, Any]] = None
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "disease_description": self.disease_description,
            "plant_type": self.plant_type,
            "severity_level": self.severity_level,
            "analysis_type": self.analysis_type,
            "retrieved_documents": len(self.retrieved_documents),
            "rag_context_length": len(self.rag_context),
            "confidence": self.confidence,
            "has_final_response": self.final_response is not None
        }


class RAGWorkflow:
    """Orchestrates RAG-enhanced disease analysis."""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the analysis workflow graph."""
        workflow = StateGraph(AnalysisState)
        
        # Add nodes
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("validate_retrieval", self._validate_retrieval)
        workflow.add_node("generate_analysis", self._generate_analysis)
        workflow.add_node("enhance_response", self._enhance_response)
        workflow.add_node("finalize", self._finalize)
        
        # Add edges
        workflow.set_entry_point("retrieve_context")
        
        workflow.add_edge("retrieve_context", "validate_retrieval")
        
        # Branching: if good retrieval, enhance; else generate without context
        workflow.add_conditional_edges(
            "validate_retrieval",
            self._should_use_context,
            {
                True: "generate_analysis",
                False: "generate_analysis"  # Both paths lead to generation
            }
        )
        
        workflow.add_edge("generate_analysis", "enhance_response")
        workflow.add_edge("enhance_response", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    async def _retrieve_context(self, state: AnalysisState) -> AnalysisState:
        """
        Step 1: Retrieve relevant documents from knowledge base.
        """
        from app.rag_core.retrieval import get_rag_retriever
        
        print("Step 1: Retrieving context...")
        retriever = get_rag_retriever()
        
        # Build query from state
        query_parts = [state.disease_description]
        if state.plant_type:
            query_parts.append(f"plant: {state.plant_type}")
        if state.severity_level:
            query_parts.append(f"severity: {state.severity_level}")
        
        query = " ".join(query_parts)
        
        # Retrieve documents
        results = retriever.retrieve(
            query=query,
            collection_name="knowledge_base",
            top_k=5,
            min_similarity=0.3
        )
        
        state.retrieved_documents = [r.to_dict() for r in results]
        state.rag_context = retriever.format_context(results)
        
        print(f"Retrieved {len(results)} documents")
        
        return state
    
    async def _validate_retrieval(self, state: AnalysisState) -> AnalysisState:
        """
        Step 2: Validate retrieval quality.
        """
        print("Step 2: Validating retrieval...")
        
        if not state.retrieved_documents:
            print("Warning: No documents retrieved")
            return state
        
        # Calculate average similarity
        avg_similarity = sum(
            doc.get("similarity_score", 0)
            for doc in state.retrieved_documents
        ) / len(state.retrieved_documents)
        
        state.confidence = avg_similarity
        print(f"Retrieval confidence: {avg_similarity:.2%}")
        
        return state
    
    async def _should_use_context(self, state: AnalysisState) -> bool:
        """
        Decide whether to use retrieved context (confidence > 0.5).
        """
        return state.confidence >= 0.5
    
    async def _generate_analysis(self, state: AnalysisState) -> AnalysisState:
        """
        Step 3: Generate initial analysis (using Gemini with optional context).
        """
        print("Step 3: Generating analysis...")
        
        from app.llm_core import analyze_leaf_image, analyze_leaf_symptoms
        
        # Build enhanced prompt with context if available
        context_prompt = ""
        if state.rag_context:
            context_prompt = f"\n\nRelevant information from knowledge base:\n{state.rag_context}"
        
        try:
            # Call appropriate analysis function
            if state.analysis_type == "symptoms":
                # For symptoms, enhance the analysis request
                enhanced_description = f"{state.disease_description}{context_prompt}"
                analysis = await analyze_leaf_symptoms(
                    symptoms_description=enhanced_description,
                    plant_type=state.plant_type
                )
            else:
                # For images, context would be included in post-processing
                analysis = None  # Image analysis would happen before workflow
            
            state.initial_analysis = analysis.model_dump() if analysis else None
            print("Analysis generated")
            
        except Exception as e:
            print(f"Analysis generation failed: {str(e)}")
            state.initial_analysis = None
        
        return state
    
    async def _enhance_response(self, state: AnalysisState) -> AnalysisState:
        """
        Step 4: Enhance response with RAG context for better recommendations.
        """
        print("Step 4: Enhancing response...")
        
        if not state.initial_analysis:
            return state
        
        # Add RAG context to response
        enhanced_response = state.initial_analysis.copy()
        
        if state.retrieved_documents:
            enhanced_response["rag_enhanced"] = True
            enhanced_response["referenced_cases"] = len(state.retrieved_documents)
            enhanced_response["context_used"] = state.rag_context[:500]  # Summary
        else:
            enhanced_response["rag_enhanced"] = False
        
        state.final_response = enhanced_response
        print("Response enhanced with RAG context")
        
        return state
    
    async def _finalize(self, state: AnalysisState) -> AnalysisState:
        """
        Step 5: Finalize and prepare output.
        """
        print("Step 5: Finalizing...")
        
        if not state.final_response:
            state.final_response = state.initial_analysis or {}
        
        # Add metadata
        state.final_response["workflow_info"] = {
            "rag_retrieval_count": len(state.retrieved_documents),
            "rag_confidence": state.confidence,
            "workflow_completed": True
        }
        
        print("Workflow finalized")
        return state
    
    async def execute(self, state: AnalysisState) -> AnalysisState:
        """
        Execute the full workflow.
        
        Args:
            state: Initial analysis state
            
        Returns:
            Final state with results
        """
        print(f"Starting RAG workflow: {state.analysis_type}")
        
        # Execute graph
        result = await self.graph.ainvoke(state)
        
        print("RAG workflow completed")
        return result


def get_rag_workflow() -> RAGWorkflow:
    """Get RAG workflow instance."""
    return RAGWorkflow()
