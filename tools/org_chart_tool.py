from typing import List
from langchain_core.documents import Document
from .base_tool import BaseHRTool

class OrgChartTool(BaseHRTool):
    """Tool for handling organization structure queries"""
    
    def __init__(self, vector_db):
        super().__init__(vector_db)
        self.tool_name = "org_chart_tool"
        self.description = "Handles queries about organizational structure and reporting"
        self.keywords = [
            "org chart", "organization", "structure", "reporting",
            "manager", "team lead", "department", "hierarchy",
            "who reports to", "reporting structure", "organization chart"
        ]
    
    def is_relevant_query(self, query: str) -> bool:
        """Check if query is about org structure"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)
    
    def process_query(self, query: str, documents: List[Document]) -> str:
        """Process org chart queries"""
        response = "Here's information about our organizational structure:\n\n"
        
        # Handle specific position queries
        if "who is" in query.lower() or "who's the" in query.lower():
            response = "Regarding specific positions:\n\n"
        elif "report" in query.lower() or "reporting" in query.lower():
            response = "Regarding reporting structure:\n\n"
        
        return response + self.format_response(documents)