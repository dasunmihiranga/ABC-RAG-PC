# core/agent.py
# Contains the main Agent (ABCBot) logic 

from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda, RunnableBranch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from operator import itemgetter

from core.llm_setup import get_llm
from core.vector_store import get_vector_store, get_retriever
from core.prompt_templates import human_prompt

store = {}

# Define the out-of-knowledge response as per your prompt templates
OUT_OF_KNOWLEDGE_RESPONSE = "I'm ABCBot, ABC's virtual assistant. I can only help with questions about ABC's services, company information, and how we can assist with your business needs. For questions outside of ABC's scope, please feel free to contact our team directly at info@abc.com or call 0123456789."

# Keywords that indicate ABC-related questions
ABC_KEYWORDS = [
    "abc", "company", "service", "services", "development", "software", "ai", "machine learning",
    "mobile", "web", "cloud", "devops", "saas", "digital transformation", "custom", "solution",
    "team", "expert", "contact", "price", "pricing", "cost", "project", "client", "portfolio",
    "technology", "innovation", "business", "enterprise", "application", "platform", "system",
    "what do you do", "tell me about", "how can you help", "what services", "expertise"
]

# Non-ABC topics that should be rejected
IRRELEVANT_KEYWORDS = [
    "weather", "sports", "news", "politics", "cooking", "recipe", "movie", "music", "game",
    "celebrity", "travel", "restaurant", "hotel", "fashion", "shopping", "medical advice",
    "legal advice", "personal", "relationship", "dating", "homework", "assignment", "math",
    "science", "history", "geography", "physics", "chemistry", "biology", "literature"
]

def is_abc_related_question(query: str) -> bool:
    """Check if the question is related to ABC company or business inquiries."""
    query_lower = query.lower()
    
    # Check for irrelevant topics first
    for keyword in IRRELEVANT_KEYWORDS:
        if keyword in query_lower:
            return False
    
    # Check for ABC-related keywords
    for keyword in ABC_KEYWORDS:
        if keyword in query_lower:
            return True
    
    # Check for business-related inquiry patterns
    business_patterns = [
        "i need", "looking for", "want to", "interested in", "can you help",
        "tell me more", "what is", "how does", "quote", "estimate", "consultation"
    ]
    
    for pattern in business_patterns:
        if pattern in query_lower:
            return True
    
    return False

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_agent_chain():
    """
    Initializes and returns the main ABC Assistant agent chain with Pinecone integrated embeddings.
    """
    llm = get_llm()
    index = get_vector_store()  # Returns Pinecone index directly
    retriever = get_retriever(index)  # Custom retriever for integrated embeddings

    # Define the condition for checking if question is ABC-related
    def is_question_relevant(input_dict):
        query = input_dict.get("input", "")
        return is_abc_related_question(query)

    # Define the condition for checking if context is empty or insufficient
    def is_context_empty(input_dict):
        context = input_dict.get("context")
        if not context:
            return True
        
        # Check if any retrieved document has meaningful content
        meaningful_content = False
        for doc in context:
            if doc.page_content.strip() and len(doc.page_content.strip()) > 20:
                meaningful_content = True
                break
        
        return not meaningful_content

    # Define the branch for irrelevant questions
    irrelevant_question_branch = RunnableLambda(lambda x: OUT_OF_KNOWLEDGE_RESPONSE)
    
    # Define the branch for when context is empty
    out_of_knowledge_branch = RunnableLambda(lambda x: "I don't have specific information about that in ABC's knowledge base. For detailed inquiries, please contact us at info@abc.com or call 0123456789.")

    # Define the main RAG processing branch with enhanced validation
    def process_with_context_validation(input_dict):
        context = input_dict.get("context", [])
        query = input_dict.get("input", "")
        
        # Double-check if the retrieved context is actually relevant to ABC
        relevant_context = []
        for doc in context:
            content_lower = doc.page_content.lower()
            if any(keyword in content_lower for keyword in ["abc", "company", "service", "development", "software"]):
                relevant_context.append(doc)
        
        if not relevant_context:
            return "I don't have specific information about that in ABC's knowledge base. For detailed inquiries, please contact us at info@abc.com or call 0123456789."
        
        # Update the context with only relevant documents
        input_dict["context"] = relevant_context
        return input_dict

    rag_processing_branch = (
        RunnableLambda(process_with_context_validation)
        | human_prompt
        | llm
        | StrOutputParser()
    )

    # Define the full RAG chain with conditional logic
    full_rag_chain = (
        {
            "context": itemgetter("input") | retriever,
            "chat_history": itemgetter("chat_history"),
            "input": itemgetter("input"),
        }
        | RunnableBranch(
            (lambda x: not is_question_relevant(x), irrelevant_question_branch),  # Check relevance first
            (is_context_empty, out_of_knowledge_branch),  # Then check if context is empty
            rag_processing_branch,  # Finally, process with RAG if all checks pass
        )
    )

    # Wrap the RAG chain with message history
    with_message_history = RunnableWithMessageHistory(
        full_rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return with_message_history 