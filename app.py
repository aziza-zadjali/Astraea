import streamlit as st
from PyPDF2 import PdfReader
import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set up Streamlit app layout
st.title("Astraea GenAI Legal Assistant")
st.sidebar.header("Legal Query Assistant")

# Function to read and extract text from the uploaded PDF file
def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to split text into smaller chunks (for large documents)
def split_text(text, max_tokens=3000):
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0

    for sentence in sentences:
        token_count = len(sentence.split())
        if current_chunk_tokens + token_count > max_tokens:
            chunks.append(". ".join(current_chunk))
            current_chunk = [sentence]
            current_chunk_tokens = token_count
        else:
            current_chunk.append(sentence)
            current_chunk_tokens += token_count

    # Add any remaining text
    if current_chunk:
        chunks.append(". ".join(current_chunk))

    return chunks

# Upload PDF document
uploaded_file = st.sidebar.file_uploader("Upload a legal document", type=["pdf"])

# If a document is uploaded, read and split it into chunks
if uploaded_file:
    document_text = read_pdf(uploaded_file)
    st.write("Document uploaded and processed successfully!")
    
    # Split the document into smaller chunks
    document_chunks = split_text(document_text, max_tokens=3000)
    st.write(f"Document split into {len(document_chunks)} chunks.")
else:
    st.warning("Please upload a PDF legal document.")

# Retrieve OpenAI API key from secrets and set it
openai.api_key = st.secrets["OPENAI_API_KEY"]

# If the API key is provided, set up the Chat model and query function
if openai.api_key:
    # Initialize ChatOpenAI with the newer model like gpt-3.5-turbo
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

    # Define the prompt template
    template = """
    You are a legal assistant. Answer the following question based on the provided legal document.
    
    Question: {question}
    
    Legal Document: {document}
    
    Answer:
    """

    # Create a prompt template and LLM chain
    prompt = PromptTemplate(input_variables=["question", "document"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)

    # User input section for legal question
    question = st.text_area("Ask your legal question")

    # When the user submits the question
    if st.button("Submit"):
        if question:
            if uploaded_file:
                # Use the first chunk of the document to reduce token size
                selected_document = document_chunks[0] if len(document_chunks) > 0 else ""
                
                # Send the first chunk to the model
                response = chain.run({"question": question, "document": selected_document})
                st.write(response)
            else:
                st.error("Please upload a document first.")
        else:
            st.error("Please enter a valid legal query.")
else:
    st.error("API key is not configured")
