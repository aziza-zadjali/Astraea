import streamlit as st
import openai
from docx import Document
import fitz  # PyMuPDF
from pyarabic.araby import strip_tashkeel, normalize_hamza
from tenacity import retry, stop_after_attempt, wait_random_exponential
import arabic_reshaper
from bidi.algorithm import get_display
import re
import sqlite3
from functools import lru_cache
import os

st.set_page_config(page_title="Astraea - Legal Query Assistant", page_icon="⚖️", layout="wide")

openai.api_key = st.secrets["OPENAI_API_KEY"]

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
    c.execute("INSERT INTO chat_history (query, response, language) VALUES (?, ?, ?)", 
              (query, response, language))
    conn.commit()
    conn.close()

def get_chat_history(language):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT query, response FROM chat_history WHERE language = ? ORDER BY id DESC", 
              (language,))
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
            chunk_size = 4000
            chunks = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]
            summaries = []

            for i, chunk in enumerate(chunks):
                context_prompt = {
                    "en": f"Document context (Part {i+1}/{len(chunks)}): {chunk}\n\nProvide a brief summary of this part of the document, focusing on key legal aspects.",
                    "ar": f"سياق الوثيقة (الجزء {i+1}/{len(chunks)}): {chunk}\n\nقدم ملخصًا موجزًا لهذا الجزء من الوثيقة، مع التركيز على الجوانب القانونية الرئيسية."
                }
                chunk_messages = messages + [{"role": "user", "content": context_prompt[language]}]
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=chunk_messages,
                    max_tokens=500,
                    temperature=0.7
                )
                summary = response.choices[0].message['content'].strip()
                summaries.append(summary)

            combined_summary = "\n\n".join(summaries)
            final_prompt = {
                "en": f"Based on the following document summaries, answer this question: {query}\n\nDocument summaries:\n{combined_summary}",
                "ar": f"بناءً على ملخصات الوثيقة التالية، أجب على هذا السؤال: {query}\n\nملخصات الوثيقة:\n{combined_summary}"
            }
            messages.append({"role": "user", "content": final_prompt[language]})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        full_response = response.choices[0].message['content'].strip()
        return full_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

@st.cache_data
def read_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

@st.cache_data
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates relevant questions based on legal documents."},
                {"role": "user", "content": prompt[language]}
            ],
            max_tokens=200
        )
        suggested_questions = response.choices[0].message['content'].strip().split('\n')
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

def process_queries(document_text, lang_code):
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("Enter your query:" if lang_code == "en" else "أدخل استفسارك:", 
                          key=f"query_{len(st.session_state.chat_history)}")
    
    if st.button("Submit" if lang_code == "en" else "إرسال", 
                 key=f"submit_{len(st.session_state.chat_history)}"):
        if query:
            with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                response = get_legal_advice(query, document_text, lang_code)
                st.markdown("### Response:")
                st.markdown(format_response(response))
                add_to_chat_history(query, response, lang_code)
                st.session_state.chat_history.append((query, response))
        else:
            st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")

    # Display chat history
    for q, r in st.session_state.chat_history:
        st.text(f"Q: {q}")
        st.text(f"A: {r}")
        st.text("---")

    if st.button("Clear Chat History" if lang_code == "en" else "مسح سجل المحادثة", 
                 key=f"clear_{len(st.session_state.chat_history)}"):
        st.session_state.chat_history = []
        st.experimental_rerun()

def main():
    init_db()
    
    language = st.sidebar.selectbox("Choose Language / اختر اللغة", ["English", "العربية"])
    lang_code = "en" if language == "English" else "ar"

    if lang_code == "ar":
        st.markdown('', unsafe_allow_html=True)

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
        uploaded_file = st.file_uploader("Upload a document" if lang_code == "en" else "قم بتحميل وثيقة", 
                                         type=["docx", "pdf", "txt"])
        if uploaded_file is not None:
            document_text = process_uploaded_file(uploaded_file)
            if document_text:
                st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")
                process_queries(document_text, lang_code)

    elif option == feature_options[lang_code][1]:  # Get Legal Advice
        process_queries(None, lang_code)

    elif option == feature_options[lang_code][2]:  # Oman Laws
        laws = get_oman_laws()
        if laws:
            selected_law = st.selectbox("Select a law:" if lang_code == "en" else "اختر قانونًا:", 
                                        list(laws.keys()))
            if selected_law:
                law_text = read_oman_law(laws[selected_law])
                if law_text:
                    process_queries(law_text, lang_code)
        else:
            st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

def process_uploaded_file(uploaded_file):
    file_type = uploaded_file.type
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(uploaded_file)
    elif file_type == "application/pdf":
        return read_pdf(uploaded_file)
    elif file_type == "text/plain":
        return read_txt(uploaded_file)
    else:
        st.error("Unsupported file type." if lang_code == "en" else "نوع الملف غير مدعوم.")
        return None

if __name__ == "__main__":
    main()
