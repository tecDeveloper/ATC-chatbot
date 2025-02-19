import streamlit as st


# Function to display chat messages in real-time
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])