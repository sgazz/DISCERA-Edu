"""
Advanced Embedding Service for DISCERA RAG System
"""
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

from app.core.config import settings
from app.rag.document_processor import DocumentChunk

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Advanced embedding service using Sentence Transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding service"""
        self.model_name = model_name
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing embedding service with model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            self.model = SentenceTransformer(model_name, device=self.device)
            logger.info("✅ Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
    
    def generate_embeddings(self, chunks: List[DocumentChunk]) -> List[Dict[str, Any]]:
        """Generate embeddings for document chunks"""
        if not chunks:
            return []
        
        try:
            # Extract text content
            texts = [chunk.content for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.model.encode(
                texts,
                convert_to_tensor=True,
                show_progress_bar=True,
                batch_size=32
            )
            
            # Convert to numpy for storage
            embeddings_np = embeddings.cpu().numpy()
            
            # Create results with metadata
            results = []
            for i, chunk in enumerate(chunks):
                result = {
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "embedding": embeddings_np[i].tolist(),
                    "embedding_dim": len(embeddings_np[i]),
                    "metadata": {
                        "page_number": chunk.page_number,
                        "section": chunk.section,
                        "chunk_size": len(chunk.content),
                        **(chunk.metadata if chunk.metadata else {})
                    }
                }
                results.append(result)
            
            logger.info(f"✅ Generated {len(results)} embeddings")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error generating embeddings: {e}")
            raise
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """Generate embedding for a single query"""
        try:
            embedding = self.model.encode(
                [query],
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            return embedding.cpu().numpy()[0]
            
        except Exception as e:
            logger.error(f"❌ Error generating query embedding: {e}")
            raise
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Normalize embeddings
            embedding1_norm = embedding1 / np.linalg.norm(embedding1)
            embedding2_norm = embedding2 / np.linalg.norm(embedding2)
            
            # Calculate cosine similarity
            similarity = np.dot(embedding1_norm, embedding2_norm)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"❌ Error calculating similarity: {e}")
            return 0.0
    
    def batch_similarity_search(
        self, 
        query_embedding: np.ndarray, 
        document_embeddings: List[np.ndarray],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Perform batch similarity search"""
        try:
            similarities = []
            
            for i, doc_embedding in enumerate(document_embeddings):
                similarity = self.calculate_similarity(query_embedding, doc_embedding)
                similarities.append({
                    "index": i,
                    "similarity": similarity
                })
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Return top_k results
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"❌ Error in batch similarity search: {e}")
            return []
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embedding model"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_seq_length": self.model.max_seq_length if hasattr(self.model, 'max_seq_length') else None,
            "embedding_dimension": self.model.get_sentence_embedding_dimension(),
            "model_info": str(self.model)
        } 