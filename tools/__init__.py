from typing import Dict, Any
from .leave_policy_tool import LeavePolicyTool
from .holiday_calendar_tool import HolidayCalendarTool
from .reimbursement_tool import ReimbursementTool
from .org_chart_tool import OrgChartTool
from .hr_forms_tool import HRFormsTool
from utils.gemini_client import GeminiClient

class HRToolManager:
    """Manages all HR tools and routes queries to the appropriate one"""
    
    def __init__(self, vector_db):
        self.tools = {
            "leave_policy": LeavePolicyTool(vector_db),
            "holiday_calendar": HolidayCalendarTool(vector_db),
            "reimbursement": ReimbursementTool(vector_db),
            "org_chart": OrgChartTool(vector_db),
            "hr_forms": HRFormsTool(vector_db)
        }
        self.gemini_client = GeminiClient()  # Initialize Gemini client here
    
    def get_tool_for_query(self, query: str) -> Any:
        """Find the most appropriate tool for the given query"""
        relevant_tools = []
        
        for tool_name, tool in self.tools.items():
            if tool.is_relevant_query(query):
                relevant_tools.append((tool_name, tool))
        
        if not relevant_tools:
            return None

        def count_matches(tool_pair):
            tool_name, tool = tool_pair
            return sum(keyword in query.lower() for keyword in tool.keywords)
        
        relevant_tools.sort(key=count_matches, reverse=True)
        return relevant_tools[0][1]
    
    def process_query(self, query: str) -> str:
        """Process the query using the most appropriate tool"""
        tool = self.get_tool_for_query(query)
        
        if not tool:
            # Handle unrecognized queries with Gemini
            return self.gemini_client.generate_hr_response(
                context="No specific HR documents matched this query",
                query=query,
                use_case="General HR Inquiry"
            )
        
        return tool.run(query)