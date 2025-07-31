from langchain_google_genai import ChatGoogleGenerativeAI
import os

class GeminiClient:
    """Wrapper for Gemini API with HR-specific prompting"""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            top_p=0.85
        )

    def generate_hr_response(self, context: str, query: str, use_case: str) -> str:
        """
        Generate a structured HR response using Gemini.
        If query is general/greeting-like, return static intro.
        """
        if self._is_greeting(query):
            return self._greeting_response()

        try:
            prompt = self._build_hr_prompt(context, query, use_case)
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error generating Gemini response: {str(e)}")
            return self._fallback_response(query, use_case)

    def _build_hr_prompt(self, context: str, query: str, use_case: str) -> str:
        """Constructs the HR-specific prompt for Gemini."""
        return f"""
ROLE: You are an expert HR assistant for a large company.
TASK: Answer the employee's question based on company documents.

USE CASE: {use_case}
USER QUESTION: "{query}"

COMPANY DOCUMENTS:
{context if context else "No relevant documents found"}

INSTRUCTIONS:
1. Start with "Detected Use Case: [use case]"
2. Provide a clear, accurate answer from the documents
3. If listing items (dates, policies), use bullet points
4. Mention document sources when possible
5. If information is incomplete, say so honestly
6. Keep response professional but friendly

FORMAT EXAMPLE:
Detected Use Case: Holiday Calendar
The company holidays for this year are:
- New Year's Day: January 1
- Independence Day: July 4
Source: Company_Holidays_2025.pdf

YOUR RESPONSE:
"""

    def _fallback_response(self, query: str, use_case: str) -> str:
        """Fallback when Gemini fails"""
        return f"""
I apologize, but I encountered a technical difficulty processing your query.

Detected Use Case: {use_case}
Question: {query}

Please try rephrasing your question or contact HR directly for assistance.
"""

    def _is_greeting(self, query: str) -> bool:
        """Check if the query is a greeting or casual question"""
        greetings = [
            "hello", "hi", "hey", "who are you", "can you tell about yourself",
              "introduce yourself","tell about you", "about yourself","what you do for me "
                ]
        return any(greet in query.lower() for greet in greetings)

    def _greeting_response(self) -> str:
        """Static response for greeting-like prompts"""
        return """
Detected Use Case: General HR Inquiry

Hello! I’m your virtual HR assistant, designed to help you with any questions related to company policies, benefits, forms, holidays, reimbursements, and more.

While I don’t have a personal background like a human, I can guide you through the HR information provided by your organization.

Please feel free to ask about any HR-related topic — for example:
- "What is the leave policy?"
- "How to apply for reimbursement?"
- "Can you show me the holiday calendar?"

I’m here to help!
"""
