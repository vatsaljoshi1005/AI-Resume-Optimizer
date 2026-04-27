import streamlit as st
import pdfplumber
import requests
from docx import Document
from dotenv import load_dotenv

load_dotenv()

def extract_keyword(jd_text):
    prompt = f"""
Extract ONLY technical skills from this job description.

STRICT:
- Only comma-separated keywords
- No sentences
- No explanation

Job Description:
{jd_text}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        keywords = data.get("response", "").strip()

        if len(keywords) < 5:
            raise Exception("Bad LLM output")

        return keywords

    except:
        jd_text = jd_text.lower()

        common_skills = [
            "python", "java", "c++", "sql", "machine learning",
            "deep learning", "tensorflow", "pytorch",
            "data analysis", "pandas", "numpy",
            "flask", "fastapi", "docker", "aws", "git"
        ]

        found = [skill for skill in common_skills if skill in jd_text]

        return ", ".join(found)



def call_local_llm(resume_text, jd_text, keywords_list):
    prompt = f"""
You are a top-tier ATS resume optimizer.

Rewrite the resume to maximize ATS score for the given job.

STRICT:
- Output ONLY the resume
- Use bullet points
- Use strong action verbs
- Add measurable impact (numbers if possible)
- Include missing keywords naturally
- Do NOT leave sections empty

MANDATORY KEYWORDS:
{", ".join(keywords_list)}

FORMAT:

SUMMARY:
2–3 lines

SKILLS:
- skills list

EXPERIENCE:
- role
  - achievement-based bullet

PROJECTS:
- project
  - what + tech + impact

EDUCATION:
- degree

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        if "response" in data and data["response"]:
            return data["response"]
        else:
            return ""

    except:
        return ""



st.set_page_config(page_title="AI Resume Optimizer", layout="wide")
st.title("AI Resume Optimizer")

st.write("Upload your resume and paste the job description to optimize it.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

with col2:
    role = st.text_input("Target Role (optional)")

jd_text = st.text_area("Paste Job Description", height=200)



if st.button("Optimize Resume"):

    if uploaded_file is None or jd_text.strip() == "":
        st.warning("Please upload resume and enter job description")

    else:
        st.write("Parsing resume...")

        
        if uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = ""
                for page in pdf.pages:
                    text = page.extract_text(x_tolerance=2, y_tolerance=2)
                    if text:
                        resume_text += text + "\n"

        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            resume_text = ""
            for para in doc.paragraphs:
                resume_text += para.text + "\n"

        else:
            st.error("Unsupported file format")
            st.stop()

        resume_text = " ".join(resume_text.split())

        # KEYWORDS
        st.info("Extracting keywords...")

        keywords = extract_keyword(jd_text)

        keywords_list = [
            k.strip().lower()
            for k in keywords.split(",")
            if len(k.strip()) > 1
        ]

        if not keywords_list:
            st.error("Keyword extraction failed")
            st.stop()

        keywords_list = list(set(keywords_list))

        st.subheader("Extracted Keywords")
        st.success(", ".join(keywords_list))

        #INITIAL SCORE
        resume_lower = resume_text.lower()

        matched = [k for k in keywords_list if k in resume_lower]
        missing = [k for k in keywords_list if k not in resume_lower]

        score = int((len(matched) / len(keywords_list)) * 100) if keywords_list else 0

        st.subheader("Initial ATS Score")
        st.progress(score)
        st.write(f"{score}% match with job description")

        st.subheader("Matched Skills")
        st.success(", ".join(matched) if matched else "None")

        st.subheader("Missing Skills")
        st.warning(", ".join(missing) if missing else "None")

        #STEP 3: OPTIMIZE
        with st.spinner("Optimizing resume..."):
            optimized_resume = call_local_llm(resume_text, jd_text, keywords_list)

        if not optimized_resume:
            st.error("Resume optimization failed. Try again.")
            st.stop()

        st.subheader("Optimized Resume")
        st.write(optimized_resume)

        #STEP 4: FINAL SCORE
        optimized_lower = optimized_resume.lower()

        matched_new = [k for k in keywords_list if k in optimized_lower]

        score_new = int((len(matched_new) / len(keywords_list)) * 100) if keywords_list else 0

        st.subheader("Improved ATS Score")
        st.progress(score_new)
        st.success(f"Improved from {score}% → {score_new}%")

        st.download_button(
            label="Download Optimized Resume",
            data=optimized_resume,
            file_name="optimized_resume.txt",
            mime="text/plain"
        )