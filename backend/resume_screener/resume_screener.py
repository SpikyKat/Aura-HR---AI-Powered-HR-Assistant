from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF
import json
import re

# This is now the only function in this file, as it handles all resume screening tasks.
def ats_and_fit_analysis(resume_path, jd_path):
    """
    Performs a comprehensive analysis including ATS parsing and a fit score against a JD.
    """
    try:
        # Extract text from resume and JD
        with fitz.open(resume_path) as resume_doc:
            resume_text = "".join(page.get_text() for page in resume_doc)
        with fitz.open(jd_path) as jd_doc:
            jd_text = "".join(page.get_text() for page in jd_doc)

        prompt = f"""
        You are a world-class Applicant Tracking System (ATS) with advanced analytical capabilities.
        Your task is to perform a two-part analysis on the provided resume and job description.
        Your response MUST be a single, valid JSON object and nothing else.

        The required JSON structure is as follows:

        {{
          "fit_analysis": {{
            "fit_score": "An integer between 0 and 100.",
            "summary": "A brief one-paragraph summary of the candidate's suitability.",
            "matching_skills": ["A list of key skills from the JD that the candidate possesses."],
            "missing_skills": ["A list of key skills from the JD the candidate seems to be missing."]
          }},
          "ats_parsing": {{
            "contact_info": {{ "name": "string", "email": "string", "phone": "string", "location": "string" }},
            "professional_summary": "string",
            "work_experience": [
              {{ "job_title": "string", "company": "string", "start_date": "string (Month YYYY)", "end_date": "string (Month YYYY or 'Present')", "responsibilities": ["string", ...] }}
            ],
            "education": [
              {{ "degree": "string", "institution": "string", "graduation_date": "string (YYYY)" }}
            ],
            "skills": ["A comprehensive list of all skills found in the resume."]
          }}
        }}

        Perform this analysis on the following documents:
        ---
        RESUME:
        {resume_text}
        ---
        JOB DESCRIPTION:
        {jd_text}
        ---
        """
        response = get_groq_response(prompt)

        # Robust JSON Parsing
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError("No valid JSON object found in the LLM response.")
        except (json.JSONDecodeError, ValueError) as e:
            return {"error": f"Failed to parse AI response. Error: {e}. Raw response: '{response[:200]}...'"}

    except Exception as e:
        return {"error": f"An unexpected error occurred during analysis: {e}"}
