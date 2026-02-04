@echo off
REM =====================================================
REM SENTINEL - Script para Iniciar Servidor FastAPI
REM =====================================================

echo.
echo ================================================
echo    SENTINEL - Starting API Server
echo ================================================
echo.

REM Verificar se está no diretório correto
if not exist "app\" (
    echo [ERRO] Script deve ser executado da raiz do projeto
    pause
    exit /b 1
)

REM Ativar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERRO] Virtual environment not found
    echo Run: scripts\setup_windows.bat
    pause
    exit /b 1
)

REM Verificar se .env existe
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    echo Copiando .env.template para .env...
    copy .env.template .env
    echo.
    echo ================================================
    echo  CONFIGURE O .env ANTES DE CONTINUAR!
    echo ================================================
    echo.
    notepad .env
    pause
)

echo.
echo Starting FastAPI server...
echo API will be available at: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.

REM Iniciar servidor FastAPI
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
