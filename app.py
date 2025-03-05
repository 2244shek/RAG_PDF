import streamlit as st
import json
import pytesseract
import fitz  # PyMuPDF for PDFs
from PIL import Image
import google.generativeai as genai
import easyocr
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("Google_API")

# Configure API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

def extract_text_from_pdf(pdf_file):
    """Extracts text from PDF with better accuracy."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

def extract_text_from_image(image_file):
    """Extracts text from an image using EasyOCR instead of Tesseract."""
    reader = easyocr.Reader(['en'])  # English language
    image = Image.open(image_file)
    result = reader.readtext(image, detail=0)
    return "\n".join(result)

def clean_extracted_text(text):
    """Cleans extracted text to remove unwanted artifacts."""
    text = text.replace("\n\n", "\n").strip()  # Remove extra new lines
    return text

def get_json_from_text(text):
    """Uses Google Gemini API to structure extracted text into JSON format."""
    prompt = f"""
    The following text is extracted from a structured form. Convert it into a properly formatted JSON with relevant key-value pairs.

    Text:
    {text}

    - Extract all key-value pairs correctly.
    - Ensure fields like "Name", "Date of Birth", "Account Number", etc., are well-organized.
    - Return **only** JSON format without additional text.
    """

    response = gemini_model.generate_content(prompt)

    if response and hasattr(response, "text"):
        response_text = response.text.strip()

        # Handle cases where Gemini wraps JSON in markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        try:
            json_data = json.loads(response_text)  # Parse JSON safely
        except json.JSONDecodeError:
            json_data = {"error": "Failed to parse response as JSON. Please check the extraction."}
    else:
        json_data = {"error": "No response from Google Gemini API."}

    return json_data

# # Streamlit UI
# st.title("AI-Powered Form Extraction to JSON")
# st.write("Upload a **PDF or image** of a form, and the system will extract and structure the details into JSON.")

# uploaded_file = st.file_uploader("Upload a form (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

# if uploaded_file is not None:
#     file_type = uploaded_file.type
    
#     with st.spinner("Extracting text..."):
#         if "pdf" in file_type:
#             raw_text = extract_text_from_pdf(uploaded_file)
#         else:
#             raw_text = extract_text_from_image(uploaded_file)

#     cleaned_text = clean_extracted_text(raw_text)

#     st.subheader("Extracted Text")
#     st.text_area("", cleaned_text, height=200)

#     if st.button("Convert to JSON"):
#         with st.spinner("Generating structured JSON..."):
#             json_output = get_json_from_text(cleaned_text)
        
#         st.subheader("Structured JSON Output")
#         st.json(json_output)

# Streamlit UI
st.set_page_config(page_title="RAG Form Extractor | Abhishek", layout="centered")
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #4CAF50;
    }
    .stTextArea > label {
        font-size: 18px;
        font-weight: bold;
    }
    .stJson > label {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 RAG Based Form Extraction to JSON")
st.write("Upload a **PDF or image** of a form, and the system will extract and structure the details into JSON.")

uploaded_file = st.file_uploader("Upload a form (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"], help="Supported formats: PDF, PNG, JPG, JPEG")

if uploaded_file is not None:
    file_type = uploaded_file.type
    extracted_text = ""
    
    with st.spinner("Extracting text..."):
        if "pdf" in file_type:
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = extract_text_from_image(uploaded_file)
    
    cleaned_text = clean_extracted_text(extracted_text)

    if st.button("🔍 Show Extracted Text"):
        st.subheader("Extracted Text")
        st.text_area("", cleaned_text, height=200)

    if st.button("🛠 Convert to JSON"):
        with st.spinner("Generating structured JSON..."):
            json_output = get_json_from_text(cleaned_text)
        st.subheader("📊 Structured JSON Output")
        st.json(json_output)
