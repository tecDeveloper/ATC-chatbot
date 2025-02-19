import os
import sys

import logging
# Configure logging once
logging.basicConfig(
    filename='app.logs',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(name)s]'
)

# Create a logger for this module
logger = logging.getLogger(__name__)



# Set the working directory paths
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from services.langchain_service import chat_prompt, model

# Vector Db Suppporting variables and functions 
from utils.loading_streamlit import load_embeddings_and_index

# for streamlit
import streamlit as st

# For displaying the chat 
from streamlit_dir.streamlit_support_functions import display_chat








# For loading embeddings
from utils.loading_streamlit import load_embeddings_and_index
embeddings, faiss_index = load_embeddings_and_index(HuggingFaceEmbeddings,FAISS)


# Initialize Streamlit app
st.title("Your Assistant")
# Apply custom CSS to hide the bottom profile image and Streamlit icon
st.markdown(
    """
    <style>
        /* Hide Streamlit branding */
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Cover the bottom right profile image and Streamlit icon */
        [data-testid="stDecoration"] {
            background-color: white !important;
            height: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize LangChain memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Add the welcoming message as the first assistant response
    welcome_message = "Hi! This is Laila from ATCMarket. Glad to be at your service. How can I help you?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})




# Chat Section
 
# Display existing chat history on app rerun
display_chat()







# User Query Section

# User query input
if user_query := st.chat_input("Ask"):
    # Add user message to LangChain memory
    st.session_state.memory.chat_memory.add_user_message(user_query)

    # Add user query to chat history for display
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Immediately display the user's message
    with st.chat_message("user"):
        st.markdown(user_query)

    logging.info(f"USer query was: {user_query}")
    # Perform similarity search with FAISS
    results = faiss_index.similarity_search(user_query, k=5)
    logger.info("Result of similarity is: ",results)
    context = "\n".join([result.page_content for result in results])
    logging.info(f"Similarity search is: {context}")

    # Prepare input for the model
    system_message = f"Information you need to answer is:\n{context}\n"
    user_message = f"User query was: {user_query}"

    # Add assistant's context to memory
    st.session_state.memory.chat_memory.add_ai_message(system_message)

    # Generate a response using the model
    with st.chat_message("assistant"):
        response_container = st.empty() 
        full_response = ""

        for chunk in model.stream(chat_prompt.format(messages=st.session_state.memory.chat_memory.messages)):
            full_response += chunk.content
            response_container.markdown(full_response)  
    logging.info(f"Model's response is: {full_response}")
    # Add assistant response to LangChain memory
    st.session_state.memory.chat_memory.add_ai_message(full_response)

    # Add assistant response to chat history for display
    st.session_state.messages.append({"role": "assistant", "content": full_response})
