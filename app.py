
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
    .stTextInput>div>div>input {
        border: 1px solid #4CAF50 !important;
        border-radius: 5px;
        padding: 8px;
    }
    .stSelectbox>div>div>div {
        border: 1px solid #4CAF50 !important;
        border-radius: 5px;
        padding: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.image("logo.png", width=200)
        title = "Astraea - Legal Query Assistant"
        st.title(title)

        disclaimer = "This assistant uses GPT-3.5-turbo to provide general legal information. Please note that this is not a substitute for professional legal advice."
        st.info(disclaimer)

        # Language selection
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="main_language_select")
        lang_code = "en" if language == "English" else "ar"

        # Feature selection
        feature_options = ['Legal Query Assistant', 'Oman Laws', 'Legal Translation Service', 'Automated Document Creation', 'Grade Legal Document'] if lang_code == "en" else ['مساعد الاستفسارات القانونية', 'قوانين عمان', 'خدمة الترجمة القانونية', 'إنشاء المستندات الآلي', 'تقييم الوثيقة القانونية']
        selected_feature = st.selectbox("Select a feature" if lang_code == "en" else "اختر ميزة", feature_options, key="feature_select")

        # Display selected feature
        if selected_feature in ['Legal Query Assistant', 'مساعد الاستفسارات القانونية']:
            legal_query_assistant(lang_code)
        elif selected_feature in ['Oman Laws', 'قوانين عمان']:
            oman_laws_feature(lang_code)
        elif selected_feature in ['Legal Translation Service', 'خدمة الترجمة القانونية']:
            legal_translation_service(lang_code)
        elif selected_feature in ['Automated Document Creation', 'إنشاء المستندات الآلي']:
            automated_document_creation(lang_code)
        elif selected_feature in ['Grade Legal Document', 'تقييم الوثيقة القانونية']:
            grade_legal_document(lang_code)

    with col2:
        subscription_options(lang_code)

def subscription_options(lang_code):
    st.sidebar.title("Subscription Options" if lang_code == "en" else "خيارات الاشتراك")
    st.sidebar.markdown("---")

    plans = {
        "Basic": {"price": "$9.99/month", "features": ["Access to basic legal queries", "Limited document processing"]},
        "Pro": {"price": "$29.99/month", "features": ["Unlimited legal queries", "Advanced document analysis", "Priority support"]},
        "Enterprise": {"price": "Custom pricing", "features": ["All Pro features", "Customized solutions", "Dedicated account manager"]}
    }

    for plan, details in plans.items():
        st.sidebar.subheader(plan)
        st.sidebar.write(f"Price: {details['price']}")
        st.sidebar.write("Features:")
        for feature in details['features']:
            st.sidebar.write(f"- {feature}")
        if plan != "Enterprise":
            st.sidebar.button(f"Subscribe to {plan}" if lang_code == "en" else f"اشترك في {plan}", key=f"subscribe_{plan}")
        else:
            st.sidebar.button("Contact Sales" if lang_code == "en" else "تواصل مع المبيعات", key="contact_sales")
        st.sidebar.markdown("---")




    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"
        st.markdown("---")
        st.markdown("### Navigation")
        
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
                # Custom query section
                st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
                custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
                submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query")
                if custom_query and submit_custom:
                    process_query(custom_query, law_text, lang_code)
                
                st.markdown("---")
                
                # Suggested questions section
                st.subheader("Suggested Questions" if lang_code == "en" else "الأسئلة المقترحة")
                suggested_questions = generate_suggested_questions(law_text, lang_code)
                question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
                selected_question = st.selectbox(question_text, [""] + suggested_questions, key="selected_question")
                submit_suggested = st.button("Submit Suggested Question" if lang_code == "en" else "إرسال السؤال المقترح", key="submit_suggested_query")
                if selected_question and submit_suggested:
                    process_query(selected_question, law_text, lang_code)
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
    
    # Custom query section
    st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
    custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
    submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query")
    if custom_query and submit_custom:
        process_query(custom_query, document_text, lang_code)
    
    st.markdown("---")
    
    # Suggested questions section
    st.subheader("Suggested Questions" if lang_code == "en" else "الأسئلة المقترحة")
    question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
    selected_question = st.selectbox(question_text, [""] + suggested_questions, key="selected_question")
    submit_suggested = st.button("Submit Suggested Question" if lang_code == "en" else "إرسال السؤال المقترح", key="submit_suggested_query")
    if selected_question and submit_suggested:
        process_query(selected_question, document_text, lang_code)
        
def translate_to_arabic(text):
    translator = GoogleTranslator(source='auto', target='ar')
    translated = translator.translate(text)
    return translated

def extract_placeholders(template_content):
    return re.findall(r'\{(\w+)\}', template_content)

def fill_template(template_content, inputs):
    for placeholder, value in inputs.items():
        template_content = template_content.replace(f"{{{placeholder}}}", value)
    return template_content

def process_query(query, context=None, lang_code="en"):
    with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
        try:
            response = get_legal_advice(query, context, lang_code)
            st.markdown("### Response:")
            st.markdown(format_response(response))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def get_document_grade(document_text, lang_code):
    prompt = {
        "en": f"Grade the following legal document on a scale of 1-10 for clarity, completeness, and legal accuracy. Provide a brief explanation for each aspect:\n\n{document_text[:4000]}...",
        "ar": f"قيّم الوثيقة القانونية التالية على مقياس من 1 إلى 10 من حيث الوضوح والاكتمال والدقة القانونية. قدم شرحًا موجزًا لكل جانب:\n\n{document_text[:4000]}..."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are an expert legal document grader. Provide a detailed assessment of the given document."},
            {"role": "user", "content": prompt[lang_code]}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message['content'].strip()

def display_grade_result(grade_result, lang_code):
    st.subheader("Grading Result:" if lang_code == "en" else "نتيجة التقييم:")
    st.markdown(grade_result)

if __name__ == "__main__":
    main()
