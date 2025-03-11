# 📝 AI Form Extractor (RAG-Based)

Extract structured data from **PDFs and images** using AI! This Streamlit-based app leverages **Google Gemini API** for text structuring, OCR (Tesseract), and medical term extraction. 🚀

---

## 📌 Features

✅ **Extract Text from PDFs & Images** using **PyMuPDF** (for PDFs) and **Tesseract OCR** (for images).  
✅ **Convert Unstructured Text to JSON** using **Google Gemini API**.  
✅ **Identify & Categorize Medical Terms** (diseases, medications, symptoms, etc.).  
✅ **Interactive UI with Streamlit** – Upload files, process data, and download JSON.  
✅ **Supports Multi-Page PDFs & Various Image Formats** (PNG, JPG, JPEG).  

---

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/ai-form-extractor.git
cd ai-form-extractor
```
### **2️⃣ Create a Virtual Environment**
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```
### **3️⃣ Install Dependencies**
```
pip install -r requirements.txt
```
### **4️⃣ Set Up Environment Variables**
```
CREATE .env file and set your API_KEY:-->
GOOGLE_API_KEY=your_api_key_here
```
### **5️⃣ Run the App**
```
streamlit run app.py
```
---

## 🎯 Usage
**Upload a PDF or image of a structured form.**
**Extract text using OCR (for images) or PDF parsing.**
**Convert text into structured JSON using AI.**
**Identify medical terms (optional).**
**Download JSON output for further use.**

---

## 📂 Project Structure
📂 ai-form-extractor
│-- 📜 app.py                # Main Streamlit app
│-- 📜 requirements.txt      # Dependencies
│-- 📜 .env.example          # Example of API key setup
│-- 📜 README.md             # Documentation

---

## ⚡ API Integration
This app uses Google Gemini API to convert extracted text into structured JSON.
**Text Extraction → OCR (Tesseract) + PyMuPDF**
**AI Processing → Google Gemini API**
**Medical Terms Extraction → AI Categorization**
