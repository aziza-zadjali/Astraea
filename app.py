import streamlit as st
import openai
from docx import Document
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_legal_advice(query, document_text=None):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful legal assistant Astraea which has all the legal information in the world and is the best assistant for lawyers, law firms, and a common citizen. Provide general legal information and advice, but remind the user to consult with a qualified attorney for specific legal issues."},
            {"role": "user", "content": query}
        ]
        if document_text:
            messages.append({"role": "user", "content": f"Here is the content of the uploaded document: {document_text}"})
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    full_text = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text.append(page.get_text())
    return '\n'.join(full_text)

def read_txt(file):
    return file.read().decode("utf-8")

st.title("Astraea - Legal Query Assistant")

st.write("This assistant uses GPT-4 to provide general legal information. Please note that this is not a substitute for professional legal advice.")

# Dropdown menu for selecting features
option = st.selectbox(
    'Choose a feature',
    ('Query from Document', 'Get Legal Advice')
)

if option == 'Query from Document':
    uploaded_file = st.file_uploader("Upload a document", type=["docx", "pdf", "txt"])

    document_text = None
    if uploaded_file is not None:
        file_type = uploaded_file.type
        with st.spinner("Reading document..."):
            if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                document_text = read_docx(uploaded_file)
            elif file_type == "application/pdf":
                document_text = read_pdf(uploaded_file)
            elif file_type == "text/plain":
                document_text = read_txt(uploaded_file)
            else:
                document_text = "Unsupported file type."

    if document_text:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        user_query = st.text_area("Enter your query:", height=100)

        if st.button("Query Document"):
            if user_query:
                with st.spinner("Analyzing your query..."):
                    response = get_legal_advice(user_query, document_text)
                    st.session_state.chat_history.append({"query": user_query, "response": response})
                    user_query = ""

        if st.session_state.chat_history:
            for i, chat in enumerate(st.session_state.chat_history):
                st.write(f"**User:** {chat['query']}")
                st.write(f"**Astraea:** {chat['response']}")
                if i == len(st.session_state.chat_history) - 1:
                    user_query = st.text_area("Enter your query:", height=100, key=f"query_{i}")
                    if st.button("Query Document", key=f"button_{i}"):
                        if user_query:
                            with st.spinner("Analyzing your query..."):
                                response = get_legal_advice(user_query, document_text)
                                st.session_state.chat_history.append({"query": user_query, "response": response})
                                user_query = ""

elif option == 'Get Legal Advice':
    user_query = st.text_area("Enter your legal question:", height=100)

    if st.button("Get Legal Information"):
        if user_query:
            with st.spinner("Analyzing your query..."):
                response = get_legal_advice(user_query)
                st.write("Response:")
                st.write(response)
        else:
            st.warning("Please enter a legal question.")

st.write("Disclaimer: This AI assistant provides general information only. For specific legal advice, please consult with a qualified attorney.")
