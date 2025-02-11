from docx import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Extract QA Pairs from a Word file with "QUESTION:" and "ANSWER:" format.
def extract_qa_pairs(file_path):
    doc = Document(file_path)
    qa_pairs = []
    current_q = None
    current_a = []
    collect_answer = False

    for para in doc.paragraphs:
        text = para.text.strip()
        
        if text.startswith("QUESTION:"):
            if current_q:  
                qa_pairs.append({
                    "question": current_q,
                    "answer": " ".join(current_a).strip()
                })
            current_q = text[len("QUESTION:"):].strip()
            current_a = []
            collect_answer = False
        elif text.startswith("ANSWER:"):
            current_a.append(text[len("ANSWER:"):].strip())
            collect_answer = True
        elif collect_answer and text:
            current_a.append(text)

    # Add the last pair
    if current_q and current_a:
        qa_pairs.append({
            "question": current_q,
            "answer": " ".join(current_a).strip()
        })
    
    return qa_pairs

# Initialize embeddings with better parameters
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_kwargs={'device': 'cpu'},  # or 'cuda' if available
    encode_kwargs={'normalize_embeddings': True}
)

# Extract structured QA pairs
qa_pairs = extract_qa_pairs("../data/Chatbot Preprocessed Questions.docx")

# Combine questions and answers into a single text for embedding
combined_texts = [f"Question: {pair['question']} Answer: {pair['answer']}" for pair in qa_pairs]

# Create FAISS index with combined texts
faiss_index = FAISS.from_texts(
    texts=combined_texts,
    embedding=embeddings
)

# Save index
faiss_index.save_local("faiss_index_improved")
print("FAISS index saved successfully!")