@echo off
echo.
echo 🚀 Content Retrieval Agent - No Docker Setup
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies (No Docker needed!)...
python -m pip install --upgrade pip
pip install -r requirements_no_docker.txt

REM Copy environment file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
)

REM Run ingestion with SQLite
echo 📊 Ingesting sample data into SQLite...
python ingestion_sqlite.py

echo.
echo ✅ Setup completed successfully!
echo.
echo 🎉 No Docker needed - everything runs locally with SQLite!
echo.
echo Next steps:
echo 1. Start the API: python api_sqlite.py
echo 2. Visit: http://localhost:8000/docs
echo 3. Test API: python test_api.py
echo.
echo Your data is stored in: marketing_content.db
echo.
pause
