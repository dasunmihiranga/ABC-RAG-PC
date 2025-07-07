# Agentic RAG Chatbot with Pinecone

This project implements an Agentic RAG (Retrieval Augmented Generation) Chatbot using Pinecone's integrated embeddings. The bot serves as a professional company assistant, capable of engaging with clients, understanding their needs, and effectively guiding them towards purchasing services and products.

## ![Untitled Diagram drawio](https://github.com/user-attachments/assets/6bf29358-d947-4904-acda-d2d072ffa83f)

## Features

- **Pinecone Integrated Embeddings**: Uses Pinecone's built-in embedding models - no local models or external embedding APIs needed
- **Lightweight**: Minimal dependencies and cloud-native architecture  
- **Scalable**: Serverless vector database with automatic scaling
- **FastAPI**: Modern, high-performance web framework
- **Agentic RAG**: Advanced retrieval-augmented generation with conversational agents

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
│   ├── embeddings.py          # Pinecone integrated embeddings
│   ├── vector_store.py        # Pinecone with integrated embeddings
│   ├── llm_setup.py
│   └── prompt_templates.py
├── knowledge_base/
│   ├── __init__.py
│   └── docs/
│       └── abc_company_info.md
└── scripts/
    ├── __init__.py
    └── ingest_data.py           # Pinecone data ingestion
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
    # Pinecone Configuration (with integrated embeddings)
    PINECONE_API_KEY=your_pinecone_api_key_here
    PINECONE_INDEX_NAME=abc-assistant-integrated
    PINECONE_CLOUD=aws
    PINECONE_REGION=us-east-1
    
    # LLM Configuration
    GROQ_API_KEY=your_groq_api_key_here
    ```
    
    You can use `.env.example` as a template.

## Setup Guide

### Pinecone Setup

1.  **Create a Pinecone account:**
    - Sign up at [Pinecone](https://www.pinecone.io/)
    - Create a new project
    - Get your API key from the console
    - Add it to your `.env` file

2.  **Index Creation:**
    The application will automatically create a Pinecone index with integrated embeddings when you run the ingestion script. No manual index creation needed!

## Running the Application

1.  **Ingest Knowledge Base Documents:**
    ```bash
    python scripts/ingest_data.py
    ```
    
    This will create a Pinecone index with integrated embeddings and upload your documents to it.

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## Key Features

- **Pinecone Integrated Embeddings**: No local models or external embedding APIs needed
- **Automatic Index Creation**: Creates Pinecone index with integrated embeddings automatically  
- **Cloud-Native**: Lightweight, serverless architecture
- **Environment-based Configuration**: Easy configuration through environment variables
- **Modern FastAPI**: High-performance web framework with automatic API documentation

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

