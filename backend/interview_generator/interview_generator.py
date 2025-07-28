from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF

def generate_interview_questions(jd_path):
    """
    Generates interview questions based on a job description.
    """
    try:
        with fitz.open(jd_path) as jd_doc:
            jd_text = ""
            for page in jd_doc:
                jd_text += page.get_text()

        prompt = f"""
        Based on the following job description, generate a list of 10-15 insightful interview questions.
        The questions should cover technical skills, behavioral aspects, and cultural fit.

        Job Description:
        {jd_text}

        Categorize the questions into:
        - Technical Questions
        - Behavioral Questions
        - Situational Questions
        """
        response = get_groq_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

