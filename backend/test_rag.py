#!/usr/bin/env python3
"""
Test RAG System for DISCERA
"""
import os
import tempfile
import logging
from app.rag.rag_service import RAGService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_document():
    """Create a test document for testing"""
    test_content = """
    DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment
    
    This is a test document for the DISCERA RAG system. It contains information about:
    
    1. Document Processing: The system can process PDF, DOC, DOCX, and TXT files.
    2. Embedding Generation: Uses Sentence Transformers to create vector embeddings.
    3. Vector Storage: ChromaDB is used for storing and retrieving document embeddings.
    4. Semantic Search: The system can find relevant documents based on semantic similarity.
    
    Key Features:
    - Advanced document processing pipeline
    - Multi-format support (PDF, DOC, DOCX, TXT)
    - Semantic chunking with overlap
    - Vector embedding generation
    - ChromaDB integration
    - Semantic search capabilities
    
    This document will be used to test the RAG system's ability to:
    - Process and chunk documents
    - Generate embeddings
    - Store in vector database
    - Perform semantic search
    - Retrieve relevant context
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        return f.name


def test_rag_system():
    """Test the complete RAG system"""
    print("🧪 Testing DISCERA RAG System")
    print("=" * 50)
    
    try:
        # Initialize RAG service
        print("🔄 Initializing RAG Service...")
        rag_service = RAGService()
        print("✅ RAG Service initialized")
        
        # Get system stats
        print("\n📊 System Statistics:")
        stats = rag_service.get_system_stats()
        print(f"   Embedding Model: {stats['embedding_model']['model_name']}")
        print(f"   Device: {stats['embedding_model']['device']}")
        print(f"   Embedding Dimension: {stats['embedding_model']['embedding_dimension']}")
        print(f"   Vector Store: {stats['vector_store']['collection_name']}")
        print(f"   Total Chunks: {stats['vector_store']['total_chunks']}")
        print(f"   Supported Extensions: {stats['document_processor']['supported_extensions']}")
        
        # Create test document
        print("\n📄 Creating test document...")
        test_file = create_test_document()
        print(f"✅ Test document created: {test_file}")
        
        # Process document
        print("\n🔄 Processing document...")
        document_id = "test_doc_001"
        result = rag_service.process_and_store_document(
            file_path=test_file,
            file_type=".txt",
            document_id=document_id,
            metadata={"test": True, "source": "test_script"}
        )
        
        print(f"✅ Document processed successfully:")
        print(f"   Total chunks: {result['total_chunks']}")
        print(f"   Total content length: {result['total_content_length']}")
        print(f"   Embeddings generated: {result['embeddings_generated']}")
        
        # Test search
        print("\n🔍 Testing semantic search...")
        search_query = "What is DISCERA and what are its key features?"
        search_results = rag_service.search_documents(search_query, n_results=3)
        
        print(f"✅ Search completed, found {len(search_results)} results:")
        for i, result in enumerate(search_results[:2]):  # Show first 2 results
            print(f"   Result {i+1}:")
            print(f"     Similarity: {result['similarity']:.3f}")
            print(f"     Content: {result['content'][:100]}...")
        
        # Test context generation
        print("\n📝 Testing context generation...")
        context = rag_service.get_context_for_query(search_query, n_results=2)
        print(f"✅ Context generated ({len(context)} characters)")
        print(f"   Context preview: {context[:200]}...")
        
        # Clean up
        print("\n🧹 Cleaning up...")
        os.unlink(test_file)
        print("✅ Test document removed")
        
        print("\n🎉 RAG System Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ RAG System Test Failed: {e}")
        logger.error(f"RAG test error: {e}")
        return False


if __name__ == "__main__":
    success = test_rag_system()
    exit(0 if success else 1) 