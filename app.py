import streamlit as st
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law
from deep_translator import GoogleTranslator
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"
        st.markdown("---")
        st.markdown("### Navigation")
        option = st.radio(
            "Choose a feature" if lang_code == "en" else "اختر ميزة",
            ('Query from Document', 'Get Legal Advice', 'Oman Laws', 'Legal Translation Service'),
            key="feature_select"
        )

    # Main content
    title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
    st.title(title)
    disclaimer = {
        "en": "This assistant uses GPT-3.5-turbo to provide general legal information. Please note that this is not a substitute for professional legal advice.",
        "ar": "يستخدم هذا المساعد نموذج GPT-3.5-turbo لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
    }
    st.info(disclaimer[lang_code])

    if option == 'Query from Document':
        document_query_feature(lang_code)
    elif option == 'Get Legal Advice':
        legal_advice_feature(lang_code)
    elif option == 'Legal Translation Service':
        legal_translation_service(lang_code)
    else:
        oman_laws_feature(lang_code)

def document_query_feature(lang_code):
    st.header("Query from Document" if lang_code == "en" else "استعلام من وثيقة")
    upload_text = "Upload a document" if lang_code == "en" else "قم بتحميل وثيقة"
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="file_uploader")

    if uploaded_file:
        document_text = process_uploaded_file(uploaded_file, lang_code)
        if document_text:
            suggested_questions = generate_suggested_questions(document_text, lang_code)
            handle_document_queries(document_text, suggested_questions, lang_code)

def process_uploaded_file(uploaded_file, lang_code):
    file_type = uploaded_file.type
    spinner_text = "Reading document..." if lang_code == "en" else "جاري قراءة الوثيقة..."
    with st.spinner(spinner_text):
        if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return read_docx(uploaded_file)
        elif file_type == "application/pdf":
            return read_pdf(uploaded_file)
        elif file_type == "text/plain":
            return read_txt(uploaded_file)
        else:
            st.error("Unsupported file type." if lang_code == "en" else "نوع الملف غير مدعوم.")
            return None

def handle_document_queries(document_text, suggested_questions, lang_code):
    st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")
    custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
    st.markdown("**OR**" if lang_code == "en" else "**أو**")
    question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
    selected_question = st.selectbox(question_text, [""] + suggested_questions, key="selected_question")

    if selected_question:
        process_query(selected_question, document_text, lang_code)
    elif custom_query and st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query"):
        process_query(custom_query, document_text, lang_code)
    elif not custom_query and st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query"):
        st.warning("Please enter a query or select a suggested question." if lang_code == "en" else "الرجاء إدخال استفسار أو اختيار سؤال مقترح.")

def legal_advice_feature(lang_code):
    st.header("Get Legal Advice" if lang_code == "en" else "الحصول على استشارة قانونية")
    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
    if query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query"):
        logger.debug(f"Processing query: {query}")
        process_query(query, context=None, lang_code=lang_code)
    elif not query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query"):
        st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")

def oman_laws_feature(lang_code):
    st.header("Oman Laws" if lang_code == "en" else "قوانين عمان")
    laws = get_oman_laws()
    if laws:
        law_select_text = "Select a law:" if lang_code == "en" else "اختر قانونًا:"
        selected_law = st.selectbox(law_select_text, list(laws.keys()), key="select_law")
        if selected_law:
            law_text = read_oman_law(laws[selected_law])
            if law_text:
                query = st.text_input("Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:", key="oman_law_query")
                if query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_oman_law_query"):
                    process_query(query, law_text, lang_code)
                elif not query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_oman_law_query"):
                    st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
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
                translated_text = translate_to_arabic(document_text)
                st.text_area("Translated Text", translated_text, height=300)
                st.download_button(
                    label="Download Arabic Translation" if lang_code == 'en' else 'تحميل الترجمة العربية',
                    data=translated_text.encode('utf-8'),
                    file_name="arabic_translation.txt",
                    mime="text/plain"
                )

def translate_to_arabic(text):
    translator = GoogleTranslator(source='auto', target='ar')
    translated = translator.translate(text)
    return translated

def process_query(query, context=None, lang_code="en"):
    with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
        try:
            logger.debug(f"Calling get_legal_advice with query: {query}, lang_code: {lang_code}")
            response = get_legal_advice(query, context, lang_code)
            logger.debug(f"Response received: {response}")
            st.markdown("### Response:")
            st.markdown(format_response(response))
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
