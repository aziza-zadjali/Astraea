import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import streamlit as st
import os
import re
from typing import Dict, Any
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law
from deep_translator import GoogleTranslator
from fpdf import FPDF
import openai

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Assuming you have a directory for templates
TEMPLATE_DIR = "templates"

def save_uploaded_file(uploaded_file):
    try:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No such file: '{pdf_path}'")
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img, lang='ara')

    return text

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Sidebar for language selection
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"

    # Inject custom CSS for RTL layout if Arabic is selected
    if lang_code == "ar":
        st.markdown(
            """
            <style>
            body {
                direction: rtl;
                text-align: right;
            }
            .css-1d391kg { /* Sidebar */
                direction: rtl;
                text-align: right;
            }
            .css-1v3fvcr { /* Main content */
                direction: rtl;
                text-align: right;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Main content with tabs
    title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
    st.title(title)

    disclaimer = {
        "en": "This assistant uses GPT-4.0 to provide general legal information. Please note that this is not a substitute for professional legal advice.",
        "ar": "يستخدم هذا المساعد نموذج GPT-4.0 لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
    }
    st.info(disclaimer[lang_code])

    tabs = st.tabs(["Legal Query Assistant", "Oman Laws", "Legal Translation Service", "Automated Document Creation", "Grade Legal Document", "Predictive Case Analysis"])

    with tabs[0]:
        legal_query_assistant(lang_code)
    with tabs[1]:
        oman_laws_feature(lang_code)
    with tabs[2]:
        legal_translation_service(lang_code)
    with tabs[3]:
        automated_document_creation(lang_code)
    with tabs[4]:
        grade_legal_document(lang_code)
    with tabs[5]:
        predictive_analysis_ui()

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
            saved_file_path = save_uploaded_file(uploaded_file)
            if saved_file_path:
                document_text = process_uploaded_file(saved_file_path, lang_code)
                if document_text:
                    suggested_questions = generate_suggested_questions(document_text, lang_code)
                    handle_document_queries(document_text, suggested_questions, lang_code)

def process_uploaded_file(file_path, lang_code):
    file_type = file_path.split('.')[-1]
    spinner_text = "Reading document..." if lang_code == "en" else "جاري قراءة الوثيقة..."
    with st.spinner(spinner_text):
        if file_type == "docx":
            return read_docx(file_path)
        elif file_type == "pdf":
            return extract_text_from_pdf(file_path)  # Use the new function for PDF handling
        elif file_type == "txt":
            return read_txt(file_path)
        else:
            st.error("Unsupported file type." if lang_code == "en" else "نوع الملف غير مدعوم.")
            return None

def handle_document_queries(document_text, suggested_questions, lang_code):
    st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")
    
    # Suggested questions section
    st.subheader("Suggested Questions" if lang_code == "en" else "الأسئلة المقترحة")
    question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
    selected_question = st.selectbox(question_text, [""] + suggested_questions, key="selected_question")
    submit_suggested = st.button("Submit Suggested Question" if lang_code == "en" else "إرسال السؤال المقترح", key="submit_suggested_query")
    
    if selected_question and submit_suggested:
        process_query(selected_question, document_text, lang_code)
    
    st.markdown("---")
    
    # Custom query section
    st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
    custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
    submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query")
    
    if custom_query and submit_custom:
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
                st.success("Law loaded successfully!" if lang_code == "en" else "تم تحميل القانون بنجاح!")
                
                # Suggested questions section
                st.subheader("Suggested Questions" if lang_code == "en" else "الأسئلة المقترحة")
                suggested_questions = generate_suggested_questions(law_text, lang_code)
                question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
                selected_question = st.selectbox(question_text, [""] + suggested_questions, key="oman_law_selected_question")
                submit_suggested = st.button("Submit Suggested Question" if lang_code == "en" else "إرسال السؤال المقترح", key="submit_oman_law_suggested_query")
                
                if selected_question and submit_suggested:
                    process_query(selected_question, law_text, lang_code)
                
                st.markdown("---")
                
                # Custom query section
                st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
                custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="oman_law_custom_query")
                submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_oman_law_custom_query")
                
                if custom_query and submit_custom:
                    process_query(custom_query, law_text, lang_code)
            else:
                st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
    else:
        st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

def legal_translation_service(lang_code):
    st.header("Legal Translation Service" if lang_code == 'en' else 'خدمة الترجمة القانونية')
    upload_text = 'Upload a document for translation to Arabic' if lang_code == 'en' else 'قم بتحميل وثيقة للترجمة إلى العربية'
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="translation_file_uploader")
    
    if uploaded_file:
        saved_file_path = save_uploaded_file(uploaded_file)
        if saved_file_path:
            document_text = process_uploaded_file(saved_file_path, lang_code)
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
            # Split the context into smaller chunks if it exceeds the token limit
            context_chunks = split_text_into_chunks(context, max_tokens=3000) if context else ["No additional context provided."]
            
            responses = []
            for chunk in context_chunks:
                prompt = {
                    "en": f"Provide a clear and direct answer to the following legal query. Avoid ambiguity and ensure the response is certain:\n\nQuery: {query}\n\nContext: {chunk}",
                    "ar": f"قدم إجابة واضحة ومباشرة للاستفسار القانوني التالي. تجنب الغموض وتأكد من أن الإجابة مؤكدة:\n\nالاستفسار: {query}\n\nالسياق: {chunk}"
                }
                
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert legal advisor. Provide a clear, direct, and certain answer to the given query."},
                        {"role": "user", "content": prompt[lang_code]}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                responses.append(response.choices[0].message['content'].strip())
            
            # Combine the responses from all chunks
            final_response = "\n\n".join(responses)
            st.markdown("### Response:")
            st.markdown(format_response(final_response))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def split_text_into_chunks(text, max_tokens=3000):
    # Split the text into chunks of max_tokens length
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1  # +1 for the space
        if current_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def grade_legal_document(lang_code):
    st.header("Grade Legal Document" if lang_code == "en" else "تقييم الوثيقة القانونية")
    
    upload_text = "Upload a legal document to grade" if lang_code == "en" else "قم بتحميل وثيقة قانونية للتقييم"
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="grade_file_uploader")
    
    if uploaded_file:
        saved_file_path = save_uploaded_file(uploaded_file)
        if saved_file_path:
            document_text = process_uploaded_file(saved_file_path, lang_code)
            if document_text:
                if st.button("Grade Document" if lang_code == "en" else "تقييم الوثيقة", key="grade_button"):
                    grade_result = get_document_grade(document_text, lang_code)
                    display_grade_result(grade_result, lang_code)

def get_document_grade(document_text, lang_code):
    prompt = {
        "en": f"Grade the following legal document on a scale of 1-10 for clarity, completeness, and legal accuracy. Provide a brief explanation for each aspect:\n\n{document_text[:4000]}...",
        "ar": f"قيّم الوثيقة القانونية التالية على مقياس من 1 إلى 10 من حيث الوضوح والاكتمال والدقة القانونية. قدم شرحًا موجزًا لكل جانب:\n\n{document_text[:4000]}..."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
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

def analyze_case_for_prediction(case_details: str) -> Dict[str, Any]:
    chunks = split_text_into_chunks(case_details)
    full_analysis = ""

    for i, chunk in enumerate(chunks):
        analysis_prompt = f"""
        Analyze the following case details (part {i+1}/{len(chunks)}) in the context of the Oman legal system and provide a predictive analysis.

        Case Details (Part {i+1}/{len(chunks)}):
        ```
        {chunk}
        ```

        Your analysis should address the following:
        * **Case Summary:** Briefly summarize the key facts, legal claims, and parties involved in the case.
        * **Predicted Outcome:** What is the most likely outcome of this case based on the provided information, Oman legal precedents, and similar cases? Explain your reasoning.
        * **Strengths of the Case:** Identify the most compelling arguments and evidence that support a favorable outcome.
        * **Weaknesses of the Case:** What are potential weaknesses in the case, or areas where the opposing party might have strong arguments?
        * **Areas of Caution:** What potential pitfalls or challenges should be considered? What strategies could the opposing party use?
        * **Relevant Oman Case Law:** Cite specific Oman legal precedents and similar cases that support your analysis and predicted outcome.
        * **Recommended Strategies:** Offer specific, actionable recommendations on how to strengthen the case and increase the likelihood of a positive result.

        Please maintain a neutral and objective tone throughout your analysis. The goal is to provide a realistic assessment of the case, not to advocate for a particular side.
        """

        try:
            chunk_analysis = get_ai_response(analysis_prompt)
            full_analysis += chunk_analysis + "\n\n"

        except Exception as e:
            return {"error": f"Error analyzing case (part {i+1}): {str(e)}"}

    return {"analysis": full_analysis}

def get_ai_response(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert legal analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

def extract_text_from_document(uploaded_file) -> str:
    file_type = uploaded_file.type
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(uploaded_file)
    elif file_type == "application/pdf":
        return read_pdf(uploaded_file)
    elif file_type == "text/plain":
        return read_txt(uploaded_file)
    else:
        st.error("Unsupported file type.")
        return ""

def predictive_analysis_ui():
    st.subheader("Predictive Case Analysis")
    st.write('''
    Enter the details of your case, including:

    * Facts: Briefly describe the key events that led to the legal dispute.
    * Legal Issues: State the specific legal questions or claims in the case.
    * Relevant Law: Identify any relevant Oman laws, statutes, or regulations.
    * Jurisdiction: Specify the Oman city where the case is filed.

    LexAI will provide a predictive analysis, outlining potential outcomes, strengths and weaknesses of the case, and relevant Oman case law.
    ''')

    st.warning("Please do not upload files larger than 5MB as it may cause issues and consume all available tokens.")

    input_method = st.radio("Choose input method:", ("Text Input", "Document Upload"))
    
    case_details = ""
    if input_method == "Text Input":
        case_details = st.text_area("Enter case details:", height=200)
    else:
        uploaded_file = st.file_uploader("Upload a document containing case details (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            case_details = extract_text_from_document(uploaded_file)

    if st.button("Analyze Case"):
        if case_details:
            with st.spinner("Analyzing your case..."):
                analysis_results = analyze_case_for_prediction(case_details)

            st.write("### Case Analysis")
            if "error" in analysis_results:
                st.error(analysis_results["error"])
            else:
                analysis = analysis_results.get("analysis", "No analysis available.")
                st.write(analysis)

                # Download button for analysis
                st.download_button(
                    label="Download Analysis",
                    data=analysis,
                    file_name="case_analysis.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter case details or upload a document to analyze.")

if __name__ == "__main__":
    main()
