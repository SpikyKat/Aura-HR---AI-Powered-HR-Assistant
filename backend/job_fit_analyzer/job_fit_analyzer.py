from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF

def analyze_job_fit(candidate_profile, jd_path):
    """
    Analyzes the fit between a candidate profile and a job description.
    """
    try:
        with fitz.open(jd_path) as jd_doc:
            jd_text = ""
            for page in jd_doc:
                jd_text += page.get_text()

        prompt = f"""
        Analyze the compatibility between the following candidate profile and job description.
        Provide a compatibility score and a summary of the analysis.

        Candidate Profile/Bio:
        {candidate_profile}

        Job Description:
        {jd_text}

        Output format:
        Compatibility Score: [score]%
        Summary: [detailed summary of why the candidate is or is not a good fit]
        """
        response = get_groq_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"
