from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF

def summarize_candidate(resume_path):
    """
    Generates a concise summary of a candidate's resume.
    """
    try:
        with fitz.open(resume_path) as resume_doc:
            resume_text = ""
            for page in resume_doc:
                resume_text += page.get_text()

        prompt = f"""
        Based on the following resume, please provide a concise, one-paragraph summary highlighting the candidate's key qualifications, experience, and skills. This summary is for a busy hiring manager.

        Resume:
        {resume_text}
        """
        response = get_groq_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"
