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
import requests
from bs4 import BeautifulSoup
from PIL import Image
st.title('Welcome to Astraea - Your AI Legal Assistant')


# Assuming you have a directory for templates
TEMPLATE_DIR = "templates"

def main():
    st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

    # Initialize session state for landing page
    if "show_main_app" not in st.session_state:
        st.session_state.show_main_app = False

    # Add custom CSS to hide the icons and style the button
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp [data-testid="stToolbar"] {visibility: hidden;}
        .stButton>button {
            background-color: #008080;
            color: white !important;
            border: none;
            padding: 10px 20px;
            font-size: 1.2em;
            border-radius: 5px;
            cursor: pointer;
            display: block;
            margin: 0 auto;
        }
        .stButton>button:hover { color: white !important;
            background-color: #006666;
        }
        .return-button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .logo-container {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
        }
        /* Hide the streamlit icon */
        .viewerBadge_Link__qRIco {
            display: none;
        }
        /* Testimonial Section */
        #testimonials {
            background-color: #fff;
            padding: 2em;
            margin: 2em auto;
            max-width: 800px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        #testimonials h2 {
            text-align: center;
            margin-bottom: 1em;
        }
        .testimonial {
            margin-bottom: 1em;
            padding: 1em;
            border-bottom: 1px solid #ddd;
        }
        .testimonial h3 {
            margin-top: 0.5em;
            font-size: 1.1em;
            color: #333;
        }
        </style>
    """
    
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Add logo to the top left corner using Streamlit's image function
    st.image("logo.png", width=100)

    # Load the image and resize it to make the length 50% shorter
    image = Image.open("poster.jpeg")
    width, height = image.size
    new_height = height // 3
    resized_image = image.resize((width, new_height))

    # Add the resized image at the top of the landing page
    st.image(resized_image, use_column_width=True)

    # Fixed position for language selection icon
    st.markdown(
        """
        <style>
        .language-selector {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Language selection icon with dropdown
    st.markdown(
        """
        <div class="language-selector">
            <select id="language-select" onchange="changeLanguage()">
                <option value="en">🇬🇧 English</option>
                <option value="ar">🇴🇲 Arabic</option>
            </select>
        </div>
        <script>
        function changeLanguage() {
            var select = document.getElementById("language-select");
            var selectedLanguage = select.options[select.selectedIndex].value;
            // Implement language change logic here
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.show_main_app:
        # Landing page
        st.markdown(
            """
            <div class="landing-page" style="text-align: center; padding: 50px 0;">
                <h1 style="color: #008080; font-size: 3em;">Welcome to Astraea</h1>
                <h2 style="color: #424242; font-size: 1.5em;">Your AI-Powered Legal Assistant</h2>
                <p style="font-size: 1.2em; max-width: 600px; margin: 20px auto; color: #424242;">
                    Astraea is here to simplify your legal queries. Get instant answers, 
                    explore Omani laws, and receive personalized legal advice.
                </p>
            """,
            unsafe_allow_html=True
        )

        if st.button("Get Started", key="get_started_button"):
            st.session_state.show_main_app = True


        # Add testimonial section
        st.markdown(
            """
            <section id="testimonials">
                <h2>What Our Clients Say</h2>
                <div class="testimonial">
                    <p>"خانة الاستفسار تعمل بشكل جيد. إن إنشاء المستندات الآلي ومراجعة الوثائق يوفران الكثير من الوقت ويزيدان من الإنتاجية والدقة بشكل ملحوظ."</p>
                    <h3>- مكتب محمد الشقصي للمحاماة والاستشارات القانونية</h3>
                </div>
                <div class="testimonial">
                    <p>"The inquiry section works very well. Automated document creation and document review are significant time-savers that noticeably increase productivity and accuracy."</p>
                    <h3>- MOHD AL-SHAQSI ADV AND LEGAL CONSULTANTS</h3>
                </div>
            </section>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.show_main_app:
        # Main app (initially hidden)
        st.markdown(
            """
            <style>
            .landing-page {display: none;}
            </style>
            """,
            unsafe_allow_html=True
        )

        # Move the "Return to Landing Page" button to the top center using Streamlit built-in button
        return_button_col = st.columns([1, 2, 1])[1]
        with return_button_col:
            if st.button("Return to Landing Page", key="return_button"):
                st.session_state.show_main_app = False

        # Main content with tabs
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select", label_visibility="collapsed")
        lang_code = "en" if language == "English" else "ar"

        # Inject custom CSS for RTL layout, font sizes, and tab styling
        st.markdown(
            f"""
            <style>
            html, body, [class*="css"] {{
                font-size: 16px;
                direction: {"rtl" if lang_code == "ar" else "ltr"};
            }}
            h1 {{
                font-size: 2rem;
            }}
            h2 {{
                font-size: 1.5rem;
            }}
            h3 {{
                font-size: 1.17rem;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
            }}
            .stTabs [data-baseweb="tab"] {{
                height: auto;
                white-space: pre-wrap;
                background-color: #F0F2F6;
                border-radius: 4px 4px 0 0;
                gap: 1rem;
                padding: 10px 20px;
                font-size: 1rem;
            }}
            .stTabs [data-baseweb="tab"]:hover {{
                background-color: #008080;
                color: white;
            }}
            .stTabs [data-baseweb="tab"][aria-selected="true"] {{
                background-color: #008080;
                color: white;
            }}
            .stTabs [data-baseweb="tab-list"] button:focus {{
                box-shadow: none;
            }}
            .stTabs [data-baseweb="tab-highlight"] {{
                background-color: transparent;
            }}
            .stTabs [data-baseweb="tab-border"] {{
                display: none;
            }}
            .stTextArea>div>div>textarea {{
                font-size: 1rem;
            }}
            .stSelectbox>div>div>div {{
                font-size: 1rem;
            }}
            .stRadio [role="radiogroup"] {{
                flex-direction: column; /* Align vertically */
                align-items: flex-start; /* Align to the left */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        title = "Astraea - Legal Query Assistant" if lang_code == "en" else "أسترايا - مساعد الاستفسارات القانونية"
        st.title(title)

        disclaimer = {
            "en": "This assistant uses GPT-4.0 to provide general legal information. Please note that this is not a substitute for professional legal advice.",
            "ar": "يستخدم هذا المساعد نموذج GPT-4.0 لتقديم معلومات قانونية عامة. يرجى ملاحظة أن هذا ليس بديلاً عن المشورة القانونية المهنية."
        }
        st.info(disclaimer[lang_code])

        # Define tab labels in both languages
        tab_labels = {
            "en": ["Legal Query Assistant", "Oman Laws", "Legal Translation Service", "Automated Document Creation", "Grade Legal Document", "Predictive Case Analysis"],
            "ar": ["مساعد الاستفسارات القانونية", "قوانين عمان", "خدمة الترجمة القانونية", "إنشاء المستندات الآلي", "تقييم الوثيقة القانونية", "التحليل التنبؤي للقضايا"]
        }

        # Create tabs using the appropriate language
        tabs = st.tabs(tab_labels[lang_code])

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

    # Move the query type selection to the top and align vertically
    query_type = st.radio(
        "Choose query type" if lang_code == "en" else "اختر نوع الاستفسار",
        ('Enter your own query', 'Query from document') if lang_code == "en" else ('أدخل استفسارك الخاص', 'استفسر من وثيقة'),
        key="query_type"
    )

    # Add a radio button for selecting the summary type
    summary_type = st.radio(
        "Please confirm the response type" if lang_code == "en" else "يرجى تأكيد نوع الملخص",
        ("Brief", "Detailed", "Comprehensive") if lang_code == "en" else ("موجز", "مفصل", "شامل"),
        key="summary_type"
    )

    if query_type in ['Enter your own query', 'أدخل استفسارك الخاص']:
        query = st.text_input("Enter your legal query:" if lang_code == "en" else "أدخل استفسارك القانوني:", key="legal_query")
        if query and st.button("Submit" if lang_code == "en" else "إرسال", key="submit_legal_query"):
            process_query(query, summary_type, context=None, lang_code=lang_code)
    else:
        uploaded_file = st.file_uploader("Upload a document" if lang_code == "en" else "قم بتحميل وثيقة", type=["docx", "pdf", "txt"], key="file_uploader")
        if uploaded_file:
            document_text = process_uploaded_file(uploaded_file, lang_code)
            if document_text:
                suggested_questions = generate_suggested_questions(document_text, lang_code)
                handle_document_queries(document_text, suggested_questions, summary_type, lang_code)

def fetch_information_from_websites(query):
    urls = ["https://qanoon.om/", "https://www.oman.om"]
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Implement specific logic to search for the query in the website's content
                # This is a placeholder for demonstration purposes
                if query.lower() in soup.text.lower():
                    return f"Information found on {url}: {query}"
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return None

def process_query(query, summary_type, context=None, lang_code="en"):
    with st.spinner("Processing..." if lang_code == "en" else "جاري المعالجة..."):
        try:
            # First, try to fetch information from the specified websites
            web_info = fetch_information_from_websites(query)
            if web_info:
                st.markdown("### Response:")
                st.markdown(format_response(web_info))
                return

            # If no information is found on the websites, proceed with the usual processing
            context_chunks = split_text_into_chunks(context, max_tokens=2000) if context else ["No additional context provided."]
            
            responses = []
            for chunk in context_chunks:
                prompt = {
                    "en": f"Provide a {summary_type.lower()} summary of the following legal query. Avoid ambiguity and ensure the response is certain:\n\nQuery: {query}\n\nContext: {chunk}",
                    "ar": f"قدم ملخصًا {summary_type.lower()} للاستفسار القانوني التالي. تجنب الغموض وتأكد من أن الإجابة مؤكدة:\n\nالاستفسار: {query}\n\nالسياق: {chunk}"
                }
                
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are Astraea, which is a greece word for justice, you are an expert legal advisor. Provide a clear, direct, and certain answer to the given query, including guidance and relevant legal precedents, statutes, or case law to support the analysis. If there are specific legal risks or potential issues, please flag them and suggest mitigating strategies."},
                        {"role": "user", "content": prompt[lang_code]}
                    ],
                    max_tokens=150 if summary_type == "Brief" else 300 if summary_type == "Detailed" else 600,
                    temperature=0.7
                )
                
                responses.append(response.choices[0].message['content'].strip())
            
            # Combine the responses from all chunks
            final_response = "\n\n".join(responses)
            st.markdown("### Response:")
            st.markdown(format_response(final_response))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def handle_document_queries(document_text, suggested_questions, summary_type, lang_code):
    st.success("Document uploaded successfully!" if lang_code == "en" else "تم تحميل الوثيقة بنجاح!")

    # Suggested questions section
    st.subheader("Suggested Questions" if lang_code == "en" else "الأسئلة المقترحة")
    question_text = "Select a suggested question:" if lang_code == "en" else "اختر سؤالاً مقترحًا:"
    selected_question = st.selectbox(question_text, [""] + suggested_questions, key="selected_question")
    submit_suggested = st.button("Submit Suggested Question" if lang_code == "en" else "إرسال السؤال المقترح", key="submit_suggested_query")

    if selected_question and submit_suggested:
        process_query(selected_question, summary_type, document_text, lang_code)

    st.markdown("---")

    # Custom query section
    st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
    custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="custom_query")
    submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_custom_query")

    if custom_query and submit_custom:
        process_query(custom_query, summary_type, document_text, lang_code)

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
                    concise_answer = get_concise_law_answer(selected_question, law_text, summary_type, lang_code)
                    st.markdown("### Answer:")
                    st.markdown(concise_answer)

                st.markdown("---")  # Separator for custom query section
                
                # Custom query section
                st.subheader("Custom Query" if lang_code == "en" else "استفسار مخصص")
                custom_query = st.text_input("Enter your custom query:" if lang_code == "en" else "أدخل استفسارك الخاص:", key="oman_law_custom_query")
                submit_custom = st.button("Submit Custom Query" if lang_code == "en" else "إرسال الاستفسار الخاص", key="submit_oman_law_custom_query")
                
                if custom_query and submit_custom:
                    concise_answer = get_concise_law_answer(custom_query, law_text, summary_type, lang_code)
                    st.markdown("### Answer:")
                    st.markdown(concise_answer)
            else:
                st.error("Failed to read the selected law. Please try again or choose a different law." if lang_code == "en" else "فشل في قراءة القانون المحدد. يرجى المحاولة مرة أخرى أو اختيار قانون آخر.")
    else:
        st.error("No laws found in the database directory." if lang_code == "en" else "لم يتم العثور على قوانين في دليل قاعدة البيانات.")

def get_concise_law_answer(query, law_text, summary_type, lang_code):
    prompt = {
        "en": f"Provide a {summary_type.lower()} summary of the following query about Oman law. Focus on the most relevant information and limit the response to 2-3 sentences:\n\nQuery: {query}\n\nLaw text: {law_text[:3000]}...",
        "ar": f"قدم ملخصًا {summary_type.lower()} للاستفسار التالي حول قانون عمان. ركز على المعلومات الأكثر صلة وحدد الإجابة في 2-3 جمل:\n\nالاستفسار: {query}\n\nنص القانون: {law_text[:3000]}..."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a concise legal advisor specializing in Oman law."},
            {"role": "user", "content": prompt[lang_code]}
        ],
        max_tokens=150 if summary_type == "Brief" else 300 if summary_type == "Detailed" else 600,
        temperature=0.7
    )
    
    return response.choices[0].message['content'].strip()

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

def grade_legal_document(lang_code):
    st.header("Grade Legal Document" if lang_code == "en" else "تقييم الوثيقة القانونية")
    
    upload_text = "Upload a legal document to grade" if lang_code == "en" else "قم بتحميل وثيقة قانونية للتقييم"
    uploaded_file = st.file_uploader(upload_text, type=["docx", "pdf", "txt"], key="grade_file_uploader")
    
    if uploaded_file:
        document_text = process_uploaded_file(uploaded_file, lang_code)
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

    Astraea will provide a predictive analysis, outlining potential outcomes, strengths and weaknesses of the case, and relevant Oman case law.
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
