@echo off
title Private Cloud ROI Calculator
echo.
echo  ==========================================
echo   Private Cloud ROI and TCO Calculator
echo   Built by Insight
echo  ==========================================
echo.

REM Check if Docker is running
docker info > nul 2>&1
if errorlevel 1 (
    echo  Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo  Waiting for Docker to start - 30 seconds...
    timeout /t 30 /nobreak > nul
)

REM Wait until Docker is ready
:waitloop
docker info > nul 2>&1
if errorlevel 1 (
    timeout /t 3 /nobreak > nul
    goto waitloop
)

echo  Docker is ready!
echo.

REM Navigate to app folder and build if first run
cd /d "%~dp0"

docker image inspect vcf-roi-calculator > nul 2>&1
if errorlevel 1 (
    echo  First run - building the app. This takes 3-5 minutes...
    docker compose build
)

REM Start the app
docker compose up -d

echo.
echo  App is running at http://localhost:8501
echo.
timeout /t 5 /nobreak > nul

REM Open browser
start http://localhost:8501

echo  Press any key to close this window. The app will keep running.
pause > nul
