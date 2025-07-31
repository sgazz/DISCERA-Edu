"""
Vector Store Service using ChromaDB for DISCERA RAG System
"""
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import numpy as np
import uuid

from app.core.config import settings
from app.rag.document_processor import DocumentChunk

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB vector store service"""
    
    def __init__(self, collection_name: str = "discera_documents"):
        """Initialize ChromaDB vector store"""
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "DISCERA Document Embeddings"}
            )
            
            logger.info(f"✅ ChromaDB initialized: {collection_name}")
            logger.info(f"Collection count: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents(
        self, 
        embeddings: List[Dict[str, Any]], 
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add document embeddings to vector store"""
        try:
            if not embeddings:
                logger.warning("No embeddings to add")
                return False
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            embeddings_list = []
            metadatas = []
            
            for embedding_data in embeddings:
                # Generate unique ID
                chunk_id = f"{document_id}_{embedding_data['chunk_id']}"
                ids.append(chunk_id)
                
                # Add document content
                documents.append(embedding_data['content'])
                
                # Add embedding
                embeddings_list.append(embedding_data['embedding'])
                
                # Add metadata (ensure all values are strings, ints, or floats)
                chunk_metadata = {
                    "document_id": str(document_id),
                    "chunk_id": str(embedding_data['chunk_id']),
                    "embedding_dim": int(embedding_data['embedding_dim'])
                }
                
                # Add optional metadata with proper type conversion
                if embedding_data['metadata']:
                    for key, value in embedding_data['metadata'].items():
                        if value is not None:
                            if isinstance(value, (int, float, str, bool)):
                                chunk_metadata[str(key)] = value
                            else:
                                chunk_metadata[str(key)] = str(value)
                
                if metadata:
                    for key, value in metadata.items():
                        if value is not None:
                            if isinstance(value, (int, float, str, bool)):
                                chunk_metadata[str(key)] = value
                            else:
                                chunk_metadata[str(key)] = str(value)
                
                metadatas.append(chunk_metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings_list,
                metadatas=metadatas
            )
            
            logger.info(f"✅ Added {len(embeddings)} chunks for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding documents to vector store: {e}")
            return False
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        n_results: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            # Convert numpy array to list
            query_embedding_list = query_embedding.tolist()
            
            # Perform search
            results = self.collection.query(
                query_embeddings=[query_embedding_list],
                n_results=n_results,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i],
                        "similarity": 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    formatted_results.append(result)
            
            logger.info(f"✅ Found {len(formatted_results)} similar documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Error searching vector store: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        try:
            # Find all chunks for this document
            results = self.collection.get(
                where={"document_id": document_id},
                include=["metadatas"]
            )
            
            if results['ids']:
                # Delete chunks
                self.collection.delete(ids=results['ids'])
                logger.info(f"✅ Deleted {len(results['ids'])} chunks for document {document_id}")
                return True
            else:
                logger.warning(f"No chunks found for document {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error deleting document from vector store: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            count = self.collection.count()
            
            # Get sample metadata to understand structure
            sample_results = self.collection.get(limit=1, include=["metadatas"])
            
            return {
                "collection_name": self.collection_name,
                "total_chunks": count,
                "sample_metadata_keys": list(sample_results['metadatas'][0].keys()) if sample_results['metadatas'] else []
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting collection stats: {e}")
            return {}
    
    def reset_collection(self) -> bool:
        """Reset the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "DISCERA Document Embeddings"}
            )
            logger.info(f"✅ Reset collection: {self.collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error resetting collection: {e}")
            return False 