import os
import glob
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_excel_as_documents(excel_path):
    """Load Excel rows as structured documents"""
    df = pd.read_excel(excel_path)
    docs = []

    for _, row in df.iterrows():
        row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col]))
        doc = Document(page_content=row_text, metadata={"source": excel_path})
        docs.append(doc)

    return docs


def load_documents(doc_paths):
    """Load and process documents from specified paths"""
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for folder_name, folder_path in doc_paths.items():
        print(f"\nProcessing: {folder_name}")
        
        try:
            # Process Excel files
            if "excel" in folder_name.lower() or "chart" in folder_name.lower():
                for excel_file in glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls")):
                    try:
                        docs = load_excel_as_documents(excel_file)
                        split_docs = text_splitter.split_documents(docs)
                        documents.extend(split_docs)
                        print(f"✓ Loaded Excel: {os.path.basename(excel_file)}")
                    except Exception as e:
                        print(f"× Failed Excel: {os.path.basename(excel_file)} - {str(e)}")

            # Process Word files
            elif "word" in folder_name.lower() or "form" in folder_name.lower() or "policy" in folder_name.lower():
                for doc_file in glob.glob(os.path.join(folder_path, "*.docx")) + glob.glob(os.path.join(folder_path, "*.doc")):
                    try:
                        loader = Docx2txtLoader(doc_file)
                        docs = loader.load()
                        split_docs = text_splitter.split_documents(docs)
                        documents.extend(split_docs)
                        print(f"✓ Loaded Word: {os.path.basename(doc_file)}")
                    except Exception as e:
                        print(f"× Failed Word: {os.path.basename(doc_file)} - {str(e)}")

        except Exception as e:
            print(f"! Folder error: {folder_name} - {str(e)}")

    return documents


def create_faiss_index(documents, index_name="faiss_index"):
    """Create and save FAISS index"""
    try:
        print("\nCreating embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        print("Building FAISS index...")
        db = FAISS.from_documents(documents, embeddings)

        print(f"Saving index to '{index_name}'...")
        db.save_local(index_name)
        print("✓ Index created successfully!")
        return db
    except Exception as e:
        print(f"× Index creation failed: {str(e)}")
        return None


if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = "# enter the API key here" # enter the API key here

    base_path = os.path.abspath("docs")
    doc_paths = {
        "Holiday calendar (Excel)": os.path.join(base_path, "Holiday calendar (Excel)"),
        "HR form (WORD)": os.path.join(base_path, "HR form (WORD)"),
        "Hr policy (WORD)": os.path.join(base_path, "Hr policy (WORD)"),
        "Organization chart": os.path.join(base_path, "Organization chart"),
        "Reimbursement rules (WORD)": os.path.join(base_path, "Reimbursement rules (WORD)")
    }

    # Verify paths exist
    for name, path in doc_paths.items():
        if not os.path.exists(path):
            print(f"⚠️ Path does not exist: {path}")
        else:
            print(f"✓ Path exists: {path}")

    # ========== EXECUTION ========== #
    print("\nStarting document processing...")
    all_documents = load_documents(doc_paths)

    if all_documents:
        print(f"\nTotal documents processed: {len(all_documents)}")
        vector_db = create_faiss_index(all_documents)
    else:
        print("\nNo documents were loaded. Please check:")
        print("- All paths above should show as existing")
        print("- Files should have correct extensions (.xlsx, .docx, etc.)")
        print("- You have read permissions for all files")
