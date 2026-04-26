#streamlit-> a python library to build UI
import streamlit as st
#pdfplumber-> exports text from PDF reliably
import pdfplumber
import requests
#Document() lets u read paras and text
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def call_local_llm(resume_text,jd_text):
    prompt=f"""
You are an expert resume writer.

Optimize the following resume for the job description.

Focus on:
-ATS-friendly structure
-Strong keyword alignment
-Impact-driven bullet points

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    response=requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
    )
    data=response.json()
    if "response" in data:
        return data["response"]
    else:
        return str(data)
    

#page_title->browser tab title
st.set_page_config(page_title="AI Resume Optimizer",layout="wide")

#creates a main heading(H1) on your app page
st.title("AI Resume Optimizer")

#st.text()->plain text
#st.markdown()->formatted text
#st.write()->flexible, automatically formats nicely
st.write("Upload your resume and paste the job description to optimize it.")
#split into two columns
col1,col2=st.columns(2)

with col1:
    #create a file object to accept file
    uploaded_file=st.file_uploader("Upload Resume(PDF/DOCX)",type=["pdf","docx"])

with col2:
    role=st.text_input("Target Role(optional)")

jd_text=st.text_area("Paste Job Description",height=200)

#create a clickable button, code runs only if user clicks this button
if st.button("Optimize Resume"):
    #if resume is missing ot jd is missing
    if uploaded_file is None or jd_text.strip()=="":
        st.warning("Please upload resume and enter job description")
    else:
        st.write("Parsing resume...")
        file_name=uploaded_file.name
        if file_name.endswith(".pdf"):
            #convert binary file->readable PDF object
            #with something as x opens resource,use it and automatically close it
            #pdf-> a PDF obj contanining pages
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text=""
                #append extracted text of each page into one final string
                for page in pdf.pages:
                    text=page.extract_text()
                    #if text is not NULL then add
                    if text:
                        resume_text+=text+"\n"
        
        elif file_name.endswith(".docx"):
            #opening docx file 
            doc=Document(uploaded_file)
            resume_text=""
            for para in doc.paragraphs:
                #no need to check for empty text as DOCX always gives string
                resume_text+=para.text+"\n"
                #st.text(resume_text[:500])
        else:
            st.error("Unsupported file format")
            st.stop()

        st.write("Calling LLM...")
        optimized_resume=call_local_llm(resume_text,jd_text)
        st.subheader("Optimized Resume")
        st.write(optimized_resume)








