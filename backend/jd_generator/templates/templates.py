import os
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # or your chosen Groq-supported LLaMA model

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def screen_resume_against_jd(resume_pdf_path, jd_pdf_path):
    resume_text = extract_text_from_pdf(resume_pdf_path)
    jd_text = extract_text_from_pdf(jd_pdf_path)

    prompt = f"""
You are an HR assistant. The following is a job description and a candidate's resume.

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Based on the above, answer:
1. Does the candidate match the job requirements?
2. What are the candidate's strengths?
3. What are the missing qualifications or gaps?
4. Give an overall fit score out of 100.
5. Final verdict: Shortlist or Reject?

Respond in bullet points.
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4
        }
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"
