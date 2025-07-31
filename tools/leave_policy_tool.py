from typing import List
from langchain_core.documents import Document
from .base_tool import BaseHRTool

class LeavePolicyTool(BaseHRTool):
    """Tool for handling leave policy queries"""
    
    def __init__(self, vector_db):
        super().__init__(vector_db)
        self.tool_name = "leave_policy_tool"
        self.description = "Handles queries about leave policies, sick leave, annual leave, etc."
        self.keywords = [
            "leave", "vacation", "sick", "holiday", "time off",
            "annual leave", "casual leave", "maternity", "paternity",
            "leave policy", "leave balance", "leave quota"
        ]
        self.required_fields = ["name", "emp id", "manager name", "days", "date", "reason"]
    
    def is_relevant_query(self, query: str) -> bool:
        """Check if query is about leave policies"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)
        
    def process_query(self, query: str, documents: List[Document]) -> str:
        """Process leave policy queries"""
        # Check if this is a leave application
        if self._is_leave_application(query):
            return self._process_leave_application(query, documents)
        
        # Otherwise handle as general policy query
        base_response = "Here's information about our leave policies:\n\n"
        detailed_response = self.format_response(documents)
        
        if "sick" in query.lower():
            base_response = "Regarding sick leave policies:\n\n"
        elif "annual" in query.lower() or "vacation" in query.lower():
            base_response = "Regarding annual/vacation leave:\n\n"
        
        return base_response + detailed_response
    
    def _is_leave_application(self, query: str) -> bool:
        """Check if the query contains leave application details"""
        query_lower = query.lower()
        return ("apply" in query_lower or "application" in query_lower) and any(
            field in query_lower for field in ["name", "emp id", "employee id", "manager"]
        )
    
    def _process_leave_application(self, query: str, documents: List[Document]) -> str:
        """Handle leave application submission"""
        # Extract details from query (simplified - in real app you'd use NLP)
        details = {
            "name": self._extract_detail(query, ["name", "employee"]),
            "emp_id": self._extract_detail(query, ["emp id", "employee id"]),
            "manager": self._extract_detail(query, ["manager", "reporting to"]),
            "days": self._extract_detail(query, ["days", "duration"]),
            "date": self._extract_detail(query, ["date", "on"]),
            "reason": self._extract_detail(query, ["reason", "because"])
        }
        
        # Check if all required fields are present
        missing_fields = [field for field in self.required_fields if not details.get(field.lower().replace(" ", "_"))]
        if missing_fields:
            return (
                f"I need more information to process your leave application. "
                f"Please provide: {', '.join(missing_fields)}.\n\n"
                f"Example format: 'I want to apply for leave. Name: John, Emp ID: 123, Manager: Alice, "
                f"Days: 2, Date: 2025-07-25, Reason: Family event'"
            )
        
        # Here you would normally validate against database
        # For now we'll assume validation passes
        return (
            f"Leave application received for {details['name']} (ID: {details['emp_id']}):\n"
            f"- Duration: {details['days']} days\n"
            f"- Dates: {details['date']}\n"
            f"- Reason: {details['reason']}\n"
            f"- Reporting to: {details['manager']}\n\n"
            "Your leave application has been submitted for approval. "
            "You'll receive a confirmation email shortly."
        )
    
    def _extract_detail(self, query: str, keywords: List[str]) -> str:
        """Simple extraction of details from query (improve with NLP in production)"""
        query_lower = query.lower()
        for keyword in keywords:
            if keyword in query_lower:
                # Find the text after the keyword
                start_idx = query_lower.find(keyword) + len(keyword)
                end_idx = query_lower.find(",", start_idx) if "," in query_lower[start_idx:] else len(query_lower)
                return query[start_idx:end_idx].strip(" :;,")
        return ""