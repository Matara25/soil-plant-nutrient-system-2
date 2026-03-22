@echo off
title Caiss Server Launcher
echo ===================================
echo Starting Caiss Application Servers...
echo.
echo [1/3] Starting Backend Server...
cd "d:\CLOUD BASED INTERGRATION\soil_project_backend-main\Matara & Aubrey\SOIL USER DATABASE"
start "Backend Server" cmd /k python app_advanced.py
timeout /t 2 >nul
echo.
echo [2/3] Starting Frontend Server...
cd "d:\CLOUD BASED INTERGRATION\SOIL AND PLANT NUTRIENT FRONTEND"
start "Frontend Server" cmd /k python -m http.server 8000
timeout /t 2 >nul
echo.
echo [3/3] Both servers started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Press any key to open browser...
pause >nul
start http://localhost:8000
