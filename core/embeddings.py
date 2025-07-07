# core/embeddings.py
# Pinecone integrated embeddings - no local models needed

from typing import List

class PineconeIntegratedEmbeddings:
    """
    Embeddings class for Pinecone's integrated embedding models.
    When using Pinecone's integrated embeddings, we don't need to generate 
    embeddings locally - Pinecone handles this automatically on upsert and query.
    """
    
    def __init__(self):
        # These values match Pinecone's integrated model
        self.model_name = "multilingual-e5-large"  # Pinecone's integrated model
        self.dimensions = 1024  # Dimension for multilingual-e5-large
        
    def embed_query(self, text: str) -> List[float]:
        """
        This method should not be called when using Pinecone integrated embeddings.
        Pinecone handles embedding generation automatically during queries.
        """
        raise NotImplementedError(
            "When using Pinecone integrated embeddings, embedding generation "
            "is handled automatically by Pinecone during queries. "
            "This method should not be called."
        )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        This method should not be called when using Pinecone integrated embeddings.
        Pinecone handles embedding generation automatically during upserts.
        """
        raise NotImplementedError(
            "When using Pinecone integrated embeddings, embedding generation "
            "is handled automatically by Pinecone during upserts. "
            "This method should not be called."
        )

def get_embedding_model():
    """
    Returns the Pinecone integrated embedding model configuration.
    No local model loading or API calls needed.
    """
    return PineconeIntegratedEmbeddings() 