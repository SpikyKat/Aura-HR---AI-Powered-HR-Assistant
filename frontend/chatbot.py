import streamlit as st
import requests
import json
from datetime import date

# ======================================================================================
# Page Config & Initial State
# ======================================================================================
st.set_page_config(page_title="Aura HR Chatbot", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for the chatbot interface
st.markdown("""
<style>
    /* Clean up the main page */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    /* Hide the Streamlit header and footer */
    header, footer {
        visibility: hidden;
    }
    /* Style for the action buttons */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background-color: transparent;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        text-align: left;
    }
    .stButton>button:hover {
        border-color: #4B8BBE;
        color: #4B8BBE;
    }
    /* Style for the main "Start Over" button */
    .stButton>button[kind="secondary"] {
        background-color: #31333F;
        border: 1px solid #31333F;
    }
    .stButton>button[kind="secondary"]:hover {
        border-color: #4B8BBE;
    }
    /* Skill tags */
    .skill-tag { display: inline-block; padding: 0.3em 0.8em; font-size: 0.85em; font-weight: 500; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 1rem; margin: 0.2rem; }
    .matching-skill { color: #D4EDDA; background-color: #155724; border: 1px solid #28a745; }
    .missing-skill { color: #F8D7DA; background-color: #721C24; border: 1px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "role" not in st.session_state:
    st.session_state.role = None
if "current_action" not in st.session_state:
    st.session_state.current_action = None
if "welcome_message_shown" not in st.session_state:
    st.session_state.welcome_message_shown = False

# ======================================================================================
# Helper Functions
# ======================================================================================

def reset_app():
    """Resets the session state to go back to the role selection screen."""
    st.session_state.role = None
    st.session_state.current_action = None
    st.session_state.messages = []
    st.session_state.welcome_message_shown = False
    st.rerun()

def go_back_to_actions():
    """Resets the current action to show the action list again."""
    st.session_state.current_action = None
    # Add a message to confirm going back
    st.session_state.messages.append({"role": "assistant", "content": f"Ok, what would you like to do next?", "type": "text"})
    st.rerun()

def display_ats_fit_results(data):
    """Formats and displays the combined ATS and Fit Analysis data."""
    if data.get("error"):
        st.error(data["error"])
        return

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
    ats_data = data.get("ats_parsing", {})
    st.subheader("Detailed ATS Parsing")
    with st.expander("View Full ATS Data"):
        contact = ats_data.get("contact_info", {})
        st.markdown(f"**Name:** {contact.get('name', 'N/A')} | **Email:** {contact.get('email', 'N/A')} | **Phone:** {contact.get('phone', 'N/A')}")
        st.markdown("**Work Experience**")
        for job in ats_data.get("work_experience", []):
            st.markdown(f"**{job.get('job_title')}** at {job.get('company')}")

# ======================================================================================
# Action Handler Functions
# ======================================================================================

def handle_ats_screening():
    st.info("Please upload a resume and the corresponding job description.")
    col1, col2 = st.columns(2)
    resume_file = col1.file_uploader("Upload Resume (PDF)", type="pdf", key="ats_resume")
    jd_file = col2.file_uploader("Upload Job Description (PDF)", type="pdf", key="ats_jd")
    
    if st.button("Run Full Analysis"):
        if resume_file and jd_file:
            with st.spinner("Performing ATS Screening & Fit Analysis..."):
                files = {"resume": (resume_file.name, resume_file.getvalue()), "jd": (jd_file.name, jd_file.getvalue())}
                try:
                    response = requests.post(f"{BACKEND_URL}/ats_fit_analysis", files=files)
                    if response.status_code == 200:
                        st.session_state.messages.append({"role": "assistant", "content": response.json(), "type": "ats_fit_result"})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": f"Error: {response.text}", "type": "text"})
                except requests.exceptions.RequestException as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"Error connecting to backend: {e}", "type": "text"})
                
                st.session_state.current_action = None
                st.session_state.welcome_message_shown = True
                st.rerun()
        else:
            st.warning("Please upload both files.")

def handle_jd_generator():
    st.info("Fill in the details to create a new Job Description.")
    with st.form("jd_form"):
        role = st.text_input("Role Title")
        level = st.selectbox("Seniority Level", ["Entry-Level", "Mid-Level", "Senior", "Lead", "Manager"])
        tone = st.selectbox("Tone & Style", ["Professional/Corporate", "Startup/Casual", "Playful & Creative"])
        skills = st.text_area("Key Skills (comma-separated)")
        submitted = st.form_submit_button("Generate JD")
        if submitted and all([role, level, skills]):
            with st.spinner("Generating JD..."):
                # Backend call would go here
                st.success("JD Generated successfully! (This is a demo)")
                go_back_to_actions()

def handle_offer_letter_generator():
    st.info("Fill in the details to create a professional offer letter.")
    with st.form("offer_form"):
        candidate_name = st.text_input("Candidate Name")
        job_title = st.text_input("Job Title")
        salary = st.number_input("Annual Salary (USD)", min_value=30000, step=1000)
        submitted = st.form_submit_button("Generate Offer Letter")
        if submitted and all([candidate_name, job_title, salary]):
            with st.spinner("Generating Offer Letter..."):
                # Backend call would go here
                st.success("Offer Letter Generated! (This is a demo)")
                go_back_to_actions()

def handle_performance_review():
    st.info("Provide notes to draft a performance review.")
    with st.form("review_form"):
        employee_name = st.text_input("Employee Name")
        points = st.text_area("Manager's Notes / Bullet Points")
        submitted = st.form_submit_button("Generate Review")
        if submitted and all([employee_name, points]):
            with st.spinner("Generating Review..."):
                # Backend call would go here
                st.success("Performance Review Generated! (This is a demo)")
                go_back_to_actions()

def handle_policy_qa():
    st.info("Ask a question about a policy document.")
    doc = st.file_uploader("Upload Policy Document", type=['pdf', 'txt', 'docx'])
    question = st.text_input("Your Question")
    if st.button("Get Answer") and doc and question:
        with st.spinner("Searching..."):
            # Backend call would go here
            st.success("Answer found! (This is a demo)")
            go_back_to_actions()

# ======================================================================================
# Main Chat Interface Logic
# ======================================================================================

st.title("✨ Aura HR Chatbot")
if st.session_state.role:
    st.button("Start Over / Change Role", on_click=reset_app, type="secondary")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "ats_fit_result":
            display_ats_fit_results(message["content"])
        else:
            st.markdown(message["content"])

# --- Main Interaction Logic ---

if not st.session_state.current_action:
    if not st.session_state.role:
        if not st.session_state.welcome_message_shown:
            st.session_state.messages.append({"role": "assistant", "content": "Welcome to Aura HR! I'm here to help. First, please tell me your role.", "type": "text"})
            st.session_state.welcome_message_shown = True

        col1, col2 = st.columns(2)
        if col1.button("Recruiter"): st.session_state.role = "Recruiter"; st.rerun()
        if col1.button("Hiring Manager"): st.session_state.role = "Hiring Manager"; st.rerun()
        if col2.button("In-house Applicant"): st.session_state.role = "In-house Applicant"; st.rerun()
        if col2.button("External Applicant"): st.session_state.role = "External Applicant"; st.rerun()
    else:
        if not st.session_state.welcome_message_shown:
            st.session_state.messages.append({"role": "user", "content": f"I am a {st.session_state.role}.", "type": "text"})
            st.session_state.messages.append({"role": "assistant", "content": f"Great! As a {st.session_state.role}, here's what I can help you with:", "type": "text"})
            st.session_state.welcome_message_shown = True

        # Define actions for each role
        actions_map = {
            "Recruiter": {
                "📄 ATS Screening & Fit Analysis": handle_ats_screening,
                "📝 JD Generator": handle_jd_generator,
                "✉️ Offer Letter Generator": handle_offer_letter_generator,
            },
            "Hiring Manager": {
                "📄 ATS Screening & Fit Analysis": handle_ats_screening,
                "📈 Performance Review Assistant": handle_performance_review,
            },
            "In-house Applicant": {
                "📘 Policy Q&A": handle_policy_qa,
            },
            "External Applicant": {}
        }
        
        actions = actions_map.get(st.session_state.role, {})
        
        if not actions:
             st.info("No actions are currently configured for this role. Please start over to select a different role.")
        else:
            action_keys = list(actions.keys())
            cols = st.columns(2)
            for i, key in enumerate(action_keys):
                if cols[i % 2].button(key, key=f"action_{i}"):
                    st.session_state.current_action = actions[key]
                    st.session_state.messages.append({"role": "user", "content": f"I'd like to: {key}", "type": "text"})
                    st.rerun()
else:
    # If an action is in progress, execute its handler and show a back button
    st.session_state.current_action()
    if st.button("‹ Back to Actions"):
        go_back_to_actions()
