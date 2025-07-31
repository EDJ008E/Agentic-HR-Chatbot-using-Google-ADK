from abc import ABC, abstractmethod
from typing import List
import re  # For cleaning unwanted text
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.gemini_client import GeminiClient

class BaseHRTool(ABC):
    """Base class for all HR tools with common functionality"""
    
    def __init__(self, vector_db: FAISS):
        self.vector_db = vector_db
        self.tool_name = "base_hr_tool"
        self.description = "Base HR tool for document retrieval"
        self.gemini_client = GeminiClient()  
        self.use_case = "General HR Inquiry"
    
    @abstractmethod
    def is_relevant_query(self, query: str) -> bool:
        """Determine if this tool should handle the query"""
        pass
    
    def retrieve_documents(self, query: str, k: int = 3) -> List[Document]:
        """Retrieve relevant documents from the vector store"""
        return self.vector_db.similarity_search(query, k=k)
    
    def format_context(self, documents: List[Document]) -> str:
        """Format documents into context string for Gemini"""
        if not documents:
            return "No relevant documents found in company records."
        
        context = []
        for doc in documents:
            # Remove bracketed or parenthetical section references
            cleaned_content = re.sub(r"\[(.*?)\]", "", doc.page_content)  # Removes [Section titles]
            cleaned_content = re.sub(r"\((.*?)\)", "", cleaned_content)   # Removes (section refs)
            context.append(cleaned_content.strip())
        return "\n".join(context)
    
    def generate_response(self, query: str, documents: List[Document]) -> str:
        """Generate response using Gemini API"""
        context = self.format_context(documents)
        raw_response = self.gemini_client.generate_hr_response(
            context=context,
            query=query,
            use_case=self.use_case
        )
        # Remove hallucinated (Source: ...) refs from model output
        cleaned_response = re.sub(r"\(Source:.*?\)", "", raw_response).strip()
        return cleaned_response
    
    def run(self, query: str) -> str:
        """Main method to handle the query"""
        if not self.is_relevant_query(query):
            return (
                "I'm here to assist only with HR and company-related questions. "
                "Topics like food, entertainment, or general inquiries are outside my scope. "
                "Please ask about leave policy, reimbursements, holidays, org charts, or HR forms."
            )
        
        documents = self.retrieve_documents(query)
        return self.generate_response(query, documents)
