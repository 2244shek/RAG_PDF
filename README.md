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

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

pip install -r requirements.txt

streamlit run app.py
```
