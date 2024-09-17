import streamlit as st
import os
import re
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law
from deep_translator import GoogleTranslator
from fpdf import FPDF

def legal_essay_feedback(lang_code):
    st.header("Legal Essay Feedback" if lang_code == "en" else "تقييم المقال القانوني")
    
    essay_text = st.text_area("Enter your legal essay:" if lang_code == "en" else "أدخل مقالك القانوني:", height=300)
    
    if st.button("Get Feedback" if lang_code == "en" else "الحصول على التقييم"):
        if essay_text:
            feedback = get_essay_feedback(essay_text, lang_code)
            display_feedback(feedback, lang_code)
        else:
            st.warning("Please enter an essay." if lang_code == "en" else "الرجاء إدخال مقال.")

def get_essay_feedback(essay_text, lang_code):
    prompt = {
        "en": "You will be provided with a law student's essay. Please give them feedback and a grade. Use this format for feedback:\n\nGrade: [Your grade, like A, B, or C]\nStrengths: [Highlight what they did really well, such as how they structured their paragraph, used Critical Thinking, Originality and Plagiarism, and Proper Grammar and Style]\nAreas for Improvement: [Tell them where you think they can make it even better]\n\nEssay:\n",
        "ar": "سيتم تزويدك بمقال لطالب قانون. يرجى إعطاؤهم ملاحظات ودرجة. استخدم هذا التنسيق للملاحظات:\n\nالدرجة: [درجتك، مثل A أو B أو C]\nنقاط القوة: [سلط الضوء على ما قاموا به بشكل جيد للغاية، مثل كيفية هيكلة الفقرة، واستخدام التفكير النقدي، والأصالة وعدم الانتحال، والقواعد النحوية والأسلوب المناسب]\nمجالات التحسين: [أخبرهم أين تعتقد أنه يمكنهم جعله أفضل]\n\nالمقال:\n"
    }
    
    messages = [
        {"role": "system", "content": prompt[lang_code]},
        {"role": "user", "content": essay_text}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error generating feedback: {str(e)}"

def display_feedback(feedback, lang_code):
    lines = feedback.split('\n')
    grade = ""
    strengths = ""
    areas_for_improvement = ""
    current_section = None
    
    for line in lines:
        if line.startswith("Grade:") or line.startswith("الدرجة:"):
            current_section = "Grade"
            grade += line + '\n'
        elif line.startswith("Strengths:") or line.startswith("نقاط القوة:"):
            current_section = "Strengths"
            strengths += line + '\n'
        elif line.startswith("Areas for Improvement:") or line.startswith("مجالات التحسين:"):
            current_section = "Areas for Improvement"
            areas_for_improvement += line + '\n'
        else:
            if current_section == "Grade":
                grade += line + '\n'
            elif current_section == "Strengths":
                strengths += line + '\n'
            elif current_section == "Areas for Improvement":
                areas_for_improvement += line + '\n'
    
    st.subheader("Feedback:" if lang_code == "en" else "التقييم:")
    st.markdown(grade)
    st.markdown(strengths)
    st.markdown(areas_for_improvement)


TEMPLATE_DIR = "templates"

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
            ('Legal Query Assistant', 'Oman Laws', 'Legal Translation Service', 'Automated Document Creation') if lang_code == "en" else 
            ('مساعد الاستفسارات القانونية', 'قوانين عمان', 'خدمة الترجمة القانونية', 'إنشاء المستندات الآلي'),
            key="feature_select"
        )
        elif option in ['Legal Essay Feedback', 'تقييم المقال القانوني']:
        legal_essay_feedback(lang_code)

    
    # Main content
    title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
    st.title(title)
    disclaimer = {
        "en": "This assistant uses GPT-3.5-turbo to provide general legal information. Please note that this is not a substitute for professional legal advice.",
        "ar": "يستخدم هذا المساعد نموذج GPT-3.5-turbo لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
    }
    st.info(disclaimer[lang_code])

    if option in ['Legal Query Assistant', 'مساعد الاستفسارات القانونية']:
        legal_query_assistant(lang_code)
    elif option in ['Oman Laws', 'قوانين عمان']:
        oman_laws_feature(lang_code)
    elif option in ['Legal Translation Service', 'خدمة الترجمة القانونية']:
        legal_translation_service(lang_code)
    elif option in ['Automated Document Creation', 'إنشاء المستندات الآلي']:
        automated_document_creation(lang_code)

def legal_query_assistant(lang_code):
    st.header("Legal Query Assistant" if lang_code == "en" else "مساعد الاستفسارات القانونية")
    
    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    if query_type in ['Enter your own query', 'أدخل استفسارك الخاص']:
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
        if query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query"):
            process_query(query, context=None, lang_code=lang_code)
    else:
        uploaded_file = st.file_uploader("Upload a document" if lang_code == "en" else "قم بتحميل وثيقة", type=["docx", "pdf", "txt"], key="file_uploader")
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

def automated_document_creation(lang_code):
    st.header("Automated Document Creation" if lang_code == "en" else "إنشاء المستندات الآلي")
    
    # Get list of available templates
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

def extract_placeholders(template_content):
    import re
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

if __name__ == "__main__":
    main()
