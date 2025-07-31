from typing import List
from langchain_core.documents import Document
from .base_tool import BaseHRTool

class HolidayCalendarTool(BaseHRTool):
    """Tool for handling holiday calendar queries"""
    
    def __init__(self, vector_db):
        super().__init__(vector_db)
        self.tool_name = "holiday_calendar_tool"
        self.description = "Handles queries about company holidays and calendar"
        self.use_case = "Holiday Calendar"
        self.keywords = [
            "holiday", "calendar", "public holiday", "company holiday",
            "day off", "holiday schedule", "holiday list", "festival"
        ]
    
    def is_relevant_query(self, query: str) -> bool:
        """Check if query is about holidays"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)