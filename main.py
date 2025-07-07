# main.py
# This is the FastAPI application entry point, defines /chat API 
# Updated to work with Pinecone vector database instead of ChromaDB
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from core.agent import get_agent_chain
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ABC Assistant Chatbot API",
    description="API for ABC Assistant, a professional company assistant powered by Agentic RAG with Pinecone.",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent chain
agent_chain = get_agent_chain()

class ChatRequest(BaseModel):
    query: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    try:
        response_raw = agent_chain.invoke(
            {"input": request.query},
            config={
                "configurable": {"session_id": request.session_id}
            },
        )

        # Ensure the response content is a string explicitly
        if isinstance(response_raw, AIMessage):
            response_content = str(response_raw.content)
        else:
            # For any other type, directly convert to string
            response_content = str(response_raw)
            
        return {"response": response_content}
    except Exception as e:
        # Log the full exception for debugging
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ABC Assistant Chatbot API",
        "version": "2.0.0",
        "description": "Professional company assistant powered by Agentic RAG with Pinecone",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)",
            "openapi": "/openapi.json (GET)"
        },
        "powered_by": "Pinecone + LangChain + FastAPI"
    }

@app.get("/info")
async def system_info():
    """System information for monitoring"""
    try:
        # Check if environment variables are available
        pinecone_configured = bool(os.getenv("PINECONE_API_KEY"))
        groq_configured = bool(os.getenv("GROQ_API_KEY"))
        
        return {
            "status": "healthy",
            "environment": {
                "pinecone_configured": pinecone_configured,
                "groq_configured": groq_configured,
                "index_name": os.getenv("PINECONE_INDEX_NAME", "not-set"),
                "region": os.getenv("PINECONE_REGION", "not-set")
            },
            "timestamp": str(os.popen('date').read().strip()) if os.name != 'nt' else "timestamp-unavailable"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e)
        }