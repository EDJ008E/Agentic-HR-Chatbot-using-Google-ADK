import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def load_faiss_index(index_path="faiss_index"):
    """
    Load existing FAISS index with safe deserialization
    """
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db = FAISS.load_local(
            index_path, 
            embeddings,
            allow_dangerous_deserialization=True  
        )
        print("FAISS index loaded successfully!")
        return db
    except Exception as e:
        print(f"Error loading index: {str(e)}")
        return None

def query_index(db, query, k=3):
    """
    Query the FAISS index and display results
    """
    if not db:
        print("No database loaded. Please check the index path.")
        return
    
    try:
        print(f"\nQuery: '{query}'")
        print(f"Top {k} most relevant results:")
        
        docs = db.similarity_search(query, k=k)
        
        for i, doc in enumerate(docs):
            print(f"\nResult {i+1}:")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content: {doc.page_content[:300]}...")  
            
    except Exception as e:
        print(f"Error querying index: {str(e)}")

def interactive_query(db):
    """
    Interactive query interface
    """
    if not db:
        return
        
    print("\nInteractive query mode (type 'exit' to quit)")
    while True:
        query = input("\nEnter your query: ")
        if query.lower() in ['exit', 'quit']:
            break
        query_index(db, query)

if __name__ == "__main__":

    os.environ["GOOGLE_API_KEY"] = ""  # enter the API key here
    
    print("Loading FAISS index...")
    vector_db = load_faiss_index()
    
    if vector_db:
        interactive_query(vector_db)
    else:
        print("Failed to load index. Please ensure:")
        print("1. You've run create_index.py first")
        print("2. The 'faiss_index' folder exists in your project directory")
        print("3. You have the correct permissions to access the files")