@echo off
REM =====================================================
REM SENTINEL - Iniciar Backend + Frontend
REM =====================================================

echo.
echo ================================================
echo    SENTINEL - Starting Full Stack
echo ================================================
echo.

REM Ativar ambiente virtual Python
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERRO] Virtual environment not found
    echo Run: scripts\setup_windows.bat
    pause
    exit /b 1
)

echo.
echo [1/2] Starting Backend API...
start "SENTINEL Backend" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM Aguardar 3 segundos para o backend iniciar
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "SENTINEL Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo  SENTINEL Started Successfully!
echo ================================================
echo.
echo Backend API: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to close this window (servers will continue running)
pause >nul
