import streamlit as st
import openai
from docx import Document
import fitz  # PyMuPDF
from pyarabic.araby import strip_tashkeel, normalize_hamza
from tenacity import retry, stop_after_attempt, wait_random_exponential
import arabic_reshaper
from bidi.algorithm import get_display
import re
import io
import sqlite3
from functools import lru_cache
import os
from openai import OpenAI

# Set page config at the very beginning
st.set_page_config(page_title="Astraea - Legal Query Assistant", page_icon="⚖️", layout="wide")

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define the path to your database directory
DATABASE_DIR = "database"

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY, query TEXT, response TEXT, language TEXT)''')
    conn.commit()
    conn.close()

def add_to_chat_history(query, response, language):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (query, response, language) VALUES (?, ?, ?)", (query, response, language))
    conn.commit()
    conn.close()

def get_chat_history(language):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT query, response FROM chat_history WHERE language = ? ORDER BY id DESC", (language,))
    results = c.fetchall()
    conn.close()
    return results

@st.cache_data(ttl=3600)
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_legal_advice(query, document_text=None, language="en"):
    try:
        system_content = {
            "en": "You are Astraea, an expert legal assistant specializing in legal documents. Provide detailed and accurate information based on the given document. Focus on key aspects such as the nature of the case, parties involved, legal issues, and court decisions.",
            "ar": "أنت أسترايا، مساعد قانوني خبير متخصص في الوثائق القانونية. قدم معلومات مفصلة ودقيقة بناءً على الوثيقة المعطاة. ركز على الجوانب الرئيسية مثل طبيعة القضية والأطراف المعنية والقضايا القانونية وقرارات المحكمة."
        }

        messages = [
            {"role": "system", "content": system_content[language]},
            {"role": "user", "content": query}
        ]

        if document_text:
            context_prompt = {
                "en": f"Document context: {document_text}\n\nProvide a detailed summary of the case, including the type of case, parties involved, main legal issues, and the court's decision if available.",
                "ar": f"سياق الوثيقة: {document_text}\n\nقدم ملخصًا مفصلاً للقضية، بما في ذلك نوع القضية والأطراف المعنية والقضايا القانونية الرئيسية وقرار المحكمة إن وجد."
            }
            messages.append({"role": "user", "content": context_prompt[language]})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000,
            stream=True
        )

        collected_messages = []
        for chunk in response:
            if chunk.choices[0].finish_reason is not None:
                break
            collected_messages.append(chunk.choices[0].delta.content or '')

        full_response = ''.join(collected_messages).strip()
        return full_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

@st.cache_data
def read_txt(file):
    return file.read().decode("utf-8")

@lru_cache(maxsize=1000)
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

@st.cache_data(ttl=3600)
def generate_suggested_questions(document_text, language):
    try:
        prompt = {
            "en": f"Based on the following legal document, generate 5 relevant questions that a user might ask about the case:\n\n{document_text[:2000]}...",
            "ar": f"بناءً على الوثيقة القانونية التالية، قم بإنشاء 5 أسئلة ذات صلة قد يطرحها المستخدم حول القضية:\n\n{document_text[:2000]}..."
        }

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates relevant questions based on legal documents."},
                {"role": "user", "content": prompt[language]}
            ],
            max_tokens=200
        )

        suggested_questions = response.choices[0].message.content.strip().split('\n')
        return [q.strip('1234567890. ') for q in suggested_questions if q.strip()]
    except Exception as e:
        st.error(f"Error generating suggested questions: {str(e)}")
        return []

def get_oman_laws():
    laws = {}
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(".pdf"):
            law_name = filename[:-4]  # Remove .pdf extension
            laws[law_name] = os.path.join(DATABASE_DIR, filename)
    return laws

def read_oman_law(file_path):
    try:
        with fitz.open(file_path) as pdf_document:
            full_text = []
            for page in pdf_document:
                text = page.get_text()
                full_text.append(text)
        return '\n'.join(full_text)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None


def main():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    language = st.sidebar.selectbox("Choose Language / اختر اللغة", ["English", "العربية"])
    lang_code = "en" if language == "English" else "ar"

    if lang_code == "ar":
        st.markdown('<style>body {direction: rtl;}</style>', unsafe_allow_html=True)

    title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
    st.title(title)

    disclaimer = {
        "en": "This assistant uses GPT-3.5-turbo to provide general legal information. Please note that this is not a substitute for professional legal advice.",
        "ar": "يستخدم هذا المساعد نموذج GPT-3.5-turbo لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
    }
    st.write(disclaimer[lang_code])

    option_text = {
        "en": "Choose a feature",
        "ar": "اختر ميزة"
    }
    feature_options = {
        "en": ('Query from Document', 'Get Legal Advice', 'Oman Laws'),
        "ar": ('استعلام من وثيقة', 'الحصول على استشارة قانونية', 'قوانين عمان')
    }
    option = st.selectbox(option_text[lang_code], feature_options[lang_code])

    if option == feature_options[lang_code][0]:  # Query from Document
        # ... (rest of the code for this option remains the same)

    elif option == feature_options[lang_code][1]:  # Get Legal Advice
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:")
        
        if st.button("Submit" if lang_code == "en" else "إرسال"):
            if query:
                with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                    response = get_legal_advice(query, language=lang_code)
                    st.markdown("### Response:")
                    st.markdown(format_response(response))
                    st.session_state.chat_history.append((query, response))
            else:
                st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")

    elif option == feature_options[lang_code][2]:  # Oman Laws
        # ... (rest of the code for this option remains the same)

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("## Chat History")
        for query, response in st.session_state.chat_history:
            st.text_area("Query", query, height=100)
            st.text_area("Response", response, height=200)
            st.markdown("---")

if __name__ == "__main__":
    main()
