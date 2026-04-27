# AI Resume Optimizer 🚀

An AI-powered web application that analyzes resumes against job descriptions and optimizes them for better ATS (Applicant Tracking System) compatibility using a **local Large Language Model (LLM)**.

---

## 🔥 Features

* 📄 Upload Resume (PDF / DOCX)
* 🧠 Extracts technical keywords from Job Description
* 📊 Calculates initial ATS score
* ❌ Identifies missing skills
* 🤖 Optimizes resume using local LLM (Ollama + Mistral)
* 📈 Displays improved ATS score
* ⬇️ Download optimized resume

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend:** Python
* **LLM:** Ollama (Mistral model)
* **Libraries:**

  * pdfplumber
  * python-docx
  * requests
  * python-dotenv

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/vatsaljoshi1005/AI-Resume-Optimizer
cd AI-Resume-Optimizer
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Ollama

Download and install from:
👉 https://ollama.com

---

### 4. Pull the model

```bash
ollama pull mistral
```

---

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. **Keyword Extraction**
   Extracts important technical skills from the job description using an LLM.

2. **ATS Scoring**
   Compares extracted keywords with the resume to compute an initial ATS score.

3. **Skill Gap Analysis**
   Identifies missing skills from the resume.

4. **Resume Optimization**
   Uses a local LLM to rewrite and enhance the resume:

   * Adds missing keywords
   * Improves bullet points
   * Makes content ATS-friendly

5. **Final Evaluation**
   Recalculates ATS score after optimization.

---

## 📊 Example Output

| Stage              | ATS Score |
| ------------------ | --------- |
| Initial            | 20–40%    |
| After Optimization | 80–100%   |

---

## 📸 Demo

🎥 Screen recording demonstrating:

* Resume upload
* Keyword extraction
* ATS scoring
* Resume optimization
* Improved score

<video controls src="AI Resume Optimizer - Brave 2026-04-27 18-55-57.mp4" title="Title"></video>

---

## 🚧 Limitations

* PDF parsing may mix multi-column content
* Local LLM output quality depends on model capability
* Resume formatting is plain text (no styled PDF export)

---

## 🔮 Future Improvements

* Better multi-column PDF parsing
* Support for stronger LLMs
* Export optimized resume as PDF/DOCX
* Deploy as web application
* Add user authentication & history

---

## 👨‍💻 Author

**Vatsal Joshi**

* B.Tech Computer Engineering
* GATE CSE 2026 AIR 2215 (Top 1%)
* Competitive Programmer (Codeforces)

---

## ⭐ Project Highlights

* Fully local AI system (no API dependency)
* End-to-end pipeline: parsing → analysis → optimization
* Real-world use case: ATS-based resume enhancement

---
