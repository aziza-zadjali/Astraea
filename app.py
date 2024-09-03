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
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        return '\n'.join(page.get_text() for page in pdf_document)
    except Exception as e:
        return f"An error occurred while reading the PDF file: {str(e)}"

def read_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        return f"An error occurred while reading the TXT file: {str(e)}"

def summarize_chunk(chunk):
    max_retries = 5
    retry_delay = 20  # initial delay in seconds

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a summarization assistant."},
                    {"role": "user", "content": f"Summarize the following text in a maximum of 50 words, ensuring it ends with a complete sentence:\n\n{chunk}"}
                ],
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.5,
            )
            summary = response.choices[0].message['content'].strip()
            if not summary.endswith('.'):
                summary += '.'
            return summary
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # exponential backoff
            else:
                return "An error occurred: Rate limit exceeded. Please try again later."
        except Exception as e:
            return f"An error occurred: {str(e)}"

def summarize_text(text):
    try:
        # Split the text into chunks of 2000 characters each
        chunks = [text[i:i + 2000] for i in range(0, len(text), 2000)]
        summaries = []
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(summarize_chunk, chunk) for chunk in chunks]
            for future in futures:
                summaries.append(future.result())
                time.sleep(20)  # Wait for 20 seconds to avoid rate limit issues
        
        # Combine all chunk summaries into a final summary
        final_summary = " ".join(summaries)
        return final_summary
    except Exception as e:
        return f"An error occurred while summarizing: {str(e)}"

st.title("Legal Query Assistant")

st.write("This assistant uses GPT-4 to provide general legal information. Please note that this is not a substitute for professional legal advice.")

# Sidebar layout with dropdown menu
st.sidebar.title("Astraea")
feature = st.sidebar.selectbox("Select a feature", ["Enter your legal question", "Upload a document"])

# Page for entering a legal question
if feature == 'Enter your legal question':
    user_query = st.text_area("Enter your legal question:", height=100)

    if st.button("Get Legal Information"):
        if user_query:
            with st.spinner("Analyzing your query..."):
                response = get_legal_advice(user_query)
                st.write("Response:")
                st.write(response)
                # Update chat history
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        else:
            st.warning("Please enter a legal question.")

# Page for uploading a document
if feature == 'Upload a document':
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
            
            if "An error occurred" in document_text:
                st.error(document_text)
            else:
                summary = summarize_text(document_text)
                st.write("Document Summary:")
                st.write(summary)

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
        else:
            st.warning("Please enter a legal question.")

st.write("Disclaimer: This AI assistant provides general information only. For specific legal advice, please consult with a qualified attorney.")
