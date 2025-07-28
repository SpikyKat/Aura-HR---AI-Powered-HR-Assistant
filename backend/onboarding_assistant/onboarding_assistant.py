from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF
import docx

def answer_onboarding_question(onboarding_guide_path, question):
    """
    Answers a new hire's question based on an onboarding guide.
    """
    try:
        if onboarding_guide_path.endswith(".pdf"):
            with fitz.open(onboarding_guide_path) as doc:
                guide_text = ""
                for page in doc:
                    guide_text += page.get_text()
        elif onboarding_guide_path.endswith(".docx"):
            doc = docx.Document(onboarding_guide_path)
            guide_text = "\n".join([para.text for para in doc.paragraphs])
        else:
            with open(onboarding_guide_path, 'r') as f:
                guide_text = f.read()

        prompt = f"""
        You are an Onboarding Assistant for new hires. Answer the following question based on the provided onboarding guide.
        Be friendly and helpful.

        Onboarding Guide:
        {guide_text}

        New Hire's Question:
        {question}
        """
        response = get_groq_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"
