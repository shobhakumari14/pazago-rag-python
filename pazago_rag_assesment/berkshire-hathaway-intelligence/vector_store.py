import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import os

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.index = None
        self.documents = []
        self.metadata = []
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for texts"""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def build_index(self, chunks: List[Dict]):
        """Build FAISS index from document chunks"""
        texts = [chunk['text'] for chunk in chunks]
        self.documents = texts
        self.metadata = [chunk['metadata'] for chunk in chunks]
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        
        # Build FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        if self.index is None:
            return []
        
        # Create query embedding
        query_embedding = self.create_embeddings([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    'text': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': float(score),
                    'rank': i + 1
                })
        
        return results
    
    def save_index(self, filepath: str):
        """Save index and metadata to disk"""
        if self.index is not None:
            faiss.write_index(self.index, f"{filepath}.faiss")
            
            with open(f"{filepath}_metadata.pkl", 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'metadata': self.metadata
                }, f)
    
    def load_index(self, filepath: str):
        """Load index and metadata from disk"""
        if os.path.exists(f"{filepath}.faiss"):
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            with open(f"{filepath}_metadata.pkl", 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
            return True
        return False