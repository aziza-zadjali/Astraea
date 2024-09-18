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

@st.cache_data(ttl=3600)
def generate_suggested_questions(document_text, lang_code):
    try:
        prompt = {
            "en": f"Based on the following legal document, generate 5 relevant questions that a user might ask about the case:\n\n{document_text[:2000]}...",
            "ar": f"بناءً على الوثيقة القانونية التالية، قم بإنشاء 5 أسئلة ذات صلة قد يطرحها المستخدم حول القضية:\n\n{document_text[:2000]}..."
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates relevant questions based on legal documents."},
                {"role": "user", "content": prompt[lang_code]}
            ],
            max_tokens=200
        )

        suggested_questions = response.choices[0].message['content'].strip().split('\n')
        return [q.strip('1234567890. ') for q in suggested_questions if q.strip()]
    except Exception as e:
        logger.error(f"Error generating suggested questions: {str(e)}")
        return []
        
# Removed add_to_chat_history function as it's no longer needed
