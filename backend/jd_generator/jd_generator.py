from ..helpers.llm_helper import get_groq_response

def generate_jd(role, level, skills, tone):
    """
    Generates a job description with a specific tone.
    """
    prompt = f"""
    Generate a detailed job description for the role of a {role} at a {level} level.
    The required skills are: {skills}.

    The tone of the job description should be: {tone}.

    The job description should include:
    - Job Title
    - Job Summary
    - Responsibilities
    - Requirements and Skills
    - Company Culture/Perks (tailored to the specified tone)
    """
    response = get_groq_response(prompt)
    return response

def check_inclusivity(jd_text):
    """
    Analyzes a job description for inclusive language.
    """
    prompt = f"""
    Please act as an inclusivity expert. Review the following job description for any language that might be biased, non-inclusive, or could discourage potential applicants from diverse backgrounds.
    Provide a list of suggestions for improvement. If the document is already well-written, please state that.

    Job Description:
    {jd_text}
    """
    response = get_groq_response(prompt)
    return response
