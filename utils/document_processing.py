import streamlit as st
from docx import Document
import fitz  # PyMuPDF
import re
import arabic_reshaper
from bidi.algorithm import get_display
from pyarabic.araby import strip_tashkeel, normalize_hamza

@st.cache_data(ttl=3600)
def read_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

@st.cache_data(ttl=3600)
def read_pdf(file):
    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        full_text = []
        for page in pdf_document:
            text = page.get_text()
            full_text.append(text)
        return '\n'.join(full_text)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def read_txt(file):
    return file.read().decode("utf-8")

@st.cache_data(ttl=3600)
def preprocess_arabic_text(text):
    if isinstance(text, list):
        text = ' '.join(text)
    text = strip_tashkeel(normalize_hamza(text))
    text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
    text = ' '.join(text.split())
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def format_response(response):
    return response.replace("\n", "\n\n")
