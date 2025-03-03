from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    """
    Create FAISS vector store with HuggingFace embeddings
    
    Args:
        chunks (list): List of text chunks
    
    Returns:
        FAISS: Vector store object
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)