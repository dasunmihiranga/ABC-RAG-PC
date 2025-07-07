# scripts/cleanup_pinecone_index.py
# Script to clean up incorrect Pinecone indexes

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from pinecone import Pinecone

def cleanup_indexes():
    """
    List and optionally delete Pinecone indexes
    """
    load_dotenv(override=True)
    
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("Error: PINECONE_API_KEY not found")
        return
    
    pc = Pinecone(api_key=api_key)
    
    # List all indexes
    indexes = pc.list_indexes()
    print(f"Found {len(indexes.names())} indexes:")
    
    for i, index_name in enumerate(indexes.names()):
        try:
            index_info = pc.describe_index(index_name)
            print(f"{i+1}. {index_name}")
            print(f"   - Dimension: {index_info.dimension}")
            print(f"   - Metric: {index_info.metric}")
            print(f"   - Status: {index_info.status.state}")
            print(f"   - Host: {index_info.host}")
        except Exception as e:
            print(f"{i+1}. {index_name} - Error getting info: {e}")
        print()
    
    # Ask user if they want to delete the problematic index
    if len(indexes.names()) > 0:
        delete_choice = input("Do you want to delete any indexes? (y/n): ").lower()
        if delete_choice == 'y':
            index_to_delete = input("Enter the name of the index to delete: ").strip()
            if index_to_delete in indexes.names():
                confirm = input(f"Are you sure you want to delete '{index_to_delete}'? This cannot be undone! (yes/no): ")
                if confirm.lower() == 'yes':
                    try:
                        pc.delete_index(index_to_delete)
                        print(f"✓ Index '{index_to_delete}' deleted successfully!")
                    except Exception as e:
                        print(f"✗ Error deleting index: {e}")
                else:
                    print("Delete cancelled.")
            else:
                print("Index name not found.")

if __name__ == "__main__":
    cleanup_indexes()
