import streamlit as st
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
import logging

logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600)
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_legal_advice(query, document_text=None, language="en"):
    try:
        system_content = {
            "en": "You are Astraea, an expert legal assistant specializing in legal documents. Provide detailed and accurate information based on the given document. Focus on key aspects such as the nature of the case, parties involved, legal issues, and court decisions.",
            "ar": "أنت أسترايا، مساعد قانوني خبير متخصص في الوثائق القانونية. قدم معلومات مفصلة ودقيقة بناءً على الوثيقة المعطاة. ركز على الجوانب الرئيسية مثل طبيعة القضية والأطراف المعنية والقضايا القانونية وقرارات المحكمة."
        }
        
        messages = [
            {"role": "system", "content": system_content[language]},
            {"role": "user", "content": query}
        ]
        
        if document_text:
            chunk_size = 4000
            chunks = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]
            summaries = []
            
            for i, chunk in enumerate(chunks):
                context_prompt = {
                    "en": f"Document context (Part {i+1}/{len(chunks)}): {chunk}\n\nProvide a brief summary of this part of the document, focusing on key legal aspects.",
                    "ar": f"سياق الوثيقة (الجزء {i+1}/{len(chunks)}): {chunk}\n\nقدم ملخصًا موجزًا لهذا الجزء من الوثيقة، مع التركيز على الجوانب القانونية الرئيسية."
                }
                
                chunk_messages = messages + [{"role": "user", "content": context_prompt[language]}]
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=chunk_messages,
                    max_tokens=500,
                    temperature=0.7
                )
                
                summary = response.choices[0].message['content'].strip()
                summaries.append(summary)
            
            combined_summary = "\n\n".join(summaries)
            final_prompt = {
                "en": f"Based on the following document summaries, answer this question: {query}\n\nDocument summaries:\n{combined_summary}",
                "ar": f"بناءً على ملخصات الوثيقة التالية، أجب على هذا السؤال: {query}\n\nملخصات الوثيقة:\n{combined_summary}"
            }
            
            messages.append({"role": "user", "content": final_prompt[language]})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        full_response = response.choices[0].message['content'].strip()
        return full_response
    except Exception as e:
        logger.error(f"An error occurred in get_legal_advice: {str(e)}")
        return f"An error occurred: {str(e)}"

@st.cache_data(ttl=3600)
def generate_suggested_questions(document_text, language):
    try:
        prompt = {
            "en": f"Based on the following legal document, generate 5 relevant questions that a user might ask about the case:\n\n{document_text[:2000]}...",
            "ar": f"بناءً على الوثيقة القانونية التالية، قم بإنشاء 5 أسئلة ذات صلة قد يطرحها المستخدم حول القضية:\n\n{document_text[:2000]}..."
        }
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates relevant questions based on legal documents."},
                {"role": "user", "content": prompt[language]}
            ],
            max_tokens=200
        )
        
        suggested_questions = response.choices[0].message['content'].strip().split('\n')
        return [q.strip('1234567890. ') for q in suggested_questions if q.strip()]
    except Exception as e:
        logger.error(f"Error generating suggested questions: {str(e)}")
        return []

# Streamlit UI
st.title("Legal Advice Assistant")

document_text = st.text_area("Paste your legal document here")
query = st.text_input("Enter your query here")

if st.button("Submit"):
    if document_text and query:
        response = get_legal_advice(query, document_text)
        st.write(response)
        st.session_state['last_response'] = response
    else:
        st.write("Please provide both a document and a query.")

if 'last_response' in st.session_state:
    if st.button("Get New Suggested Questions"):
        suggested_questions = generate_suggested_questions(document_text)
        st.write("Suggested Questions:")
        for question in suggested_questions:
            if st.button(question):
                query = question
                response = get_legal_advice(query, document_text)
                st.write(response)
                st.session_state['last_response'] = response
else:
    if document_text:
        suggested_questions = generate_suggested_questions(document_text)
        st.write("Suggested Questions:")
        for question in suggested_questions:
            if st.button(question):
                query = question
                response = get_legal_advice(query, document_text)
                st.write(response)
                st.session_state['last_response'] = response
