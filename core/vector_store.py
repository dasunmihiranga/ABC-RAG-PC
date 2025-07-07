# core/vector_store.py
# Manages Pinecone initialization with integrated embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

def get_pinecone_client():
    """
    Initialize and return Pinecone client
    """
    load_dotenv(override=True)
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in environment variables. Please check your .env file.")
    
    try:
        return Pinecone(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Failed to initialize Pinecone client. Please check your API key. Error: {str(e)}")

def get_vector_store():
    """
    Initializes and returns the Pinecone vector store with integrated embeddings.
    Uses Pinecone's built-in embedding model - no local models needed.
    """
    pc = get_pinecone_client()
    
    index_name = os.getenv("PINECONE_INDEX_NAME", "abc-assistant-integrated")
    print(f"Using Pinecone index with integrated embeddings: {index_name}")
    
    # Check if index exists, if not create it with integrated embeddings
    try:
        if not pc.has_index(index_name):
            print(f"Index {index_name} does not exist. Creating new index with integrated embeddings...")
            # Create index with integrated embeddings model
            pc.create_index_for_model(
                name=index_name,
                cloud=os.getenv("PINECONE_CLOUD", "aws"),
                region=os.getenv("PINECONE_REGION", "us-east-1"),
                embed={
                    "model": "multilingual-e5-large",
                    "field_map": {"text": "chunk_text"}
                }
            )
            print(f"Created new Pinecone index with integrated embeddings: {index_name}")
        else:
            print(f"Using existing index: {index_name}")
    except Exception as e:
        raise ValueError(f"Failed to check or create Pinecone index. Error: {str(e)}")
    
    # Return the index directly for integrated embeddings
    return pc.Index(index_name)

def get_retriever(index, k=4):
    """
    Returns a simple retriever function that works with Pinecone's integrated embeddings.
    Using a simple function approach to avoid Pydantic validation issues.
    """
    from langchain_core.runnables import RunnableLambda
    
    def retrieve_documents(query: str):
        """
        Query the index using integrated embeddings.
        """
        try:
            from pinecone import Pinecone
            import os
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            
            # Generate query embedding using Pinecone's inference API
            model_name = "multilingual-e5-large"
            embedding_response = pc.inference.embed(
                model=model_name,
                inputs=[query],
                parameters={"input_type": "query"}
            )
            
            # Get the query vector
            query_vector = embedding_response.data[0].values
            
            # Query the index with the embedded vector
            results = index.query(
                vector=query_vector,
                top_k=k,
                include_metadata=True
            )
            
            # Convert to LangChain Document format
            from langchain_core.documents import Document
            docs = []
            for match in results.matches:
                metadata = match.metadata or {}
                content = metadata.get('text', metadata.get('chunk_text', ''))
                docs.append(Document(
                    page_content=content,
                    metadata=metadata
                ))
            return docs
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    return RunnableLambda(retrieve_documents)

def split_documents(documents):
    """
    Splits documents into smaller chunks for ingestion into the vector store.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)

def add_documents_to_index(index, documents):
    """
    Add documents to Pinecone index using integrated embeddings.
    For integrated embeddings, we need to use the inference namespace.
    """
    import uuid
    
    # Get the Pinecone client to use inference API
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Prepare data for embedding and upsert
    texts_to_embed = []
    metadata_list = []
    ids = []
    
    for i, doc in enumerate(documents):
        doc_id = str(uuid.uuid4())
        ids.append(doc_id)
        texts_to_embed.append(doc.page_content)
        metadata_list.append({
            "text": doc.page_content,
            **doc.metadata
        })
    
    try:
        # Use the inference API to embed and upsert
        # For integrated embeddings, we use the inference.embed method
        model_name = "multilingual-e5-large"  # Pinecone's integrated model
        
        # Generate embeddings using Pinecone's inference API
        embeddings_response = pc.inference.embed(
            model=model_name,
            inputs=texts_to_embed,
            parameters={"input_type": "passage"}
        )
        
        # Prepare vectors for upsert
        vectors_to_upsert = []
        for i, embedding in enumerate(embeddings_response.data):
            vectors_to_upsert.append({
                "id": ids[i],
                "values": embedding.values,
                "metadata": metadata_list[i]
            })
        
        # Upsert the vectors
        index.upsert(vectors=vectors_to_upsert)
        print(f"Successfully upserted {len(vectors_to_upsert)} documents with integrated embeddings")
        
    except Exception as e:
        print(f"Error upserting documents: {e}")
        raise 