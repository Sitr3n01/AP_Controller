@echo off
echo ========================================
echo  SENTINEL - Upload para GitHub
echo ========================================
echo.

cd "%~dp0"

echo [PASSO 1] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git nao esta instalado!
    echo.
    echo Baixe em: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git instalado

echo.
echo [PASSO 2] Verificando arquivos sensiveis...
if exist ".env" (
    findstr /C:".env" .gitignore >nul
    if errorlevel 1 (
        echo ❌ ATENCAO! .env existe mas NAO esta no .gitignore!
        echo.
        echo Adicionando .env ao .gitignore...
        echo .env >> .gitignore
    ) else (
        echo ✓ .env protegido pelo .gitignore
    )
) else (
    echo ✓ .env nao existe (ok)
)

echo.
echo [PASSO 3] Status do repositorio...
git status >nul 2>&1
if errorlevel 1 (
    echo → Repositorio nao inicializado ainda
    echo.
    echo Deseja inicializar o repositorio Git agora? (S/N)
    set /p INIT="Resposta: "
    if /i "%INIT%"=="S" (
        git init
        echo ✓ Repositorio inicializado
    ) else (
        echo.
        echo Operacao cancelada.
        pause
        exit /b 0
    )
) else (
    echo ✓ Repositorio ja inicializado
)

echo.
echo [PASSO 4] Verificando remote...
git remote -v | findstr "origin" >nul 2>&1
if errorlevel 1 (
    echo → Remote 'origin' nao configurado
    echo.
    echo Cole a URL do seu repositorio GitHub:
    echo Exemplo: https://github.com/usuario/sentinel-apartment-manager.git
    echo.
    set /p REMOTE_URL="URL: "

    if not "%REMOTE_URL%"=="" (
        git remote add origin %REMOTE_URL%
        echo ✓ Remote configurado
    ) else (
        echo.
        echo Nenhuma URL fornecida. Configure manualmente:
        echo git remote add origin URL_DO_REPOSITORIO
        pause
        exit /b 1
    )
) else (
    echo ✓ Remote ja configurado:
    git remote -v | findstr "origin"
)

echo.
echo [PASSO 5] Adicionar arquivos...
git add .
echo ✓ Arquivos adicionados

echo.
echo [PASSO 6] Verificar o que sera enviado...
echo.
git status
echo.
echo ========================================
echo IMPORTANTE: Verifique se .env ou dados
echo sensiveis aparecem acima!
echo ========================================
echo.
pause

echo.
echo [PASSO 7] Criar commit...
echo.
echo Digite a mensagem do commit:
echo (ou pressione Enter para usar mensagem padrao)
set /p COMMIT_MSG="Mensagem: "

if "%COMMIT_MSG%"=="" (
    set "COMMIT_MSG=Update: Alteracoes no projeto SENTINEL"
)

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo.
    echo ❌ Erro ao criar commit
    echo.
    echo Possivel causa: Nenhuma alteracao para commitar
    pause
    exit /b 1
)
echo ✓ Commit criado

echo.
echo [PASSO 8] Enviar para GitHub...
echo.
echo Preparando para enviar...
echo Quando pedir credenciais:
echo   Username: seu-usuario-github
echo   Password: seu-token (NAO a senha da conta!)
echo.
pause

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Erro ao enviar para GitHub
    echo.
    echo Possiveies causas:
    echo 1. Credenciais incorretas
    echo 2. Remote URL incorreta
    echo 3. Sem permissao no repositorio
    echo.
    echo Para gerar token: https://github.com/settings/tokens
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✓ Upload concluido com sucesso!
echo ========================================
echo.
echo Seu codigo esta agora no GitHub!
echo.
echo Proximos uploads:
echo 1. git add .
echo 2. git commit -m "sua mensagem"
echo 3. git push
echo.
pause
