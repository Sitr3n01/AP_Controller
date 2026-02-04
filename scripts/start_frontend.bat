@echo off
REM =====================================================
REM SENTINEL - Iniciar Frontend (React + Vite)
REM =====================================================

echo.
echo ================================================
echo    SENTINEL - Starting Frontend
echo ================================================
echo.

REM Verificar se está no diretório correto
if not exist "frontend\" (
    echo [ERRO] Script deve ser executado da raiz do projeto
    pause
    exit /b 1
)

REM Verificar se node_modules existe
if not exist "frontend\node_modules\" (
    echo [INFO] Dependencias nao instaladas. Instalando...
    cd frontend
    call npm install
    cd ..
)

echo.
echo Starting Vite dev server...
echo Frontend will be available at: http://localhost:5173
echo.

REM Iniciar servidor Vite
cd frontend
npm run dev

pause
