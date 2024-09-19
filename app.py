import streamlit as st
import os
import re
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law
from deep_translator import GoogleTranslator
from fpdf import FPDF
import openai

# Assuming you have a directory for templates
TEMPLATE_DIR = "templates"

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Custom CSS for improved styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"
        st.markdown("---")
        st.markdown("### Navigation")
        
        # Replace radio buttons with a more visually appealing option
        options = ['Legal Query Assistant', 'Oman Laws', 'Legal Translation Service', 'Automated Document Creation', 'Grade Legal Document'] if lang_code == "en" else ['مساعد الاستفسارات القانونية', 'قوانين عمان', 'خدمة الترجمة القانونية', 'إنشاء المستندات الآلي', 'تقييم الوثيقة القانونية']
        icons = ['💬', '📚', '🔄', '📝', '✅']
        
        for i, opt in enumerate(options):
            if st.button(f"{icons[i]} {opt}", key=f"nav_{i}"):
                st.session_state.option = opt

    # Main content
    title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
    st.title(title)

    disclaimer = {
        "en": "This assistant uses GPT-3.5-turbo to provide general legal information. Please note that this is not a substitute for professional legal advice.",
        "ar": "يستخدم هذا المساعد نموذج GPT-3.5-turbo لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
    }
    st.info(disclaimer[lang_code])

    # Use tabs for main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(options)

    with tab1:
        legal_query_assistant(lang_code)
    with tab2:
        oman_laws_feature(lang_code)
    with tab3:
        legal_translation_service(lang_code)
    with tab4:
        automated_document_creation(lang_code)
    with tab5:
        grade_legal_document(lang_code)

def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")
    
    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    if query_type in ['Enter your own query', 'أدخل استفسارك الخاص']:
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
        col1, col2 = st.columns([1, 5])
        with col1:
            submit = st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query")
        with col2:
            clear = st.button("Clear" if lang_code == "en" else "مسح", key="clear_legal_query")
        
        if clear:
            st.session_state.legal_query = ""
        
        if query and submit:
            process_query(query, context=None, lang_code=lang_code)
    else:
        uploaded_file = st.file_uploader("Upload a document" if lang_code == "en" else "قم بتحميل وثيقة", type=["docx", "pdf", "txt"], key="file_uploader")
        if uploaded_file:
            document_text = process_uploaded_file(uploaded_file, lang_code)
            if document_text:
                suggested_questions = generate_suggested_questions(document_text, lang_code)
                handle_document_queries(document_text, suggested_questions, lang_code)

def oman_laws_feature(lang_code):
    st.header("Oman Laws" if lang_code == "en" else "قوانين عمان")
    laws = get_oman_laws()
    
    if laws:
        law_select_text = "Select a law:" if lang_code == "en" else "اختر قانونًا:"
        selected_law = st.selectbox(law_select_text, list(laws.keys()), key="select_law")
        
        if selected_law:
            law_text = read_oman_law(laws[selected_law])
            if law_text:
                st.markdown(f"### {selected_law}")
                st.text_area("Law Content", law_text, height=300)
                
                query = st.text_input("Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:", key="oman_law_query")
                if query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_oman_law_query"):
                    process_query(query, law_text, lang_code)
            else:
                st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
    else:
        st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

def legal_translation_service(lang_code):
    st.header("Legal Translation Service" if lang_code == 'en' else 'خدمة الترجمة القانونية')
    
    upload_text = 'Upload a document for translation to Arabic' if lang_code == 'en' else 'قم بتحميل وثيقة للترجمة إلى العربية'
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="translation_file_uploader")
    
    if uploaded_file:
        document_text = process_uploaded_file(uploaded_file, lang_code)
        if document_text:
            if st.button("Translate to Arabic" if lang_code == 'en' else 'ترجمة إلى العربية', key="translate_button"):
                with st.spinner("Translating..." if lang_code == 'en' else 'جاري الترجمة...'):
                    translated_text = translate_to_arabic(document_text)
                st.text_area("Translated Text", translated_text, height=300)
                st.download_button(
                    label="Download Arabic Translation" if lang_code == 'en' else 'تحميل الترجمة العربية',
                    data=translated_text.encode('utf-8'),
                    file_name="arabic_translation.txt",
                    mime="text/plain"
                )

def automated_document_creation(lang_code):
    st.header("Automated Document Creation" if lang_code == "en" else "إنشاء المستندات الآلي")
    
    templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
    selected_template = st.selectbox(
        "Select a template:" if lang_code == "en" else "اختر نموذجًا:",
        templates,
        key="template_select"
    )
    
    if selected_template:
        with open(os.path.join(TEMPLATE_DIR, selected_template), 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        placeholders = extract_placeholders(template_content)
        st.subheader("Fill in the details:" if lang_code == "en" else "املأ التفاصيل:")
        
        inputs = {}
        for i, placeholder in enumerate(placeholders):
            inputs[placeholder] = st.text_input(
                f"Enter {placeholder}:" if lang_code == "en" else f"أدخل {placeholder}:",
                key=f"input_{placeholder}_{i}"
            )
        
        if st.button("Generate Document" if lang_code == "en" else "إنشاء المستند", key="generate_doc_button"):
            filled_document = fill_template(template_content, inputs)
            st.text_area("Generated Document", filled_document, height=300, key="generated_doc_area")
            st.download_button(
                label="Download Document" if lang_code == "en" else "تحميل المستند",
                data=filled_document.encode('utf-8'),
                file_name=f"filled_{selected_template}",
                mime="text/plain",
                key="download_doc_button"
            )

def grade_legal_document(lang_code):
    st.header("Grade Legal Document" if lang_code == "en" else "تقييم الوثيقة القانونية")
    
    upload_text = "Upload a legal document to grade" if lang_code == "en" else "قم بتحميل وثيقة قانونية للتقييم"
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="grade_file_uploader")
    
    if uploaded_file:
        document_text = process_uploaded_file(uploaded_file, lang_code)
        if document_text:
            if st.button("Grade Document" if lang_code == "en" else "تقييم الوثيقة", key="grade_button"):
                with st.spinner("Grading document..." if lang_code == "en" else "جاري تقييم الوثيقة..."):
                    grade_result = get_document_grade(document_text, lang_code)
                display_grade_result(grade_result, lang_code)

# Helper functions (process_uploaded_file, translate_to_arabic, extract_placeholders, fill_template, get_document_grade, display_grade_result) remain the same

if __name__ == "__main__":
    main()
