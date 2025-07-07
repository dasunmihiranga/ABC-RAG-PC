# scripts/migrate_to_pinecone.py
# Script to help migrate from ChromaDB to Pinecone

import os
import sys
import shutil
from pathlib import Path

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def cleanup_chromadb():
    """
    Remove the old ChromaDB directory and files
    """
    chroma_path = Path("./chroma_db")
    if chroma_path.exists():
        print(f"Removing ChromaDB directory: {chroma_path}")
        shutil.rmtree(chroma_path)
        print("ChromaDB directory removed successfully.")
    else:
        print("ChromaDB directory not found.")

def check_env_setup():
    """
    Check if required environment variables are set
    """
    required_vars = ["PINECONE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file before proceeding.")
        return False
    
    print("All required environment variables are set.")
    return True

def main():
    """
    Main migration function
    """
    print("=" * 50)
    print("ChromaDB to Pinecone Migration Tool")
    print("=" * 50)
    
    # Check environment setup
    if not check_env_setup():
        print("\nPlease configure your .env file with Pinecone credentials.")
        print("Use .env.example as a template.")
        return
    
    # Clean up old ChromaDB files
    cleanup_response = input("\nDo you want to remove the old ChromaDB directory? (y/n): ")
    if cleanup_response.lower() in ['y', 'yes']:
        cleanup_chromadb()
    
    print("\nMigration steps completed!")
    print("\nNext steps:")
    print("1. Install the new requirements: pip install -r requirements.txt")
    print("2. Run the data ingestion script: python scripts/ingest_data.py")
    print("3. Test your application: python main.py")

if __name__ == "__main__":
    main()
