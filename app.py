import streamlit as st
import openai
from docx import Document
import fitz  # PyMuPDF
from pyarabic.araby import strip_tashkeel, normalize_hamza
import arabic_reshaper
from bidi.algorithm import get_display
import re
import os

# Set page config at the very beginning
st.set_page_config(page_title="Astraea - Legal Query Assistant", page_icon="⚖️", layout="wide")

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the path to your database directory
DATABASE_DIR = "database"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

@st.cache_data(ttl=3600)
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
            messages.append({"role": "user", "content": f"Document context: {document_text[:4000]}..."})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
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

@st.cache_data
def get_oman_laws():
    laws = {}
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(".pdf"):
            law_name = filename[:-4]  # Remove .pdf extension
            laws[law_name] = os.path.join(DATABASE_DIR, filename)
    return laws

def main():
    language = st.sidebar.selectbox("Choose Language / اختر اللغة", ["English", "العربية"])
    lang_code = "en" if language == "English" else "ar"
    
    if lang_code == "ar":
        st.markdown('<style>.css-18e3th9 { direction: rtl; } .css-1d391kg { direction: rtl; }</style>', unsafe_allow_html=True)
    
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
        upload_text = "Upload a document" if lang_code == "en" else "قم بتحميل وثيقة"
        uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"])
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            spinner_text = "Reading document..." if lang_code == "en" else "جاري قراءة الوثيقة..."
            
            with st.spinner(spinner_text):
                if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    document_text = read_docx(uploaded_file)
                elif file_type == "application/pdf":
                    document_text = read_pdf(uploaded_file)
                elif file_type == "text/plain":
                    document_text = read_txt(uploaded_file)
                else:
                    document_text = None
                    st.error("Unsupported file type." if lang_code == "en" else "نوع الملف غير مدعوم.")
            
            if document_text:
                st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")
                
                query = st.text_input("Enter your query:" if lang_code == "en" else "أدخل استفسارك:")
                if st.button("Submit" if lang_code == "en" else "إرسال"):
                    if query:
                        with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                            response = get_legal_advice(query, document_text, lang_code)
                            st.markdown("### Response:")
                            st.markdown(response)
                            st.session_state.chat_history.append((query, response))
                    else:
                        st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
            else:
                st.error("Failed to read the document. Please try uploading it again or use a different file." if lang_code == "en" else "فشل في قراءة الوثيقة. يرجى محاولة تحميلها مرة أخرى أو استخدام ملف مختلف.")
    
    elif option == feature_options[lang_code][1]:  # Get Legal Advice
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:")
        if st.button("Submit" if lang_code == "en" else "إرسال"):
            if query:
                with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                    response = get_legal_advice(query, language=lang_code)
                    st.markdown("### Response:")
                    st.markdown(response)
                    st.session_state.chat_history.append((query, response))
            else:
                st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
    
    elif option == feature_options[lang_code][2]:  # Oman Laws
        laws = get_oman_laws()
        if laws:
            law_select_text = "Select a law:" if lang_code == "en" else "اختر قانونًا:"
            selected_law = st.selectbox(law_select_text, list(laws.keys()))
            
            if selected_law:
                law_text = read_pdf(laws[selected_law])
                if law_text:
                    query_text = "Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:"
                    query = st.text_input(query_text)
                    if st.button("Submit" if lang_code == "en" else "إرسال"):
                        if query:
                            with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                                response = get_legal_advice(query, law_text, lang_code)
                                st.markdown("### Response:")
                                st.markdown(response)
                                st.session_state.chat_history.append((query, response))
                        else:
                            st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
                else:
                    st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
        else:
            st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")
    
    # Display chat history
    st.sidebar.markdown("### Chat History")
    for query, response in st.session_state.chat_history:
        st.sidebar.text_area("Query:", value=query, height=100, disabled=True)
        st.sidebar.text_area("Response:", value=response, height=200, disabled=True)
        st.sidebar.markdown("---")

if __name__ == "__main__":
    main()
