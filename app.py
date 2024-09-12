import streamlit as st
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Initialize session state
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0

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

    while True:
        if suggested_questions:
            question_text = "Suggested questions:" if lang_code == "en" else "الأسئلة المقترحة:"
            selected_question = st.selectbox(question_text, [""] + suggested_questions, key=f"suggested_questions_{st.session_state.query_count}")
            if selected_question:
                process_query(selected_question, document_text, lang_code)
                suggested_questions = generate_suggested_questions(document_text, lang_code)
                st.session_state.query_count += 1
                continue

        query = st.text_input("Enter your query:" if lang_code == "en" else "أدخل استفسارك:", key=f"document_query_{st.session_state.query_count}")
        if st.button("Submit Query" if lang_code == "en" else "إرسال الاستفسار", key=f"submit_document_query_{st.session_state.query_count}"):
            if query:
                process_query(query, document_text, lang_code)
                suggested_questions = generate_suggested_questions(document_text, lang_code)
                st.session_state.query_count += 1
            else:
                st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")

        if not ask_for_more_questions(lang_code):
            break

def ask_for_more_questions(lang_code):
    return st.button("Ask more questions" if lang_code == "en" else "اطرح المزيد من الأسئلة", key=f"ask_more_{st.session_state.query_count}")

def legal_advice_feature(lang_code):
    st.header("Get Legal Advice" if lang_code == "en" else "الحصول على استشارة قانونية")
    query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key=f"legal_query_{st.session_state.query_count}")
    if st.button("Submit" if lang_code == "en" else "إرسال", key=f"submit_legal_query_{st.session_state.query_count}"):
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
                query = st.text_input("Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:", key=f"oman_law_query_{st.session_state.query_count}")
                if st.button("Submit" if lang_code == "en" else "إرسال", key=f"submit_oman_law_query_{st.session_state.query_count}"):
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
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
