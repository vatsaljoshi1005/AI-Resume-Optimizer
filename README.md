# AI Resume Optimizer (Local LLM Powered)

AI-powered Resume Optimizer built using Streamlit and Ollama (LLaMA/phi).

## 🚀 Features

* Upload Resume (PDF/DOCX)
* Extract text from resume
* Paste Job Description
* AI-based resume optimization
* Runs completely locally (no API, no cost)

## 🧠 Tech Stack

* Python
* Streamlit
* pdfplumber
* python-docx
* Ollama (Local LLM)
* requests

## ⚙️ Setup Instructions

### 1. Install dependencies

pip install -r requirements.txt

### 2. Install Ollama

https://ollama.com

### 3. Run model

ollama run phi

### 4. Run app

streamlit run app.py

## 💡 Note

* Uses local LLM (phi) for fast and cost-free execution
* No API key required

## 🎯 Future Improvements

* Keyword extraction from JD
* ATS score calculation
* Resume section restructuring
