@echo OFF
ECHO =================================================================
ECHO == LAUNCHING AURA HR CHATBOT                                   ==
ECHO =================================================================
ECHO.

REM Ensure the script runs from the project root directory
cd /d %~dp0

REM Activate the virtual environment
ECHO [1] Activating virtual environment...
call venv\Scripts\activate

REM Start the backend FastAPI server using Uvicorn from the root directory
ECHO [2] Starting FastAPI backend server...
start "Backend" cmd /k "uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait for a few seconds to allow the backend to initialize
timeout /t 5

REM Start the Streamlit chatbot application from the root directory
ECHO [3] Starting Streamlit chatbot frontend...
start "Chatbot Frontend" cmd /k "streamlit run frontend/chatbot.py"

ECHO.
ECHO Both servers have been started. The chatbot will be available shortly.