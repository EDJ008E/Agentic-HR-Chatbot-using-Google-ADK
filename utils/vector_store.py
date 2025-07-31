import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

class VectorStoreManager:
    """Manages loading and accessing the FAISS vector store"""
    
    def __init__(self, index_path: str = "faiss_index"):
        self.index_path = index_path
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_db = None
    
    def load_vector_store(self) -> bool:
        """Load the FAISS index"""
        try:
            self.vector_db = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def get_vector_db(self) -> FAISS:
        """Get the loaded vector database"""
        return self.vector_db