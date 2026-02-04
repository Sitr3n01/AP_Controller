@echo off
echo ========================================
echo  SENTINEL - Limpeza do Projeto
echo ========================================
echo.

cd "%~dp0"

echo [1/5] Removendo pasta app/interfaces/ (duplicada)...
if exist "app\interfaces" (
    rmdir /s /q "app\interfaces"
    echo    ✓ app/interfaces/ removida
) else (
    echo    → app/interfaces/ já não existe
)

echo.
echo [2/5] Removendo arquivos temporários...
del /s /q *.pyc 2>nul
del /s /q *.tmp 2>nul
del /s /q *.bak 2>nul
del /s /q *.log 2>nul
echo    ✓ Arquivos temporários removidos

echo.
echo [3/5] Removendo cache do Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo    ✓ __pycache__ removidos

echo.
echo [4/5] Verificando estrutura...
echo    Pastas principais:
if exist "app" (echo    ✓ app/) else (echo    ✗ app/ NÃO ENCONTRADA!)
if exist "frontend" (echo    ✓ frontend/) else (echo    ✗ frontend/ NÃO ENCONTRADA!)
if exist "docs" (echo    ✓ docs/) else (echo    ✗ docs/ NÃO ENCONTRADA!)
if exist "data" (echo    ✓ data/) else (echo    ✗ data/ NÃO ENCONTRADA!)

echo.
echo [5/5] Criando backup do banco de dados...
if exist "data\sentinel.db" (
    if not exist "data\backups" mkdir "data\backups"
    copy "data\sentinel.db" "data\backups\sentinel_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db" >nul
    echo    ✓ Backup criado em data/backups/
) else (
    echo    → Nenhum banco de dados para backup
)

echo.
echo ========================================
echo  Limpeza Concluída!
echo ========================================
echo.
echo Ações realizadas:
echo  • Pasta app/interfaces/ removida (duplicada)
echo  • Arquivos temporários limpos
echo  • Cache do Python removido
echo  • Backup do DB criado (se existir)
echo.
echo Próximo passo: Configurar .env com dados reais
echo Veja: .env.example
echo.
pause
