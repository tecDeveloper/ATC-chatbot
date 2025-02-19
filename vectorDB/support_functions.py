# For vector DB
from langchain.vectorstores import FAISS

# Now because the data is in word document so we need to import
from docx import Document


# For logging
import logging
# Create a logger for this module
logger = logging.getLogger(__name__)







# For Data preprocessing
# Extract QA Pairs from a Word file with "QUESTION:" and "ANSWER:" format.
def extract_qa_pairs(file_path):
    """ This function takes path of docs, extract data from it and make pairs of question answers for embeddings
    INPUT:
        directory_name/file_name
        
    OUTPUT:
        qa_pairs (which countains pairs of question/answers).
        - Each pair contains a question and its answer
    """
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






def make_faiss_vector_db(combined_texts, embeddings):
    
    """ The Fuction creates a FAISS INDEX.
    INPUT:
        -text: combined_text (which has a question and its answer)
        - Embddings 
        """
    
    try:
        # Create FAISS index with combined texts
        faiss_index = FAISS.from_texts(
            texts=combined_texts,
            embedding=embeddings
        )
        logger.info("FAISS DB created sucessfully")
        return faiss_index
    except Exception as e:
        logger.error(f"Error while creating FAISS DB: {str(e)}")



def save_faiss_db(faiss_index):
    """ Save index of FAISS 
    INPUT:
        FAISS index 
    
    OUTPUT:
        - No output
        - Just saves index in the same directory
    """
    try:
        faiss_index.save_local("faiss_index")
        logger.info("FAISS index saved successfully!")
    except Exception as e:
        logger.error(f"Error while saving FAISS Db: {str(e)}")
        raise


