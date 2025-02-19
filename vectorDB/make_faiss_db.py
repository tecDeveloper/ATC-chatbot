# For making embeddings
from langchain.embeddings import HuggingFaceEmbeddings

#  For Data extraction and preprocessing
from support_functions import extract_qa_pairs

#  for creating and storing FAISS 
from support_functions import save_faiss_db, make_faiss_vector_db


import logging
# Configure logging once
logging.basicConfig(
    filename='app.logs',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(name)s]'
)



# Initialize embeddings with better parameters
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_kwargs={'device': 'cpu'}, 
    encode_kwargs={'normalize_embeddings': True}
)

# Extract structured QA pairs
qa_pairs = extract_qa_pairs("../data/Chatbot Preprocessed Questions.docx")



# Combine questions and answers into a single text for embedding
combined_texts = [f"Question: {pair['question']} Answer: {pair['answer']}" for pair in qa_pairs]



# Make vector DB
faiss_index = make_faiss_vector_db(combined_texts, embeddings)

# Save index
save_faiss_db(faiss_index)