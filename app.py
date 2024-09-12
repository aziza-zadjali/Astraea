import streamlit as st
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law, add_to_chat_history

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'law_queries' not in st.session_state:
        st.session_state.law_queries = []
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'suggested_questions' not in st.session_state:
        st.session_state.suggested_questions = []

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"
        st.markdown("---")
        st.markdown("### Navigation")
        option = st.radio(
            "Choose a feature" if lang_code == "en" else "اختر ميزة",
            ('Query from Document', 'Get Legal Advice', 'Oman Laws'),
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
    else:
        oman_laws_feature(lang_code)

    # Display chat history
    st.markdown("---")
    st.markdown("### Chat History")
    for item in st.session_state.chat_history:
        st.markdown(f"**You:** {item['query']}")
        st.markdown(f"**Astraea:** {item['response']}")
    st.markdown("---")

def document_query_feature(lang_code):
    st.header("Query from Document" if lang_code == "en" else "استعلام من وثيقة")
    upload_text = "Upload a document" if lang_code == "en" else "قم بتحميل وثيقة"
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="file_uploader")

    if uploaded_file:
        st.session_state.document_text = process_uploaded_file(uploaded_file, lang_code)
        if st.session_state.document_text:
            st.session_state.suggested_questions = generate_suggested_questions(st.session_state.document_text, lang_code)
            handle_document_queries(lang_code)

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

def handle_document_queries(lang_code):
    st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")

    if st.session_state.suggested_questions:
        question_text = "Suggested questions:" if lang_code == "en" else "الأسئلة المقترحة:"
        selected_question = st.selectbox(question_text, [""] + st.session_state.suggested_questions, key="suggested_questions")
        if selected_question:
            process_query(selected_question, st.session_state.document_text, lang_code)
            st.experimental_rerun()

    custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
    if st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query"):
        if custom_query:
            process_query(custom_query, st.session_state.document_text, lang_code)
        else:
            st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")

def legal_advice_feature(lang_code):
    st.header("Get Legal Advice" if lang_code == "en" else "الحصول على استشارة قانونية")
    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key=f"legal_query_{len(st.session_state.chat_history)}")
    if st.button("Submit" if lang_code == "en" else "إرسال", key=f"submit_legal_query_{len(st.session_state.chat_history)}"):
        if query:
            process_query(query, language=lang_code)
        else:
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
                query_text = "Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:"
                query = st.text_input(query_text, key="oman_law_query")
                if st.button("Submit" if lang_code == "en" else "إرسال", key="submit_oman_law_query"):
                    if query:
                        process_query(query, law_text, lang_code)
                    else:
                        st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
            else:
                st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
    else:
        st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

def process_query(query, context=None, lang_code="en"):
    with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
        try:
            response = get_legal_advice(query, context, lang_code)
            st.markdown("### Response:")
            st.markdown(format_response(response))
            add_to_chat_history(query, response, lang_code)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
