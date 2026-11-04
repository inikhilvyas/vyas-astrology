@echo off
setlocal
cd /d "%~dp0"
echo ===================================================
echo   Starting VYAS Vedic Astrology Platform...
echo ===================================================

:: Detect virtual environment
if exist "%~dp0.venv311\Scripts\activate.bat" (
    echo [OK] Using Python Virtual Environment (.venv311)
    call "%~dp0.venv311\Scripts\activate.bat"
) else if exist "%~dp0.venv\Scripts\activate.bat" (
    echo [OK] Using Python Virtual Environment (.venv)
    call "%~dp0.venv\Scripts\activate.bat"
) else (
    echo [INFO] Virtual environment not found, attempting system python...
)

echo App URL: http://localhost:8501
python -m streamlit run app.py --server.port 8501
if errorlevel 1 (
    echo.
    echo [ERROR] Streamlit failed to start.
    echo Please ensure dependencies are installed via: pip install -r requirements.txt
)
pause
