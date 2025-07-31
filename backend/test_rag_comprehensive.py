#!/usr/bin/env python3
"""
Comprehensive RAG System Test Suite for DISCERA
"""
import os
import tempfile
import logging
import time
from typing import List, Dict, Any

from app.rag.rag_service import RAGService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_documents() -> List[Dict[str, str]]:
    """Create multiple test documents"""
    documents = [
        {
            "id": "doc_001",
            "type": ".txt",
            "content": """
            DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment
            
            DISCERA je napredan digitalni sistem za inteligentnu analizu dokumenata i generisanje testova.
            Sistem koristi AI tehnologije za automatizaciju edukacijskog procesa.
            
            Glavne funkcionalnosti:
            - Document processing i text extraction
            - AI-powered test generation
            - Semantic search i retrieval
            - Progress tracking i analytics
            
            Tehnologije:
            - FastAPI backend
            - Next.js frontend
            - OpenAI GPT-4
            - ChromaDB vector storage
            - Sentence Transformers
            """
        },
        {
            "id": "doc_002", 
            "type": ".txt",
            "content": """
            Machine Learning Fundamentals
            
            Machine learning je grana veštačke inteligencije koja omogućava računarima da uče
            bez eksplicitnog programiranja. Osnovni koncepti uključuju:
            
            Supervised Learning:
            - Classification (klasifikacija)
            - Regression (regresija)
            - Neural Networks (neuronske mreže)
            
            Unsupervised Learning:
            - Clustering (grupisanje)
            - Dimensionality reduction
            - Association rules
            
            Deep Learning:
            - Convolutional Neural Networks (CNN)
            - Recurrent Neural Networks (RNN)
            - Transformer models
            """
        },
        {
            "id": "doc_003",
            "type": ".txt", 
            "content": """
            Python Programming Language
            
            Python je visokonivo programski jezik koji se koristi za:
            - Web development (Django, Flask)
            - Data science (Pandas, NumPy)
            - Machine learning (Scikit-learn, TensorFlow)
            - Automation i scripting
            
            Ključne karakteristike:
            - Simple syntax
            - Large standard library
            - Cross-platform compatibility
            - Extensive third-party packages
            
            Popularni frameworks:
            - FastAPI za API development
            - Django za web aplikacije
            - Pandas za data analysis
            - PyTorch za deep learning
            """
        }
    ]
    return documents


def test_document_processing(rag_service: RAGService) -> bool:
    """Test document processing capabilities"""
    print("\n📄 Testing Document Processing...")
    
    try:
        documents = create_test_documents()
        processed_docs = []
        
        for doc in documents:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix=doc['type'], delete=False) as f:
                f.write(doc['content'])
                temp_file = f.name
            
            # Process document
            result = rag_service.process_and_store_document(
                file_path=temp_file,
                file_type=doc['type'],
                document_id=doc['id'],
                metadata={
                    "category": "test",
                    "source": "test_suite",
                    "user_id": 123
                }
            )
            
            processed_docs.append({
                "id": doc['id'],
                "file": temp_file,
                "result": result
            })
            
            print(f"✅ Processed {doc['id']}: {result['total_chunks']} chunks, {result['embeddings_generated']} embeddings")
        
        return True, processed_docs
        
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return False, []


def test_semantic_search(rag_service: RAGService) -> bool:
    """Test semantic search capabilities"""
    print("\n🔍 Testing Semantic Search...")
    
    test_queries = [
        "What is DISCERA and its main features?",
        "Explain machine learning fundamentals",
        "What are Python frameworks for web development?",
        "How does neural network work?",
        "What is data science?"
    ]
    
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Query {i}: {query}")
            
            # Search documents
            results = rag_service.search_documents(query, n_results=3)
            
            print(f"   Found {len(results)} results:")
            for j, result in enumerate(results[:2], 1):
                similarity = result['similarity']
                content_preview = result['content'][:80] + "..."
                doc_id = result['metadata'].get('document_id', 'Unknown')
                
                print(f"     {j}. [{doc_id}] Similarity: {similarity:.3f}")
                print(f"        Content: {content_preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Semantic search failed: {e}")
        return False


def test_context_generation(rag_service: RAGService) -> bool:
    """Test context generation for AI"""
    print("\n📝 Testing Context Generation...")
    
    test_queries = [
        "Explain DISCERA system architecture",
        "What are the benefits of machine learning?",
        "Compare Python frameworks"
    ]
    
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Query {i}: {query}")
            
            # Generate context
            context = rag_service.get_context_for_query(query, n_results=2)
            
            print(f"   Context length: {len(context)} characters")
            print(f"   Context preview: {context[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Context generation failed: {e}")
        return False


def test_system_stats(rag_service: RAGService) -> bool:
    """Test system statistics"""
    print("\n📊 Testing System Statistics...")
    
    try:
        stats = rag_service.get_system_stats()
        
        print("   System Status:")
        print(f"     Status: {stats['status']}")
        print(f"     Embedding Model: {stats['embedding_model']['model_name']}")
        print(f"     Device: {stats['embedding_model']['device']}")
        print(f"     Embedding Dimension: {stats['embedding_model']['embedding_dimension']}")
        print(f"     Vector Store: {stats['vector_store']['collection_name']}")
        print(f"     Total Chunks: {stats['vector_store']['total_chunks']}")
        print(f"     Supported Extensions: {stats['document_processor']['supported_extensions']}")
        
        return True
        
    except Exception as e:
        print(f"❌ System stats failed: {e}")
        return False


def test_performance(rag_service: RAGService) -> bool:
    """Test system performance"""
    print("\n⚡ Testing Performance...")
    
    try:
        # Test search performance
        query = "What is artificial intelligence?"
        
        start_time = time.time()
        results = rag_service.search_documents(query, n_results=5)
        search_time = time.time() - start_time
        
        start_time = time.time()
        context = rag_service.get_context_for_query(query, n_results=3)
        context_time = time.time() - start_time
        
        print(f"   Search Performance:")
        print(f"     Query: {query}")
        print(f"     Search time: {search_time:.3f}s")
        print(f"     Results found: {len(results)}")
        print(f"     Context generation time: {context_time:.3f}s")
        print(f"     Context length: {len(context)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


def main():
    """Run comprehensive RAG tests"""
    print("🧪 DISCERA RAG System - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Initialize RAG service
        print("🔄 Initializing RAG Service...")
        start_time = time.time()
        rag_service = RAGService()
        init_time = time.time() - start_time
        print(f"✅ RAG Service initialized in {init_time:.2f}s")
        
        # Test results
        test_results = {}
        
        # Test 1: Document Processing
        success, processed_docs = test_document_processing(rag_service)
        test_results['document_processing'] = success
        
        # Test 2: Semantic Search
        success = test_semantic_search(rag_service)
        test_results['semantic_search'] = success
        
        # Test 3: Context Generation
        success = test_context_generation(rag_service)
        test_results['context_generation'] = success
        
        # Test 4: System Stats
        success = test_system_stats(rag_service)
        test_results['system_stats'] = success
        
        # Test 5: Performance
        success = test_performance(rag_service)
        test_results['performance'] = success
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        for doc in processed_docs:
            try:
                os.unlink(doc['file'])
            except:
                pass
        print("✅ Test files cleaned up")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary:")
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        all_passed = all(test_results.values())
        if all_passed:
            print("\n🎉 ALL TESTS PASSED! RAG System is fully functional!")
        else:
            print("\n⚠️ Some tests failed. Please check the errors above.")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 