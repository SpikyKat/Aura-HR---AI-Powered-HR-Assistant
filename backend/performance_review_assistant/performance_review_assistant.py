from ..helpers.llm_helper import get_groq_response

def generate_performance_review(points, employee_name, review_period):
    """
    Drafts a structured performance review from bullet points.
    """
    prompt = f"""
    Act as an experienced HR manager. Your task is to convert a list of bullet points into a well-structured, constructive, and professional performance review.

    Employee Name: {employee_name}
    Review Period: {review_period}

    Manager's Notes (Bullet Points):
    {points}

    Please structure the review with the following sections:
    1.  **Overall Summary:** A brief opening statement about the employee's performance during the review period.
    2.  **Strengths / Key Accomplishments:** Elaborate on the positive points provided. Use professional and encouraging language.
    3.  **Areas for Development:** Frame the negative points constructively. Focus on growth, opportunities for improvement, and actionable feedback rather than criticism.
    4.  **Goals for Next Period:** Suggest one or two forward-looking goals based on the feedback.
    5.  **Closing Remarks:** A concluding paragraph.

    The tone should be balanced, supportive, and professional.
    """
    response = get_groq_response(prompt)
    return response
