from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.responses import JSONResponse
import os
import shutil
from typing import Dict, Any

# Import feature modules
from .resume_screener.resume_screener import ats_and_fit_analysis # Import the new all-in-one function
from .jd_generator.jd_generator import generate_jd, check_inclusivity
from .interview_generator.interview_generator import generate_interview_questions
from .policy_assistant.policy_assistant import answer_policy_question
from .onboarding_assistant.onboarding_assistant import answer_onboarding_question
from .job_fit_analyzer.job_fit_analyzer import analyze_job_fit
from .candidate_summarizer.candidate_summarizer import summarize_candidate
from .offer_letter_generator.offer_letter_generator import generate_offer_letter
from .performance_review_assistant.performance_review_assistant import generate_performance_review
from .analytics_dashboard.analytics_dashboard import log_data, get_analytics_data

app = FastAPI()

# Create a temporary directory for file uploads
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- PRIMARY ATS & FIT ANALYSIS ENDPOINT ---
@app.post("/ats_fit_analysis")
async def ats_fit_analysis_endpoint(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)
    jd_path = os.path.join(UPLOAD_DIR, jd.filename)

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)
    
    result = ats_and_fit_analysis(resume_path, jd_path)
    
    # Log the fit score for analytics if it exists
    if result and "fit_analysis" in result and "fit_score" in result["fit_analysis"]:
        fit_score = result["fit_analysis"]["fit_score"]
        # Attempt to get role from parsed data, otherwise use 'Unknown'
        role = result.get("ats_parsing", {}).get("work_experience", [{}])[0].get("job_title", "Unknown Role")
        log_data("fit_score", {"role": role, "score": fit_score})
        
    return JSONResponse(content=result)


# --- OTHER ENDPOINTS ---

@app.post("/jdgenerate")
async def jd_generate_endpoint(role: str = Form(...), level: str = Form(...), skills: str = Form(...), tone: str = Form(...)):
    result = generate_jd(role, level, skills, tone)
    log_data("jd_generated", {})
    return JSONResponse(content={"result": result})

@app.post("/policyqa")
async def policy_qa_endpoint(policy_doc: UploadFile = File(...), question: str = Form(...)):
    policy_doc_path = os.path.join(UPLOAD_DIR, policy_doc.filename)
    with open(policy_doc_path, "wb") as buffer:
        shutil.copyfileobj(policy_doc.file, buffer)
    log_data("policy_question", question)
    result = answer_policy_question(policy_doc_path, question)
    return JSONResponse(content={"result": result})

@app.post("/generateoffer")
async def generate_offer_endpoint(details: Dict[str, Any] = Body(...)):
    result = generate_offer_letter(details)
    return JSONResponse(content={"result": result})

@app.post("/generateperformance")
async def generate_performance_endpoint(points: str = Form(...), employee_name: str = Form(...), review_period: str = Form(...)):
    result = generate_performance_review(points, employee_name, review_period)
    return JSONResponse(content={"result": result})

@app.get("/getanalytics")
async def get_analytics_endpoint():
    data = get_analytics_data()
    return JSONResponse(content=data)

@app.post("/checkinclusivity")
async def check_inclusivity_endpoint(jd_text: str = Form(...)):
    result = check_inclusivity(jd_text)
    return JSONResponse(content={"result": result})

@app.post("/interviewgenerate")
async def interview_generate_endpoint(jd: UploadFile = File(...)):
    jd_path = os.path.join(UPLOAD_DIR, jd.filename)
    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)
    result = generate_interview_questions(jd_path)
    return JSONResponse(content={"result": result})

@app.post("/onboardingqa")
async def onboarding_qa_endpoint(onboarding_guide: UploadFile = File(...), question: str = Form(...)):
    onboarding_guide_path = os.path.join(UPLOAD_DIR, onboarding_guide.filename)
    with open(onboarding_guide_path, "wb") as buffer:
        shutil.copyfileobj(onboarding_guide.file, buffer)
    result = answer_onboarding_question(onboarding_guide_path, question)
    return JSONResponse(content={"result": result})

@app.post("/jobfit")
async def job_fit_endpoint(candidate_profile: str = Form(...), jd: UploadFile = File(...)):
    jd_path = os.path.join(UPLOAD_DIR, jd.filename)
    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)
    result = analyze_job_fit(candidate_profile, jd_path)
    return JSONResponse(content={"result": result})

@app.post("/summarizecandidate")
async def summarize_candidate_endpoint(resume: UploadFile = File(...)):
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    result = summarize_candidate(resume_path)
    return JSONResponse(content={"result": result})

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered HR Assistant API"}
