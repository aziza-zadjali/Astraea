import streamlit as st
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law, add_to_chat_history

def main():
    language = st.sidebar.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
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
    option = st.selectbox(option_text[lang_code], feature_options[lang_code], key="feature_select")
    
    if option == feature_options[lang_code][0]:  # Query from Document
        upload_text = "Upload a document" if lang_code == "en" else "قم بتحميل وثيقة"
        uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="file_uploader")
        
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
            
            if document_text is None:
                st.error("Failed to read the document. Please try uploading it again or use a different file." if lang_code == "en" else "فشل في قراءة الوثيقة. يرجى محاولة تحميلها مرة أخرى أو استخدام ملف مختلف.")
            else:
                st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")
                
                suggested_questions = generate_suggested_questions(document_text, lang_code)
                if suggested_questions:
                    question_text = "Suggested questions:" if lang_code == "en" else "الأسئلة المقترحة:"
                    selected_question = st.selectbox(question_text, [""] + suggested_questions, key="suggested_questions")
                    
                    if selected_question:
                        query = selected_question
                        st.write(f"**Selected question:** {query}")
                        
                        with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                            try:
                                response = get_legal_advice(query, document_text, lang_code)
                                st.markdown("### Response:")
                                st.markdown(format_response(response))
                                add_to_chat_history(query, response, lang_code)
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                
                custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
                if st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query"):
                    if custom_query:
                        with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                            try:
                                response = get_legal_advice(custom_query, document_text, lang_code)
                                st.markdown("### Response:")
                                st.markdown(format_response(response))
                                add_to_chat_history(custom_query, response, lang_code)
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                    else:
                        st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
    
    elif option == feature_options[lang_code][1]:  # Get Legal Advice
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
        if st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query"):
            if query:
                with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                    try:
                        response = get_legal_advice(query, language=lang_code)
                        st.markdown("### Response:")
                        st.markdown(format_response(response))
                        add_to_chat_history(query, response, lang_code)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a query." if lang_code == "en" else "الرجاء إدخال استفسار.")
    
    elif option == feature_options[lang_code][2]:  # Oman Laws
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
                            with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                                try:
                                    response = get_legal_advice(query, law_text, lang_code)
                                    st.markdown("### Response:")
                                    st.markdown(format_response(response))
                                    add_to_chat_history(query, response, lang_code)
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")
                        
                        # Allow user to query again
                        while True:
                            query_text_again = "Enter your query about this law:" if lang_code == "en" else "أدخل استفسارك حول هذا القانون:"
                            query_again = st.text_input(query_text_again, key=f"oman_law_query_again_{len(st.session_state.chat_history)}")
                            if st.button("Submit" if lang_code == "en" else "إرسال", key=f"submit_oman_law_query_again_{len(st.session_state.chat_history)}"):
                                if query_again:
                                    with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
                                        try:
                                            response_again = get_legal_advice(query_again, law_text, lang_code)
                                            st.markdown("### Response:")
                                            st.markdown(format_response(response_again))
                                            add_to_chat_history(query_again, response_again, lang_code)
                                        except Exception as e:
                                            st.error(f"An error occurred: {str(e)}")
                else:
                    st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
        else:
            st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

if __name__ == "__main__":
    main()
