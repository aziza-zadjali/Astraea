import openai
import langchain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.cache import InMemoryCache
import streamlit as st
import logging

logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set up caching
langchain.llm_cache = InMemoryCache()

@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo-16k",
        temperature=0.7,
        max_tokens=1000,
        request_timeout=60
    )

@st.cache_resource
def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

@st.cache_data(ttl=3600)
def get_legal_advice(query, document_text=None, lang_code="en"):
    try:
        llm = get_llm()
        memory = get_memory()

        system_content = {
            "en": "You are Astraea, an expert legal assistant specializing in legal documents.",
            "ar": "أنت أسترايا، مساعد قانوني خبير متخصص في الوثائق القانونية."
        }

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input", "context"],
            template=f"{system_content[lang_code]}\n\nChat History: {{chat_history}}\nHuman: {{human_input}}\nContext: {{context}}\nAstraea:"
        )

        chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

        with get_openai_callback() as cb:
            if document_text:
                context = summarize_document(document_text, lang_code)
            else:
                context = "No additional context provided."
            
            response = chain.run(human_input=query, context=context)
            
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

        return response

    except Exception as e:
        logger.error(f"An error occurred in get_legal_advice: {str(e)}")
        return f"An error occurred: {str(e)}"

def summarize_document(document_text, lang_code):
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["document"],
        template="Summarize the following document, focusing on key legal aspects:\n\n{document}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(document=document_text[:4000])

@st.cache_data(ttl=3600)
def generate_suggested_questions(document_text, lang_code):
    try:
        llm = get_llm()
        prompt = PromptTemplate(
            input_variables=["document"],
            template="Based on the following legal document, generate 5 relevant questions a user might ask:\n\n{document}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(document=document_text[:2000])
        return response.strip().split('\n')
    except Exception as e:
        logger.error(f"Error generating suggested questions: {str(e)}")
        return []
