@echo off
REM run.bat - Start both backend and frontend servers (Windows)

echo.
echo ========================================================
echo  AI Language Tutor - Development Server Launcher
echo ========================================================
echo.

REM Check if MongoDB is running
echo Checking MongoDB...
mongosh --eval "db.version()" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: MongoDB is not running!
    echo Start MongoDB with: mongod
    echo.
    pause
    exit /b 1
)
echo [OK] MongoDB is running
echo.

REM Change to backend directory
cd backend

REM Check Python dependencies
echo Checking Python dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

REM Seed quizzes
echo.
echo Seeding quiz questions...
python -m app.scripts.seed_quizzes

REM Start backend
echo.
echo ========================================================
echo Starting Backend Server...
echo ========================================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

start "Backend Server" cmd /c "python -m uvicorn app.main:app --reload"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start frontend
cd ..\frontend

REM Check Node dependencies
if not exist node_modules (
    echo.
    echo Installing frontend dependencies...
    call npm install
)

echo.
echo ========================================================
echo Starting Frontend Server...
echo ========================================================
echo.
echo Frontend: http://localhost:5173
echo.
echo Both servers are now running!
echo.

start "Frontend Server" cmd /c "npm run dev"

echo.
echo ========================================================
echo SUCCESS: Both servers are running!
echo ========================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close the terminal windows to stop the servers.
echo.

pause
