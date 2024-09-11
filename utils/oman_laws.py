import streamlit as st
import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)

@st.cache_data
def get_oman_laws():
    DATABASE_DIR = "database"
    laws = {}
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(".pdf"):
            law_name = filename[:-4]  # Remove .pdf extension
            laws[law_name] = os.path.join(DATABASE_DIR, filename)
    return laws

@st.cache_data
def read_oman_law(file_path):
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
    st.session_state.chat_history.append({"query": query, "response": response, "language": lang_code})
