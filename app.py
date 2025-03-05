import streamlit as st
import json
import pytesseract
import fitz  # PyMuPDF for PDFs
from PIL import Image
import google.generativeai as genai
import pandas as pd
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
    """Extracts text from an image using Tesseract OCR with optimized settings."""
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image, config="--oem 3 --psm 6")
    return text.strip()

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

def extract_medical_terms(text):
    """Uses Google Gemini API to extract and categorize medical terms."""
    prompt = f"""
    Extract only medical-related terms from the following text. Examples include diseases, symptoms, treatments, and medical conditions
    and categorize all medical-related terms from the following text.
    The categories should include:
    - Diseases
    - Medications
    - Symptoms
    - Medical Procedures
    - Medical Devices
    - Chemicals

    Text:
    {text}
    
    Return the response in this **exact JSON format**:
    {{
        "Diseases": ["disease1", "disease2"],
        "Medications": ["medication1", "medication2"],
        "Symptoms": ["symptom1", "symptom2"],
        "Medical Procedures": ["procedure1", "procedure2"],
        "Medical Devices": ["device1", "device2"],
        "Chemicals": ["chemical1", "chemical2"]
    }}

    Ensure:
    - No extra text, only valid JSON.
    - No explanations, only the structured JSON response.
    """

    response = gemini_model.generate_content(prompt)

    if response and hasattr(response, "text"):
        response_text = response.text.strip()

        # Handle cases where Gemini wraps JSON in markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        try:
            json_data = json.loads(response_text)  # Parse JSON safely
            return json_data
        except json.JSONDecodeError:
            return {"error": "Gemini returned an invalid response. Try again."}
    else:
        return {"error": "No response from Google Gemini API."}

# Streamlit UI Enhancements
st.set_page_config(page_title="AI Form Extractor", layout="centered")
st.markdown("""
    <style>
    .stButton > button {
        background-color: #590f79;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #590f79;
    }
    .stTextArea > label {
        font-size: 18px;
        font-weight: bold;
    }
    .stJson > label {
        font-size: 18px;
        font-weight: bold;
    }
    .center-text {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 RAG Based Form Extraction to JSON")
st.write("Upload a **PDF or image** of a form, and the system will extract and structure the details into JSON.")

# Initialize session state for UI buttons
if "show_extracted" not in st.session_state:
    st.session_state.show_extracted = False
if "show_medical_terms" not in st.session_state:
    st.session_state.show_medical_terms = False

uploaded_file = st.file_uploader("📂 Upload a form (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"], help="Supported formats: PDF, PNG, JPG, JPEG")

if uploaded_file is not None:
    file_type = uploaded_file.type
    extracted_text = ""

    with st.spinner("🔍 Extracting text..."):
        if "pdf" in file_type:
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = extract_text_from_image(uploaded_file)

    cleaned_text = clean_extracted_text(extracted_text)

    # Button to show extracted text
    if st.button("👁 Show Extracted Text"):
        st.session_state.show_extracted = not st.session_state.show_extracted

    if st.session_state.show_extracted:
        st.subheader("📜 Extracted Text")
        st.text_area("", cleaned_text, height=200)

    # Button to convert text to JSON
    if st.button("🛠 Convert to JSON"):
        with st.spinner("🧠 Generating structured JSON..."):
            json_output = get_json_from_text(cleaned_text)
        st.subheader("📊 Structured JSON Output")
        st.json(json_output)
        
        # Add download button for JSON file
        json_str = json.dumps(json_output, indent=4)
        st.download_button(label="📥 Download JSON", data=json_str, file_name="extracted_data.json", mime="application/json")

    # Button to extract medical terms
    if st.button("⚕️ Extract Medical Terms"):
        st.session_state.show_medical_terms = not st.session_state.show_medical_terms

    if st.session_state.show_medical_terms:
        with st.spinner("🔎 Identifying Medical Terms..."):
            medical_terms = extract_medical_terms(cleaned_text)
        st.subheader("🩺 Medical Terms Found")
        st.write(medical_terms if medical_terms else "No medical terms found.")
