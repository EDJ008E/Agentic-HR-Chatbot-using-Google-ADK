from typing import List
from langchain_core.documents import Document
from .base_tool import BaseHRTool

class HRFormsTool(BaseHRTool):
    """Tool for handling HR forms and procedures queries"""
    
    def __init__(self, vector_db):
        super().__init__(vector_db)
        self.tool_name = "hr_forms_tool"
        self.description = "Handles queries about HR forms and procedures"
        self.keywords = [
            "form", "procedure", "process", "application",
            "request", "template", "document", "paperwork",
            "how to apply", "where to find", "submit", "download"
        ]
    
    def is_relevant_query(self, query: str) -> bool:
        """Check if query is about HR forms"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)
    
    def process_query(self, query: str, documents: List[Document]) -> str:
        """Process HR forms queries"""
        response = "Here's information about HR forms and procedures:\n\n"

        if "where" in query.lower() and "form" in query.lower():
            response = "You can find the requested form here:\n\n"
        elif "how to" in query.lower() and ("apply" in query.lower() or "submit" in query.lower()):
            response = "Here's the process you need to follow:\n\n"
        
        return response + self.format_response(documents)