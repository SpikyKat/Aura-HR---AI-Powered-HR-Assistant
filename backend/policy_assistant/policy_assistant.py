from ..helpers.llm_helper import get_groq_response
import fitz # PyMuPDF
import docx

def answer_policy_question(policy_doc_path, question):
    """
    Answers a question based on a policy document.
    """
    try:
        if policy_doc_path.endswith(".pdf"):
            with fitz.open(policy_doc_path) as doc:
                policy_text = ""
                for page in doc:
                    policy_text += page.get_text()
        elif policy_doc_path.endswith(".docx"):
            doc = docx.Document(policy_doc_path)
            policy_text = "\n".join([para.text for para in doc.paragraphs])
        else:
            with open(policy_doc_path, 'r') as f:
                policy_text = f.read()

        prompt = f"""
        You are an HR Policy Q&A Assistant. Answer the following question based *only* on the provided policy document.
        If the answer is not in the document, state that.

        Policy Document:
        {policy_text}

        Question:
        {question}
        """
        response = get_groq_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"
