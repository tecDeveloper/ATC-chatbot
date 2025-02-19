import streamlit as st



# For logging
import logging
# Create a logger for this module
logger = logging.getLogger(__name__)

# Cache the embeddings and FAISS index to load them only once
@st.cache_resource
def load_embeddings_and_index(HuggingFaceEmbeddings,FAISS):
    try:
        logger.info("Loading FAISS...")
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
        # Load FAISS index
        faiss_index = FAISS.load_local("./vectorDB/faiss_index", embeddings, allow_dangerous_deserialization=True)
        return embeddings, faiss_index
    except Exception as e:
        logger.error(f"Error while loading the embeddings in support_functions.py: {str(e)}")
        raise
