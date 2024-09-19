
import streamlit as st
import os
import re
from utils.document_processing import read_docx, read_pdf, read_txt, preprocess_arabic_text, format_response
from utils.legal_advice import get_legal_advice, generate_suggested_questions
from utils.oman_laws import get_oman_laws, read_oman_law
from deep_translator import GoogleTranslator
from fpdf import FPDF
import openai

# Set page configuration at the very top
st.set_page_config(page_title="Astraea - Legal Query Assistant", layout="wide")

# Custom CSS for color themes
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply custom color themes
def apply_custom_css():
    st.markdown(
        '''
        <style>
            /* Sidebar background color */
            .css-1aumxhk {
                background-color: #f0f2f6;
            }
            /* Text color in sidebar */
            .css-1aumxhk h2, .css-1aumxhk p {
                color: #1e3d59;
            }
            /* Button styles */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
            /* Header and body colors */
            .stMarkdown h1, h2, h3 {
                color: #1e3d59;
            }
            .stMarkdown {
                color: #1e3d59;
            }
        </style>
        ''', 
        unsafe_allow_html=True
    )

def main():
    # Apply custom CSS
    apply_custom_css()

    st.image("logo.png", width=300)
    st.title("Astraea - Legal Query Assistant")

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=200)
        language = st.selectbox("Choose Language / اختر اللغة", ["English", "العربية"], key="language_select")
        lang_code = "en" if language == "English" else "ar"
        st.markdown("---")
        st.markdown("### Navigation")
        option = st.radio(
            "Choose a feature" if lang_code == "en" else "اختر ميزة",
            ('Legal Query Assistant', 'Oman Laws', 'Document Upload', 'Legal Translation', 'FAQs')
        )
        
        # Adding subscription options separately
        st.markdown("---")
        st.markdown("### Subscription Options")
        st.markdown("Choose from our flexible subscription plans:")
        col1, col2, col3 = st.columns(3)

        # Basic Plan
        with col1:
            st.subheader("Basic")
            st.write("For individual users")
            st.write("- Limited access to features")
            st.write("- Basic support")
            st.button("Subscribe Basic")
        
        # Pro Plan
        with col2:
            st.subheader("Pro")
            st.write("For small businesses")
            st.write("- Access to all features")
            st.write("- Priority support")
            st.button("Subscribe Pro")
        
        # Enterprise Plan
        with col3:
            st.subheader("Enterprise")
            st.write("For large organizations")
            st.write("- Unlimited access to features")
            st.write("- Dedicated support")
            st.button("Subscribe Enterprise")

    # Main content
    if option == 'Legal Query Assistant':
        st.title("Legal Query Assistant")
        st.write("Get assistance with your legal queries here.")
        # Your existing functionality for Legal Query Assistant
        
    elif option == 'Oman Laws':
        st.title("Oman Laws")
        st.write("Access Oman laws and regulations.")
        # Your existing functionality for Oman Laws
    
    elif option == 'Document Upload':
        st.title("Document Upload")
        st.write("Upload and process legal documents.")
        # Your existing functionality for Document Upload
    
    elif option == 'Legal Translation':
        st.title("Legal Translation")
        st.write("Translate legal documents.")
        # Your existing functionality for Legal Translation
    
    elif option == 'FAQs':
        st.title("Frequently Asked Questions")
        st.write("Find answers to common legal questions.")
        # Your existing functionality for FAQs

if __name__ == '__main__':
    main()
