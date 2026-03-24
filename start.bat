@echo off
REM SIMDCCO Quick Start Script (Windows)
REM This script sets up and runs both backend and frontend

echo.
echo ========================================
echo   SIMDCCO Quick Start
echo ========================================
echo.

REM Check if in correct directory
if not exist "backend" (
    echo ERROR: backend directory not found
    echo Please run this script from the SIMDCCO root directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: frontend directory not found
    echo Please run this script from the SIMDCCO root directory
    pause
    exit /b 1
)

echo [Step 1/3] Setting up Backend...
echo.

cd backend

REM Check if .env exists
if not exist ".env" (
    echo WARNING: No .env file found. Creating from example...
    copy .env.example .env
    echo.
    echo Please edit backend\.env with your PostgreSQL credentials
    echo Press any key after editing...
    pause
)

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo Initializing database and seeding data...
python seed.py

echo.
echo Starting backend server...
start "SIMDCCO Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

cd ..

echo.
echo [Step 2/3] Setting up Frontend...
echo.

cd frontend

REM Check if .env.local exists
if not exist ".env.local" (
    echo Creating .env.local...
    copy .env.local.example .env.local
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

echo.
echo Starting frontend development server...
start "SIMDCCO Frontend" cmd /k "npm run dev"

cd ..

echo.
echo ========================================
echo   SIMDCCO is now running!
echo ========================================
echo.
echo URLs:
echo   * Frontend: http://localhost:3000
echo   * Backend:  http://localhost:8000
echo   * API Docs: http://localhost:8000/api/docs
echo.
echo Default Admin Credentials:
echo   * Email:    admin@simdcco.com
echo   * Password: admin123
echo   WARNING: Change password in production!
echo.
echo Next Steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Test the respondent flow
echo   3. Login to admin panel
echo.
echo Two terminal windows have been opened.
echo Close them to stop the servers.
echo.
pause
