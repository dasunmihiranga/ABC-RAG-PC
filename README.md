# Agentic RAG Chatbot with Pinecone

This project implements an Agentic RAG (Retrieval Augmented Generation) Chatbot using Pinecone as the vector database. The bot serves as a professional company assistant, capable of engaging with clients, understanding their needs, and effectively guiding them towards purchasing services and products.

**Note:** This project has been migrated from ChromaDB to Pinecone for improved scalability and performance.

## ![Untitled Diagram drawio](https://github.com/user-attachments/assets/6bf29358-d947-4904-acda-d2d072ffa83f)

## Project Structure

```
├── venv/
├── .env
├── main.py
├── requirements.txt
├── README.md
├── core/
│   ├── __init__.py
│   ├── agent.py
│   ├── embeddings.py
│   ├── vector_store.py        # Updated for Pinecone
│   ├── llm_setup.py
│   └── prompt_templates.py
├── knowledge_base/
│   ├── __init__.py
│   └── docs/
│       ├── abc_company_info.md
└── scripts/
    ├── __init__.py
    ├── ingest_data.py           # Updated for Pinecone
    └── migrate_to_pinecone.py   # New migration script
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd assistant_agent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    Create a `.env` file in the project directory and add your API keys:
    ```
    # Pinecone Configuration
    PINECONE_API_KEY=your_pinecone_api_key_here
    PINECONE_INDEX_NAME=abc-assistant-index
    PINECONE_CLOUD=aws
    PINECONE_REGION=us-east-1
    
    # Other API Keys
    GROQ_API_KEY=your_groq_api_key_here
    ```
    
    You can use `.env.example` as a template.

## Migration from ChromaDB

If you're migrating from the previous ChromaDB version:

1.  **Run the migration script:**
    ```bash
    python scripts/migrate_to_pinecone.py
    ```

2.  **Set up your Pinecone account:**
    - Sign up at [Pinecone](https://www.pinecone.io/)
    - Create a new project
    - Get your API key from the console
    - Add it to your `.env` file

## Running the Application

1.  **Ingest Knowledge Base Documents:**
    ```bash
    python scripts/ingest_data.py
    ```
    
    This will create a Pinecone index and upload your documents to it.

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## Key Features

- **Pinecone Integration**: Scalable vector database for improved performance
- **Integrated Embeddings**: Uses Pinecone's integrated embedding models
- **Automatic Index Creation**: Automatically creates Pinecone index if it doesn't exist
- **Environment-based Configuration**: Easy configuration through environment variables

## API Endpoints

*   **`/chat` (POST):** Accepts user queries and returns bot responses.
    *   **Request Body:**
        ```json
        {
            "query": "Your user query here",
            "session_id": "user1"
        }
        ```
    *   **Response Body:**
        ```json
        {
            "response": "Bot's reply here"
        }
        ```

![image](https://github.com/user-attachments/assets/82f59fab-fded-435f-8942-269ca8dbe58f)

