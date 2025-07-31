"""
Main RAG Service for DISCERA - Orchestrates all RAG components
"""
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import uuid

from app.rag.document_processor import DocumentProcessor, DocumentChunk
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGService:
    """Main RAG service orchestrating all components"""
    
    def __init__(self):
        """Initialize RAG service with all components"""
        self.document_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        
        logger.info("✅ RAG Service initialized with all components")
    
    def process_and_store_document(
        self, 
        file_path: str, 
        file_type: str,
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process document and store in vector database"""
        try:
            logger.info(f"🔄 Processing document: {file_path}")
            
            # Step 1: Process document into chunks
            chunks = self.document_processor.process_document(file_path, file_type)
            logger.info(f"📄 Created {len(chunks)} chunks")
            
            # Step 2: Generate embeddings
            embeddings = self.embedding_service.generate_embeddings(chunks)
            logger.info(f"🧠 Generated {len(embeddings)} embeddings")
            
            # Step 3: Store in vector database
            success = self.vector_store.add_documents(
                embeddings=embeddings,
                document_id=document_id,
                metadata=metadata
            )
            
            if success:
                # Generate summary
                summary = self.document_processor.get_document_summary(chunks)
                summary.update({
                    "document_id": document_id,
                    "file_path": file_path,
                    "file_type": file_type,
                    "embeddings_generated": len(embeddings),
                    "vector_store_success": success
                })
                
                logger.info(f"✅ Document processed and stored successfully")
                return summary
            else:
                raise Exception("Failed to store documents in vector database")
                
        except Exception as e:
            logger.error(f"❌ Error processing document: {e}")
            raise
    
    def search_documents(
        self, 
        query: str, 
        n_results: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search documents using semantic similarity"""
        try:
            logger.info(f"🔍 Searching for: {query}")
            
            # Generate query embedding
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            # Search vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            logger.info(f"✅ Found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching documents: {e}")
            return []
    
    def get_context_for_query(
        self, 
        query: str, 
        n_results: int = 5
    ) -> str:
        """Get context string for a query (for AI generation)"""
        try:
            results = self.search_documents(query, n_results=n_results)
            
            if not results:
                return ""
            
            # Build context string
            context_parts = []
            for i, result in enumerate(results):
                content = result['content']
                similarity = result['similarity']
                metadata = result['metadata']
                
                # Add metadata info
                doc_info = f"[Document: {metadata.get('document_id', 'Unknown')}"
                if metadata.get('page_number'):
                    doc_info += f", Page: {metadata['page_number']}"
                doc_info += f", Similarity: {similarity:.3f}]"
                
                context_parts.append(f"{doc_info}\n{content}\n")
            
            context = "\n".join(context_parts)
            logger.info(f"📝 Generated context with {len(results)} chunks")
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Error generating context: {e}")
            return ""
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document from vector store"""
        try:
            success = self.vector_store.delete_document(document_id)
            if success:
                logger.info(f"✅ Deleted document: {document_id}")
            else:
                logger.warning(f"⚠️ No chunks found for document: {document_id}")
            return success
            
        except Exception as e:
            logger.error(f"❌ Error deleting document: {e}")
            return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            # Get embedding model info
            model_info = self.embedding_service.get_model_info()
            
            # Get vector store stats
            vector_stats = self.vector_store.get_collection_stats()
            
            # Get document processor info
            processor_info = {
                "supported_extensions": list(self.document_processor.supported_extensions),
                "chunk_size": self.document_processor.chunk_size,
                "chunk_overlap": self.document_processor.chunk_overlap
            }
            
            return {
                "embedding_model": model_info,
                "vector_store": vector_stats,
                "document_processor": processor_info,
                "status": "operational"
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting system stats: {e}")
            return {"status": "error", "error": str(e)}
    
    def reset_system(self) -> bool:
        """Reset the entire RAG system"""
        try:
            success = self.vector_store.reset_collection()
            if success:
                logger.info("✅ RAG system reset successfully")
            return success
            
        except Exception as e:
            logger.error(f"❌ Error resetting RAG system: {e}")
            return False 