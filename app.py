import time
import streamlit as st
import openai
from docx import Document
import fitz  # PyMuPDF
from concurrent.futures import ThreadPoolExecutor

# Display the logo image
st.image("logo.png", width=100)

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_legal_advice(query, document_text=None):
    try:
        messages = [
            {"role": "system", "content": "You are Astraea, a knowledgeable legal assistant with access to extensive legal information. Your role is to assist lawyers, law firms, and the general public by providing general legal information. Please ensure to remind users that for specific legal issues, consulting a qualified attorney is recommended."},
            {"role": "user", "content": query}
        ]
        if document_text:
            messages.append({"role": "user", "content": f"Here is the content of the uploaded document: {document_text}"})

        # Add chat history to messages
        messages.extend(st.session_state.chat_history)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        response_content = response.choices[0].message['content']
        source_link = "Source: 1"

        # Update chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response_content})

        return f"{response_content}\n\n{source_link}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def read_docx(file):
    try:
        doc = Document(file)
        return '\n'.join(para.text for para in doc.paragraphs)
    except Exception as e:
        return f"An error occurred while reading the DOCX file: {str(e)}"

def read_pdf(file):
    try:
        pdf_document = fitz.open(stream=file.read(), filetype='pdf')
        text = ''
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        return f"An error occurred while reading the PDF file: {str(e)}"

def summarize_text(text):
    # Placeholder for summarization logic or API call
    return text[:500]  # Returning the first 500 characters for demonstration

def read_and_summarize_document(file, file_type):
    # Depending on file type, read the document
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document_text = read_docx(file)
    elif file_type == "application/pdf":
        document_text = read_pdf(file)
    elif file_type == "text/plain":
        document_text = file.getvalue().decode("utf-8")
    else:
        return "Unsupported file type.", None

    if "An error occurred" in document_text:
        return document_text, None

    # Summarize the text
    summary = summarize_text(document_text)
    return document_text, summary

def handle_document(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(read_and_summarize_document, uploaded_file, file_type)
            document_text, summary = future.result()
            return document_text, summary
    else:
        return "No file uploaded.", None

uploaded_file = st.file_uploader("Upload a document", type=["docx", "pdf", "txt"])
if uploaded_file:
    document_text, summary = handle_document(uploaded_file)
    if document_text and summary:
        st.write("Document Summary:")
        st.write(summary)
    elif document_text:
        st.error(document_text)
    else:
        st.warning("Please upload a valid document.")

user_query = st.text_area("Enter your legal question:", height=100)
if st.button("Get Legal Information"):
    if user_query:
        with st.spinner("Analyzing your query..."):
            response = get_legal_advice(user_query, document_text)
            st.write("Response:")
            st.write(response)
            # Update chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            if "An error occurred" in response:
                if st.button("Search for more information on the web"):
                    st.write("Searching for more information on the web...")
                    # Implement web search functionality here
    else:
        st.warning("Please enter a legal question.")

st.write("Disclaimer: This AI assistant provides general information only. For specific legal advice, please consult with a qualified attorney.")
