@echo off
REM Start the uMap Data API server

echo Starting uMap Data API...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Copy example environment file if .env doesn't exist
if not exist ".env" (
    copy .env.example .env
    echo Created .env file from template
)

REM Run the application
echo Starting server on http://localhost:8000
python main.py