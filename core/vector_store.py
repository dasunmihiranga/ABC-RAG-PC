# core/vector_store.py
# Manages Pinecone initialization and RAG retrieval 
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from core.embeddings import get_embedding_model
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def get_pinecone_client():
    """
    Initialize and return Pinecone client
    """
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in environment variables. Please check your .env file.")
    
    try:
        return Pinecone(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Failed to initialize Pinecone client. Please check your API key. Error: {str(e)}")

def get_vector_store():
    """
    Initializes and returns the Pinecone vector store.
    If the index does not exist, it will be created.
    """
    # Load environment variables
    load_dotenv(override=True)
    
    pc = get_pinecone_client()
    embeddings = get_embedding_model()
    
    # Get embedding dimension
    try:
        # Test embedding to get dimension
        test_embedding = embeddings.embed_query("test")
        embedding_dimension = len(test_embedding)
        print(f"Embedding dimension: {embedding_dimension}")
    except Exception as e:
        print(f"Warning: Could not determine embedding dimension: {e}")
        embedding_dimension = 384  # Default for sentence-transformers/all-MiniLM-L6-v2
    
    index_name = os.getenv("PINECONE_INDEX_NAME", "abc-assistant-index")
    print(f"Using Pinecone index: {index_name}")
    
    # Check if index exists, if not create it
    try:
        if not pc.has_index(index_name):
            print(f"Index {index_name} does not exist. Creating new index...")
            # Create index with correct dimensions for HuggingFace embeddings
            pc.create_index(
                name=index_name,
                dimension=embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=os.getenv("PINECONE_CLOUD", "aws"),
                    region=os.getenv("PINECONE_REGION", "us-east-1")
                )
            )
            print(f"Created new Pinecone index: {index_name} with dimension {embedding_dimension}")
        else:
            # Check if existing index has correct dimensions
            index_info = pc.describe_index(index_name)
            existing_dimension = index_info.dimension
            print(f"Existing index dimension: {existing_dimension}")
            
            if existing_dimension != embedding_dimension:
                print(f"Dimension mismatch! Index has {existing_dimension}, embeddings have {embedding_dimension}")
                # Create a new index with a different name
                new_index_name = f"{index_name}-{embedding_dimension}d"
                if not pc.has_index(new_index_name):
                    print(f"Creating new index {new_index_name} with correct dimensions...")
                    pc.create_index(
                        name=new_index_name,
                        dimension=embedding_dimension,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud=os.getenv("PINECONE_CLOUD", "aws"),
                            region=os.getenv("PINECONE_REGION", "us-east-1")
                        )
                    )
                    index_name = new_index_name
                    print(f"Created new index: {index_name}")
                else:
                    index_name = new_index_name
                    print(f"Using existing index: {index_name}")
            else:
                print(f"Using existing index: {index_name}")
    except Exception as e:
        raise ValueError(f"Failed to check or create Pinecone index. Error: {str(e)}")
    
    # Create vector store
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    
    return vector_store

def get_retriever(vector_store, k=4):
    """
    Returns a retriever for the given vector store.
    """
    return vector_store.as_retriever(search_kwargs={"k": k})

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