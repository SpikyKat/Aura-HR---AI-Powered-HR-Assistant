✨ Aura HR - AI-Powered HR Assistant
Aura HR is a comprehensive, AI-powered platform designed to streamline and automate key human resources workflows. Built with a modern Python stack, it leverages the power of Large Language Models (via the Groq API) to provide intelligent assistance for tasks ranging from candidate screening to performance reviews.
The application features two distinct user interfaces: a traditional Dashboard UI for a quick overview and a conversational Chatbot UI that provides a role-based, guided experience for different types of users.

🌟 Key Features
Aura HR is composed of several powerful, independent modules accessible through both the dashboard and the chatbot interface.
📊 Analytics Dashboard: A central hub to visualize key metrics, such as the number of resumes screened, average fit scores by role, and the most frequently asked policy questions.
📄 ATS Resume Screener: A sophisticated tool that not only parses resumes like a modern Applicant Tracking System (ATS) but also analyzes them against a job description to provide a fit score, a summary, and a detailed skills match/gap analysis.
📝 Job Description Generator: Automatically generates professional and detailed job descriptions based on a role, seniority level, and required skills. It includes options for setting the tone and an inclusivity checker to ensure fair and unbiased language.
✍️ Candidate Summarizer: Quickly generates a concise, one-paragraph summary of a candidate's resume, perfect for busy hiring managers.
✉️ Offer Letter Generator: Creates formal and professional job offer letters from a simple form, standardizing the offer process.
📈 Performance Review Assistant: Helps managers overcome writer's block by drafting structured, constructive, and well-written performance reviews from a list of bullet points.
❓ Interview Question Generator: Generates a list of insightful interview questions tailored to a specific job description.
📘 Policy Q&A Assistant: Allows users to upload internal policy documents and ask questions to get instant, AI-powered answers.
👋 Onboarding Assistant: Helps new hires get up to speed by answering their questions based on an onboarding guide.
🔍 Job Fit Analyzer: A quick tool to compare a candidate's bio or short profile against a job description for a compatibility verdict.

🛠️ Tech Stack
| Layer | Technology / Library |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM API | Groq |
| PDF/DOCX | PyMuPDF, python-docx |
| Data | Pandas (for analytics processing) |
| Core Libs | Python 3.11, python-dotenv, requests |
🚀 Getting Started
Follow these steps to set up and run the project on your local machine.
1. Prerequisites
Python 3.9+
An API key from Groq
2. Installation
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name



Create and activate a Python virtual environment:
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate



Install the required dependencies:
pip install -r requirements.txt



Set up your environment variables:
Create a file named .env in the root of the project directory.
Add your Groq API key to this file:
GROQ_API_KEY="your_groq_api_key_here"



3. Running the Application
You can run either the traditional dashboard UI or the new chatbot UI.
To run the Dashboard UI:
# Execute the batch file
run_hr_assistant.bat


This will start the backend server and the Streamlit dashboard application.
To run the Chatbot UI:
# Execute the batch file
run_chatbot.bat


This will start the backend server and the Streamlit chatbot application.
The backend will be available at http://127.0.0.1:8000, and the frontend will open in your browser, typically at http://localhost:8501.
folder Structure

END_TO_END_HR_ASSISTANT_V1/
├── backend/
│   ├── analytics_dashboard/
│   ├── candidate_summarizer/
│   ├── helpers/
│   ├── interview_generator/
│   ├── jd_generator/
│   ├── job_fit_analyzer/
│   ├── offer_letter_generator/
│   ├── onboarding_assistant/
│   ├── performance_review_assistant/
│   ├── policy_assistant/
│   ├── resume_screener/
│   └── main.py
├── frontend/
│   ├── app.py         # The Dashboard UI
│   └── chatbot.py     # The Chatbot UI
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── run_chatbot.bat
└── run_hr_assistant.bat

