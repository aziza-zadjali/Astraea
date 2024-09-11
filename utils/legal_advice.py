import streamlit as st
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600)
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_legal_advice(query, document_text=None, language="en"):
    try:
        system_content = {
            "en": "You are Astraea, an expert legal assistant specializing in legal documents. Provide concise and accurate information based on the given document. Focus on key aspects such as the nature of the case, parties involved, legal issues, and court decisions.",
            "ar": "أنت أسترايا، مساعد قانوني خبير متخصص في الوثائق القانونية. قدم معلومات موجزة ودقيقة بناءً على الوثيقة المعطاة. ركز على الجوانب الرئيسية مثل طبيعة القضية والأطراف المعنية والقضايا القانونية وقرارات المحكمة."
        }

        messages = [
            {"role": "system", "content": system_content[language]},
            {"role": "user", "content": query}
        ]

        if document_text:
            chunk_size = 4000
            chunks = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]
            
            with ThreadPoolExecutor(max_workers=min(len(chunks), 5)) as executor:
                future_to_chunk = {executor.submit(summarize_chunk, chunk, i, len(chunks), language): i for i, chunk in enumerate(chunks)}
                summaries = []
                for future in as_completed(future_to_chunk):
                    summaries.append(future.result())

            combined_summary = "\n\n".join(summaries)
            final_prompt = {
                "en": f"Based on the following document summaries, answer this question concisely: {query}\n\nDocument summaries:\n{combined_summary}",
                "ar": f"بناءً على ملخصات الوثيقة التالية، أجب على هذا السؤال بإيجاز: {query}\n\nملخصات الوثيقة:\n{combined_summary}"
            }

            messages.append({"role": "user", "content": final_prompt[language]})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        full_response = response.choices[0].message['content'].strip()
        return full_response
    except Exception as e:
        logger.error(f"An error occurred in get_legal_advice: {str(e)}")
        return f"An error occurred: {str(e)}"

def summarize_chunk(chunk, i, total_chunks, language):
    context_prompt = {
        "en": f"Document context (Part {i+1}/{total_chunks}): {chunk}\n\nProvide a brief summary of this part of the document, focusing on key legal aspects.",
        "ar": f"سياق الوثيقة (الجزء {i+1}/{total_chunks}): {chunk}\n\nقدم ملخصًا موجزًا لهذا الجزء من الوثيقة، مع التركيز على الجوانب القانونية الرئيسية."
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes legal documents."},
            {"role": "user", "content": context_prompt[language]}
        ],
        max_tokens=250,
        temperature=0.7
    )

    return response.choices[0].message['content'].strip()

@st.cache_data(ttl=3600)
def generate_suggested_questions(document_text, language):
    try:
        prompt = {
            "en": f"Based on the following legal document, generate 3 relevant questions that a user might ask about the case:\n\n{document_text[:1500]}...",
            "ar": f"بناءً على الوثيقة القانونية التالية، قم بإنشاء 3 أسئلة ذات صلة قد يطرحها المستخدم حول القضية:\n\n{document_text[:1500]}..."
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates relevant questions based on legal documents."},
                {"role": "user", "content": prompt[language]}
            ],
            max_tokens=150
        )

        suggested_questions = response.choices[0].message['content'].strip().split('\n')
        return [q.strip('1234567890. ') for q in suggested_questions if q.strip()]
    except Exception as e:
        logger.error(f"Error generating suggested questions: {str(e)}")
        return []
