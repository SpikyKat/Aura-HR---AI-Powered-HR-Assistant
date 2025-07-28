@echo OFF
ECHO Starting the AI-Powered HR Assistant...

REM Ensure the script runs from the project root directory
cd /d %~dp0

REM Activate the virtual environment
ECHO Activating virtual environment...
call venv\Scripts\activate

REM Start the backend FastAPI server using Uvicorn from the root directory
ECHO Starting FastAPI backend server...
REM The command "backend.main:app" tells uvicorn where to find the FastAPI app instance
start "Backend" cmd /k "uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait for a few seconds to allow the backend to initialize
timeout /t 5

REM Start the frontend Streamlit application from the root directory
ECHO Starting Streamlit frontend...
start "Frontend" cmd /k "streamlit run frontend/app.py"

ECHO Both servers have been started.
