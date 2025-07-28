import streamlit as st
import requests
import os
import json
import pandas as pd
from datetime import date

# ======================================================================================
# Page Configuration & Custom CSS
# ======================================================================================
st.set_page_config(
    page_title="Aura HR | AI Assistant",
    page_icon="✨",
    layout="wide"
)

# Inject custom CSS for a modern, polished dark-mode look
st.markdown("""
<style>
    /* Main app layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    
    /* Set default text color for the app to be light */
    body, .st-emotion-cache-16txtl3, .st-write, .st-markdown, .st-metric-label {
        color: #EAEAEA !important;
    }

    /* Center the main title */
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .title-container h1 {
        font-size: 3em;
        font-weight: 700;
        color: #FFFFFF; /* White title */
    }
    .title-container p {
        font-size: 1.1em;
        color: #A0A0A0; /* Light gray subtitle */
    }

    /* Card-like containers for each module */
    .module-container {
        background-color: #1E1E1E; /* Dark background for cards */
        border: 1px solid #3A3A3C; /* Subtle border */
        border-radius: 0.5rem;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        margin-bottom: 2rem;
    }

    /* Custom headers */
    h2 {
        font-size: 1.75em;
        font-weight: 600;
        color: #FFFFFF; /* White header */
        border-bottom: 2px solid #3A3A3C;
        padding-bottom: 0.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    h3 {
        font-size: 1.25em;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #FFFFFF; /* White sub-header */
    }

    /* Skill tags */
    .skill-tag { display: inline-block; padding: 0.3em 0.8em; font-size: 0.85em; font-weight: 500; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 1rem; margin: 0.2rem; }
    .matching-skill { color: #D4EDDA; background-color: #155724; border: 1px solid #28a745; }
    .missing-skill { color: #F8D7DA; background-color: #721C24; border: 1px solid #dc3545; }

    /* Style Streamlit's buttons */
    .stButton>button {
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        color: white;
        background-color: #4B8BBE; /* A nice blue */
    }
    .stButton>button:hover {
        background-color: #3A6A94;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# Helper Functions
# ======================================================================================
BACKEND_URL = "http://127.0.0.1:8000"

def render_header(title, icon):
    """Renders a consistent header for each module."""
    st.markdown(f"<h2>{icon} {title}</h2>", unsafe_allow_html=True)

# ======================================================================================
# Page Rendering Functions (ALL MODULES INCLUDED)
# ======================================================================================

def show_dashboard():
    render_header("Analytics Dashboard", "📊")
    st.write("Get real-time insights into your HR processes and application usage.")
    
    response = requests.get(f"{BACKEND_URL}/getanalytics")
    if response.status_code == 200:
        data = response.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Resumes Screened", data.get("total_screenings", 0))
        col2.metric("Average Fit Score", f"{data.get('avg_fit_score', 0)}%")
        col3.metric("Total JDs Generated", data.get("total_jds_generated", 0))

        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Average Fit Score by Role")
            avg_scores = data.get("avg_score_by_role", {})
            if avg_scores:
                df_scores = pd.DataFrame(list(avg_scores.items()), columns=['Role', 'Average Score'])
                st.bar_chart(df_scores.set_index('Role'))
            else:
                st.info("No resume screening data yet to display.")
        
        with c2:
            st.subheader("Most Common Policy Questions")
            common_questions = data.get("common_policy_questions", {})
            if common_questions:
                df_questions = pd.DataFrame(list(common_questions.items()), columns=['Question', 'Frequency'])
                st.table(df_questions)
            else:
                st.info("No policy questions have been asked yet.")
    else:
        st.error("Could not fetch analytics data from the backend.")

def show_ats_resume_screener():
    render_header("ATS Resume Screener", "📄")
    st.write("Perform a comprehensive analysis including ATS parsing and a fit score against a JD.")
    
    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="ats_resume")
    with col2:
        jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf", key="ats_jd")

    if st.button("Run Full Analysis"):
        if resume_file and jd_file:
            with st.spinner("Performing ATS Screening & Fit Analysis..."):
                files = {
                    "resume": (resume_file.name, resume_file.getvalue()),
                    "jd": (jd_file.name, jd_file.getvalue())
                }
                response = requests.post(f"{BACKEND_URL}/ats_fit_analysis", files=files)
                
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    data = response.json()

                    if data.get("error"):
                        st.error(data["error"])
                    else:
                        # --- Fit Analysis Section ---
                        fit_data = data.get("fit_analysis", {})
                        st.metric(label="Fit Score", value=f"{fit_data.get('fit_score', 0)}%")
                        
                        with st.expander("View Fit Analysis Details", expanded=True):
                            st.subheader("AI Summary")
                            st.write(fit_data.get("summary", "N/A"))
                            
                            st.subheader("Skills Match")
                            matching_skills_html = "".join([f'<span class="skill-tag matching-skill">{skill}</span>' for skill in fit_data.get("matching_skills", [])])
                            st.markdown("<h6>Matching Skills</h6>" + matching_skills_html if matching_skills_html else "No matching skills identified.", unsafe_allow_html=True)
                            
                            missing_skills_html = "".join([f'<span class="skill-tag missing-skill">{skill}</span>' for skill in fit_data.get("missing_skills", [])])
                            st.markdown("<h6>Missing Skills</h6>" + missing_skills_html if missing_skills_html else "No missing skills identified.", unsafe_allow_html=True)

                        st.markdown("---")

                        # --- ATS Parsing Section ---
                        ats_data = data.get("ats_parsing", {})
                        st.subheader("Detailed ATS Parsing")
                        with st.expander("View Full ATS Data"):
                            contact = ats_data.get("contact_info", {})
                            st.markdown(f"**Name:** {contact.get('name', 'N/A')} | **Email:** {contact.get('email', 'N/A')} | **Phone:** {contact.get('phone', 'N/A')}")

                            st.markdown("**Professional Summary**")
                            st.write(ats_data.get("professional_summary", "N/A"))
                            
                            st.markdown("**Work Experience**")
                            for job in ats_data.get("work_experience", []):
                                st.markdown(f"**{job.get('job_title')}** at {job.get('company')} ({job.get('start_date')} - {job.get('end_date')})")
                            
                            st.markdown("**Education**")
                            for edu in ats_data.get("education", []):
                                st.markdown(f"**{edu.get('degree')}**, {edu.get('institution')} ({edu.get('graduation_date')})")
                            
                            st.markdown("**Skills**")
                            st.write(", ".join(ats_data.get("skills", [])))
                else:
                    st.error(f"An error occurred: {response.status_code} - {response.text}")
        else:
            st.warning("Please upload both a resume and a job description.")

def show_jd_generator():
    render_header("Job Description Generator", "📝")
    st.write("Generate a professional job description with a specific tone and check for inclusive language.")
    
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""

    with st.form("jd_form"):
        role = st.text_input("Role Title")
        level = st.selectbox("Seniority Level", ["Entry-Level", "Mid-Level", "Senior", "Lead", "Manager"])
        tone = st.selectbox("Tone & Style", ["Professional/Corporate", "Startup/Casual", "Playful & Creative", "Formal & Academic"])
        skills = st.text_area("Key Skills (comma-separated)")
        
        submitted = st.form_submit_button("Generate JD")
        if submitted:
            if role and level and skills:
                with st.spinner("Generating JD..."):
                    data = {"role": role, "level": level, "skills": skills, "tone": tone}
                    response = requests.post(f"{BACKEND_URL}/jdgenerate", data=data)
                    if response.status_code == 200:
                        st.success("JD Generated!")
                        st.session_state.generated_jd = response.json()["result"]
                    else:
                        st.error(f"An error occurred: {response.text}")
            else:
                st.warning("Please fill in all fields.")

    if st.session_state.generated_jd:
        st.subheader("Generated Job Description")
        st.text_area("JD Output", st.session_state.generated_jd, height=400, key="jd_output")
        if st.button("Check for Inclusivity"):
            with st.spinner("Analyzing for inclusive language..."):
                response = requests.post(f"{BACKEND_URL}/checkinclusivity", data={"jd_text": st.session_state.generated_jd})
                if response.status_code == 200:
                    st.info("Inclusivity Analysis:")
                    st.markdown(response.json()["result"])
                else:
                    st.error("Could not perform inclusivity check.")

def show_candidate_summarizer():
    render_header("Candidate Summarizer", "✍️")
    st.write("Upload a resume to get a concise, one-paragraph summary for busy hiring managers.")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="summarizer")
    if st.button("Summarize Candidate"):
        if resume_file:
            with st.spinner("Summarizing..."):
                files = {"resume": (resume_file.name, resume_file.getvalue())}
                response = requests.post(f"{BACKEND_URL}/summarizecandidate", files=files)
                if response.status_code == 200:
                    st.success("Summary Generated!")
                    st.markdown(response.json()["result"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please upload a resume.")

def show_offer_letter_generator():
    render_header("Offer Letter Generator", "✉️")
    st.write("Fill in the details below to create a professional job offer letter.")
    
    with st.form("offer_letter_form"):
        st.subheader("Candidate & Role Details")
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("Candidate Name")
            job_title = st.text_input("Job Title")
            manager_name = st.text_input("Reporting Manager")
        with col2:
            salary = st.number_input("Annual Salary (USD)", min_value=0, step=1000)
            start_date = st.date_input("Start Date", min_value=date.today())
            expiration_date = st.date_input("Offer Expiration Date", min_value=date.today())

        submitted = st.form_submit_button("Generate Offer Letter")
        if submitted:
            if all([candidate_name, job_title, manager_name, salary, start_date, expiration_date]):
                with st.spinner("Drafting offer letter..."):
                    details = {
                        "candidate_name": candidate_name, "job_title": job_title, "manager_name": manager_name,
                        "salary": salary, "start_date": start_date.strftime("%B %d, %Y"),
                        "expiration_date": expiration_date.strftime("%B %d, %Y")
                    }
                    response = requests.post(f"{BACKEND_URL}/generateoffer", json=details)
                    if response.status_code == 200:
                        st.success("Offer Letter Generated!")
                        st.text_area("Generated Letter", response.json()['result'], height=500, key="offer_letter_output")
                    else:
                        st.error(f"An error occurred: {response.text}")
            else:
                st.warning("Please fill in all the details.")

def show_performance_review_assistant():
    render_header("Performance Review Assistant", "📈")
    st.write("Draft a structured and constructive performance review from your notes.")
    
    with st.form("performance_review_form"):
        employee_name = st.text_input("Employee Name")
        review_period = st.text_input("Review Period (e.g., 'Q3 2025')")
        points = st.text_area("Manager's Notes / Bullet Points", height=200, placeholder="- Exceeded sales targets by 20%\n- Needs to improve communication in team meetings\n- Successfully led the Project Phoenix initiative")
        
        submitted = st.form_submit_button("Generate Review")
        if submitted:
            if employee_name and review_period and points:
                with st.spinner("Drafting performance review..."):
                    data = {"employee_name": employee_name, "review_period": review_period, "points": points}
                    response = requests.post(f"{BACKEND_URL}/generateperformance", data=data)
                    if response.status_code == 200:
                        st.success("Review Generated!")
                        st.text_area("Generated Review", response.json()['result'], height=500, key="perf_review_output")
                    else:
                        st.error(f"An error occurred: {response.text}")
            else:
                st.warning("Please fill in all fields.")

def show_interview_generator():
    render_header("Interview Question Generator", "❓")
    st.write("Generate tailored interview questions from a job description.")
    jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf", key="interview_jd")
    if st.button("Generate Questions"):
        if jd_file:
            with st.spinner("Generating questions..."):
                files = {"jd": (jd_file.name, jd_file.getvalue())}
                response = requests.post(f"{BACKEND_URL}/interviewgenerate", files=files)
                if response.status_code == 200:
                    st.success("Questions Generated!")
                    st.markdown(response.json()["result"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please upload a job description.")

def show_policy_qa():
    render_header("Policy Q&A Assistant", "�")
    st.write("Get instant answers from your internal policy documents.")
    policy_doc = st.file_uploader("Upload Policy Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="policy_doc")
    question = st.text_input("Your Question about the Policy")
    if st.button("Get Answer"):
        if policy_doc and question:
            with st.spinner("Searching policy document..."):
                files = {"policy_doc": (policy_doc.name, policy_doc.getvalue())}
                data = {"question": question}
                response = requests.post(f"{BACKEND_URL}/policyqa", files=files, data=data)
                if response.status_code == 200:
                    st.success("Answer Found!")
                    st.markdown(response.json()["result"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please upload a policy document and ask a question.")

def show_onboarding_assistant():
    render_header("Onboarding Assistant", "👋")
    st.write("Provide new joiners with quick answers to their onboarding questions.")
    onboarding_guide = st.file_uploader("Upload Onboarding Guide (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="onboarding_guide")
    question = st.text_input("New Hire's Question")
    if st.button("Find Answer"):
        if onboarding_guide and question:
            with st.spinner("Searching onboarding guide..."):
                files = {"onboarding_guide": (onboarding_guide.name, onboarding_guide.getvalue())}
                data = {"question": question}
                response = requests.post(f"{BACKEND_URL}/onboardingqa", files=files, data=data)
                if response.status_code == 200:
                    st.success("Answer Found!")
                    st.markdown(response.json()["result"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please upload an onboarding guide and ask a question.")

def show_job_fit_analyzer():
    render_header("Job Fit Analyzer", "🔍")
    st.write("Compare a candidate's profile or bio to a job description.")
    candidate_profile = st.text_area("Candidate Bio/Profile", height=150)
    jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf", key="job_fit_jd")
    if st.button("Analyze Job Fit"):
        if candidate_profile and jd_file:
            with st.spinner("Analyzing fit..."):
                data = {"candidate_profile": candidate_profile}
                files = {"jd": (jd_file.name, jd_file.getvalue())}
                response = requests.post(f"{BACKEND_URL}/jobfit", data=data, files=files)
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    st.markdown(response.json()["result"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please provide a candidate profile and a job description.")


# ======================================================================================
# Main App Logic
# ======================================================================================

# --- Centered Title ---
st.markdown("""
<div class="title-container">
    <h1>✨ Aura HR Assistant</h1>
    <p>Your intelligent partner for streamlining HR workflows, from screening to analytics.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("✨ Aura HR")
    st.write("Navigation")
    
    PAGES = {
        "📊 Analytics Dashboard": show_dashboard,
        "📄 ATS Resume Screener": show_ats_resume_screener,
        "📝 JD Generator": show_jd_generator,
        "✍️ Candidate Summarizer": show_candidate_summarizer,
        "✉️ Offer Letter Generator": show_offer_letter_generator,
        "📈 Performance Review Assistant": show_performance_review_assistant,
        "❓ Interview Question Generator": show_interview_generator,
        "📘 Policy Q&A Assistant": show_policy_qa,
        "👋 Onboarding Assistant": show_onboarding_assistant,
        "🔍 Job Fit Analyzer": show_job_fit_analyzer,
    }
    
    selection = st.radio("Go to", list(PAGES.keys()))
    
    st.markdown("---")
    st.info("© 2025 Aura HR. All rights reserved.")

# --- Page Content ---
st.markdown('<div class="module-container">', unsafe_allow_html=True)
page_function = PAGES[selection]
page_function()
st.markdown('</div>', unsafe_allow_html=True)