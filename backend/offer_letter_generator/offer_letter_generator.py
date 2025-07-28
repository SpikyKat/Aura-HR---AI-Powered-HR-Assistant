# VERIFICATION STEP 1: Ensure this file has this exact content.
from ..helpers.llm_helper import get_groq_response

def generate_offer_letter(details):
    """
    Generates a professional offer letter based on provided details.
    """
    prompt = f"""
    Please act as an HR professional and draft a formal job offer letter.
    Use the following details to construct the letter:

    - Company Name: "InnovateTech Solutions" (use this as a placeholder)
    - Candidate Name: {details['candidate_name']}
    - Job Title: {details['job_title']}
    - Start Date: {details['start_date']}
    - Annual Salary: ${details['salary']:,}
    - Reporting Manager: {details['manager_name']}
    - Offer Expiration Date: {details['expiration_date']}

    The letter should be professional, welcoming, and include standard sections such as:
    1.  Introduction and congratulations.
    2.  Position details (title, start date, manager).
    3.  Compensation details.
    4.  A brief mention of company benefits (e.g., "health insurance, paid time off, and a retirement savings plan").
    5.  At-will employment statement (if applicable in the US).
    6.  Next steps and a signature line for acceptance.

    Please return only the complete, formatted letter.
    """
    response = get_groq_response(prompt)
    return response