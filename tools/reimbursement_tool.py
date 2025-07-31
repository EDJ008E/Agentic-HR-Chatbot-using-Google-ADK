from typing import List
from langchain_core.documents import Document
from .base_tool import BaseHRTool

class ReimbursementTool(BaseHRTool):
    """Tool for handling reimbursement queries"""
    
    def __init__(self, vector_db):
        super().__init__(vector_db)
        self.tool_name = "reimbursement_tool"
        self.description = "Handles queries about travel expenses and reimbursement"
        self.keywords = [
            "reimbursement", "expense", "travel", "claim",
            "receipt", "refund", "allowance", "per diem",
            "business trip", "travel policy", "mileage"
        ]
    
    def is_relevant_query(self, query: str) -> bool:
        """Check if query is about reimbursement"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)
    
    def process_query(self, query: str, documents: List[Document]) -> str:
        """Process reimbursement queries"""
        response = "Here's information about reimbursement policies:\n\n"
        
        if "travel" in query.lower():
            response = "Regarding travel reimbursement:\n\n"
        elif "meal" in query.lower() or "food" in query.lower():
            response = "Regarding meal allowances:\n\n"
        elif "receipt" in query.lower():
            response = "About receipt requirements for reimbursement:\n\n"
        
        return response + self.format_response(documents)