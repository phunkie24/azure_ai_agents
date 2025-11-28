@echo off
echo.
echo 🚀 Content Retrieval Agent - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
)

REM Start PostgreSQL
echo 🐘 Starting PostgreSQL with Docker...
docker-compose up -d

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

REM Run ingestion
echo 📊 Ingesting sample data...
python ingestion.py

echo.
echo ✅ Setup completed successfully!
echo.
echo Next steps:
echo 1. Start the API: python api.py
echo 2. Visit: http://localhost:8000/docs
echo 3. Test API: python test_api.py
echo.
pause
