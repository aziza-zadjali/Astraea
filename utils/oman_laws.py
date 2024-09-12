import streamlit as st
import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600, allow_output_mutation=True)
def get_oman_laws():
    """
    Retrieves a list of Oman laws from the database directory.
    
    Returns:
        dict: A dictionary where keys are law names and values are file paths.
    """
    DATABASE_DIR = "database"
    laws = {}
    
    # Check if the database directory exists
    if not os.path.exists(DATABASE_DIR):
        logger.error(f"Database directory '{DATABASE_DIR}' does not exist.")
        return laws
    
    # List files in the database directory
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(".pdf"):
            law_name = filename[:-4]  # Remove .pdf extension
            laws[law_name] = os.path.join(DATABASE_DIR, filename)
    
    return laws

@st.cache_data(ttl=3600, allow_output_mutation=True)
def read_oman_law(file_path):
    """
    Reads the content of an Oman law PDF file.
    
    Parameters:
        file_path (str): The path to the PDF file.
    
    Returns:
        str: The text content of the PDF file.
    """
    try:
        with fitz.open(file_path) as pdf_document:
            full_text = []
            for page in pdf_document:
                text = page.get_text()
                full_text.append(text)
            return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")
        return None

def add_to_chat_history(query, response, lang_code):
    """
    Adds a query and response to the chat history.
    
    Parameters:
        query (str): The user's query.
        response (str): The AI's response.
        lang_code (str): The language code (e.g., "en" or "ar").
    """
    st.session_state.chat_history.append({"query": query, "response": response, "language": lang_code})
