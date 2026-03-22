@echo off
echo Starting SoilDoctor Integrated Application...
echo.

echo [1/3] Starting Backend Server...
cd "d:\CLOUD BASED INTERGRATION\soil_project_backend-main\Matara & Aubrey\SOIL USER DATABASE"
start "Backend Server" python app_integrated.py

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend Server...
cd "d:\CLOUD BASED INTERGRATION\SOIL AND PLANT NUTRIENT FRONTEND"
start "Frontend Server" python -m http.server 8000

echo [3/3] Opening Application in Browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000

echo.
echo ========================================
echo SoilDoctor Application Started!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Demo Credentials:
echo Username: farmer
echo Password: soil123
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /f /im python.exe >nul 2>&1
echo Done!
