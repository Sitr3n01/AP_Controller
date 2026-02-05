# Guia Completo de Instalacao - SENTINEL

**GUIA PARA INICIANTES - Passo a Passo Detalhado**

Este guia assume que voce tem **ZERO experiencia** com desenvolvimento. Vamos do absoluto zero ate ter o sistema funcionando.

---

## Indice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalacao do Python](#instalacao-do-python)
3. [Instalacao do Node.js](#instalacao-do-nodejs)
4. [Instalacao do Git](#instalacao-do-git)
5. [Clone do Repositorio](#clone-do-repositorio)
6. [Configuracao do Backend](#configuracao-do-backend)
7. [Configuracao do Frontend](#configuracao-do-frontend)
8. [Configuracao de Variaveis de Ambiente](#configuracao-de-variaveis-de-ambiente)
9. [Inicializacao do Banco de Dados](#inicializacao-do-banco-de-dados)
10. [Executar o Sistema](#executar-o-sistema)
11. [Primeiro Acesso](#primeiro-acesso)
12. [Troubleshooting](#troubleshooting)
13. [Proximos Passos](#proximos-passos)

---

## Requisitos do Sistema

### Minimos
- **Sistema Operacional**: Windows 10+, macOS 10.14+, ou Linux (Ubuntu 20.04+)
- **RAM**: 4GB (recomendado 8GB)
- **Espaco em Disco**: 2GB livres
- **Conexao com Internet**: Para baixar dependencias

### Software Necessario
- Python 3.10 ou superior
- Node.js 18 ou superior
- Git
- Um editor de texto (recomendamos VS Code)

---

## 1. Instalacao do Python

### Windows

1. Acesse https://www.python.org/downloads/
2. Baixe o instalador do Python 3.11 ou superior
3. **IMPORTANTE**: Durante a instalacao, marque a opcao "Add Python to PATH"
4. Clique em "Install Now"
5. Aguarde a instalacao concluir

**Verificar instalacao**:
```bash
# Abra o Prompt de Comando (CMD) e execute:
python --version
# Deve mostrar algo como: Python 3.11.x

# Tambem verifique o pip:
pip --version
# Deve mostrar: pip 23.x.x
```

### macOS

**Usando Homebrew** (recomendado):
```bash
# Se nao tem Homebrew, instale primeiro:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale o Python:
brew install python@3.11

# Verifique:
python3 --version
pip3 --version
```

### Linux (Ubuntu/Debian)

```bash
# Atualize os pacotes:
sudo apt update

# Instale Python e pip:
sudo apt install python3.11 python3-pip python3-venv

# Verifique:
python3 --version
pip3 --version
```

---

## 2. Instalacao do Node.js

### Windows

1. Acesse https://nodejs.org/
2. Baixe a versao LTS (Long Term Support)
3. Execute o instalador
4. Aceite as opcoes padrao
5. Aguarde a instalacao

**Verificar**:
```bash
node --version
# Deve mostrar: v18.x.x ou superior

npm --version
# Deve mostrar: 9.x.x ou superior
```

### macOS

```bash
# Usando Homebrew:
brew install node

# Verifique:
node --version
npm --version
```

### Linux

```bash
# Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verifique:
node --version
npm --version
```

---

## 3. Instalacao do Git

### Windows

1. Acesse https://git-scm.com/download/win
2. Baixe o instalador
3. Execute e aceite as opcoes padrao
4. Aguarde a instalacao

**Verificar**:
```bash
git --version
# Deve mostrar: git version 2.x.x
```

### macOS

```bash
# Git ja vem pre-instalado, mas pode atualizar:
brew install git

git --version
```

### Linux

```bash
sudo apt install git

git --version
```

---

## 4. Clone do Repositorio

### Passo 4.1: Criar Pasta de Projetos

**Windows**:
```bash
# Abra o CMD e execute:
cd C:\Users\SeuUsuario\Documents
mkdir Projetos
cd Projetos
```

**macOS/Linux**:
```bash
cd ~
mkdir projetos
cd projetos
```

### Passo 4.2: Clonar o Repositorio

```bash
# Clone o repositorio:
git clone https://github.com/SEU_USUARIO/AP_Controller.git

# Entre na pasta:
cd AP_Controller

# Liste os arquivos para confirmar:
dir  # Windows
ls   # macOS/Linux
```

**Deve ver algo como**:
```
app/
frontend/
docs/
requirements.txt
README.md
...
```

---

## 5. Configuracao do Backend

### Passo 5.1: Criar Ambiente Virtual

**Windows**:
```bash
# Certifique-se de estar na pasta AP_Controller
cd C:\Users\SeuUsuario\Documents\Projetos\AP_Controller

# Crie o ambiente virtual:
python -m venv venv

# Ative o ambiente:
venv\Scripts\activate

# Seu prompt deve mudar para mostrar (venv)
```

**macOS/Linux**:
```bash
# Certifique-se de estar na pasta AP_Controller
cd ~/projetos/AP_Controller

# Crie o ambiente virtual:
python3 -m venv venv

# Ative o ambiente:
source venv/bin/activate

# Seu prompt deve mudar para mostrar (venv)
```

**IMPORTANTE**: Sempre ative o ambiente virtual antes de trabalhar no projeto!

### Passo 5.2: Instalar Dependencias do Backend

```bash
# Com o venv ativado, instale as dependencias:
pip install -r requirements.txt

# Isso vai demorar 2-5 minutos. Aguarde...
# Voce vera muitas linhas de texto instalando pacotes
```

**Verificar instalacao**:
```bash
# Verifique se o FastAPI foi instalado:
python -c "import fastapi; print(fastapi.__version__)"
# Deve mostrar: 0.115.x
```

---

## 6. Configuracao do Frontend

### Passo 6.1: Entrar na Pasta do Frontend

```bash
# A partir da pasta raiz do projeto:
cd frontend
```

### Passo 6.2: Instalar Dependencias do Frontend

```bash
# Instale as dependencias com npm:
npm install

# Isso vai demorar 3-7 minutos. Aguarde...
# Voce vera muitas linhas instalando pacotes
```

**O que acontece**:
- npm baixa todas as bibliotecas necessarias
- Cria uma pasta `node_modules/` (GRANDE - ~300MB)
- Isso e normal!

### Passo 6.3: Voltar para a Raiz

```bash
# Volte para a pasta raiz:
cd ..
```

---

## 7. Configuracao de Variaveis de Ambiente

### Passo 7.1: Criar arquivo .env

**Windows**:
```bash
# Na pasta raiz do projeto:
copy .env.example .env
```

**macOS/Linux**:
```bash
cp .env.example .env
```

### Passo 7.2: Editar o arquivo .env

Abra o arquivo `.env` com qualquer editor de texto (Notepad, VS Code, etc).

**Configuracao MINIMA para comecar**:

```bash
# ==============================================
# CONFIGURACAO ESSENCIAL
# ==============================================

# Aplicacao
APP_NAME=SENTINEL
APP_ENV=development
APP_DEBUG=True

# Seguranca (MUDE ISSO!)
SECRET_KEY=sua-chave-secreta-muito-forte-aqui-mude-isso
JWT_SECRET_KEY=outra-chave-secreta-diferente-mude-tambem

# Banco de Dados (SQLite para comecar)
DATABASE_URL=sqlite:///./data/sentinel.db

# API
API_V1_PREFIX=/api/v1
API_HOST=0.0.0.0
API_PORT=8000

# CORS (permite acesso do frontend)
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# ==============================================
# TELEGRAM (OPCIONAL - Configure depois)
# ==============================================
TELEGRAM_BOT_TOKEN=seu-token-aqui
TELEGRAM_CHAT_ID=seu-chat-id-aqui

# ==============================================
# EMAIL (OPCIONAL - Configure depois)
# ==============================================
EMAIL_PROVIDER=gmail
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app-aqui

# ==============================================
# OUTRAS CONFIGURACOES
# ==============================================
LOG_LEVEL=INFO
BACKUP_ENABLED=True
BACKUP_INTERVAL_HOURS=24
```

**IMPORTANTE - Geracao de Chaves Secretas**:

Execute este comando para gerar chaves seguras:

**Windows**:
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

**macOS/Linux**:
```bash
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Copie as chaves geradas e cole no `.env`.

---

## 8. Inicializacao do Banco de Dados

### Passo 8.1: Criar Pasta de Dados

```bash
# Crie a pasta data se nao existir:
mkdir data

# Windows:
if not exist "data" mkdir data

# macOS/Linux:
mkdir -p data
```

### Passo 8.2: Criar Tabelas do Banco

```bash
# Com o venv ativado, execute:
python -c "from app.database.session import create_all_tables; create_all_tables()"

# Deve mostrar algo como:
# INFO: Criando tabelas no banco de dados...
# INFO: Tabelas criadas com sucesso!
```

### Passo 8.3: Criar Usuario Administrador

```bash
# Execute o script de criacao de admin:
python scripts/create_default_admin.py

# Deve mostrar:
# INFO: Usuario admin criado com sucesso!
# Username: admin
# Password: Admin123!
# IMPORTANTE: Mude a senha apos o primeiro login!
```

**Credenciais padrao**:
- **Username**: `admin`
- **Password**: `Admin123!`
- **MUDE A SENHA IMEDIATAMENTE APOS O PRIMEIRO LOGIN!**

---

## 9. Executar o Sistema

Agora vamos iniciar o backend e o frontend!

### Passo 9.1: Abrir Dois Terminais

Voce precisa de **2 terminais abertos** ao mesmo tempo:
- Terminal 1: Backend (Python)
- Terminal 2: Frontend (Node.js)

### Passo 9.2: Iniciar o Backend

**Terminal 1**:

```bash
# Entre na pasta do projeto:
cd C:\Users\SeuUsuario\Documents\Projetos\AP_Controller  # Windows
cd ~/projetos/AP_Controller  # macOS/Linux

# Ative o ambiente virtual:
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Inicie o servidor:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Aguarde ate ver:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

**NAO FECHE ESTE TERMINAL!** Deixe rodando.

### Passo 9.3: Iniciar o Frontend

**Terminal 2** (novo terminal):

```bash
# Entre na pasta do projeto:
cd C:\Users\SeuUsuario\Documents\Projetos\AP_Controller  # Windows
cd ~/projetos/AP_Controller  # macOS/Linux

# Entre na pasta do frontend:
cd frontend

# Inicie o servidor de desenvolvimento:
npm run dev

# Aguarde ate ver algo como:
#   VITE v4.x.x  ready in XXX ms
#
#   ➜  Local:   http://localhost:5173/
#   ➜  Network: http://192.168.x.x:5173/
```

**NAO FECHE ESTE TERMINAL!** Deixe rodando.

---

## 10. Primeiro Acesso

### Passo 10.1: Acessar a Interface Web

1. Abra seu navegador (Chrome, Firefox, Edge)
2. Acesse: **http://localhost:5173**

Voce deve ver a tela de login do SENTINEL!

### Passo 10.2: Fazer Login

1. Digite o username: `admin`
2. Digite a senha: `Admin123!`
3. Clique em "Entrar"

Voce sera redirecionado para o dashboard!

### Passo 10.3: Acessar a Documentacao da API

A API possui documentacao interativa automatica:

1. Acesse: **http://localhost:8000/docs**
2. Voce vera a interface Swagger UI com todos os endpoints
3. Pode testar os endpoints diretamente na interface!

**Endpoints importantes**:
- `GET /health` - Verifica se a API esta funcionando
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/bookings/` - Listar reservas
- `GET /api/v1/properties/` - Listar imoveis

### Passo 10.4: MUDAR A SENHA DO ADMIN

**IMPORTANTE - FACA ISSO AGORA!**

1. No dashboard, va em "Perfil" ou "Configuracoes"
2. Clique em "Mudar Senha"
3. Digite a senha atual: `Admin123!`
4. Digite uma senha FORTE nova (minimo 8 caracteres, maiusculas, minusculas, numeros)
5. Salve

---

## 11. Troubleshooting

### Problema 1: "python nao e reconhecido"

**Solucao Windows**:
1. Verifique se Python foi adicionado ao PATH durante instalacao
2. Reinstale o Python e marque "Add Python to PATH"
3. Ou use `py` ao inves de `python`

**Solucao macOS/Linux**:
Use `python3` ao inves de `python`

---

### Problema 2: "pip nao e reconhecido"

**Solucao**:
```bash
# Windows:
python -m pip --version

# macOS/Linux:
python3 -m pip --version
```

Se ainda nao funcionar, reinstale o Python.

---

### Problema 3: "Erro ao ativar venv"

**Windows - Erro de Execution Policy**:
```bash
# Execute como Administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Tente ativar novamente:
venv\Scripts\activate
```

---

### Problema 4: "ModuleNotFoundError: No module named 'fastapi'"

**Causa**: Dependencias nao instaladas ou venv nao ativado

**Solucao**:
```bash
# Certifique-se de ativar o venv:
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstale as dependencias:
pip install -r requirements.txt
```

---

### Problema 5: "Port 8000 already in use"

**Causa**: Outra aplicacao usando a porta 8000

**Solucao**:
```bash
# Use outra porta:
uvicorn app.main:app --reload --port 8001

# Depois atualize o frontend para usar a nova porta
# (edite vite.config.js ou use variavel de ambiente)
```

---

### Problema 6: "Cannot connect to backend"

**Verificacoes**:

1. Backend esta rodando?
```bash
# Acesse no navegador:
http://localhost:8000/health

# Deve retornar:
{"status": "healthy"}
```

2. CORS configurado?
```bash
# Verifique no .env:
CORS_ORIGINS=["http://localhost:5173"]
```

3. Firewall bloqueando?
```bash
# Windows: Permita Python no firewall
# macOS: System Preferences > Security > Firewall
```

---

### Problema 7: "Database locked"

**Causa**: SQLite sendo acessado por multiplos processos

**Solucao**:
```bash
# Feche TODOS os processos do backend
# Reinicie apenas 1 processo

# Se persistir:
rm data/sentinel.db
python -c "from app.database.session import create_all_tables; create_all_tables()"
python scripts/create_default_admin.py
```

---

### Problema 8: "npm install falhou"

**Solucoes**:

```bash
# Limpe o cache do npm:
npm cache clean --force

# Delete node_modules e tente novamente:
rm -rf node_modules package-lock.json  # macOS/Linux
rmdir /s node_modules && del package-lock.json  # Windows

npm install
```

---

### Problema 9: "Frontend nao carrega"

**Verificacoes**:

1. npm run dev esta rodando?
2. Navegador esta em http://localhost:5173?
3. Console do navegador (F12) mostra erros?

**Solucao**:
```bash
# Reinicie o frontend:
# Ctrl+C no terminal do frontend
npm run dev
```

---

## 12. Proximos Passos

Parabens! Voce tem o SENTINEL rodando!

### Passo 1: Explorar o Sistema

1. **Criar um Imovel**:
   - Va em "Imoveis" > "Novo Imovel"
   - Preencha os dados
   - Salve

2. **Criar uma Reserva**:
   - Va em "Reservas" > "Nova Reserva"
   - Selecione o imovel
   - Preencha datas e dados do hospede
   - Salve

3. **Verificar Dashboard**:
   - Va em "Dashboard"
   - Veja estatisticas de ocupacao
   - Veja calendario de reservas

### Passo 2: Configurar Integracao com Airbnb/Booking

Leia: [Guia de Integracao de Calendarios](../architecture/INTEGRACAO_CALENDARIOS.md)

### Passo 3: Configurar Bot Telegram

Leia: [Guia do Telegram Bot](GUIA_TELEGRAM.md)

### Passo 4: Configurar Email

Leia o arquivo `.env` para configurar email SMTP/IMAP

### Passo 5: Gerar Documentos

1. Va em "Documentos" > "Gerar Autorizacao"
2. Selecione uma reserva
3. Clique em "Gerar"
4. Faca download do documento .docx

---

## 13. Comandos Uteis

### Parar o Sistema

**Backend** (Terminal 1):
```bash
# Pressione Ctrl+C
```

**Frontend** (Terminal 2):
```bash
# Pressione Ctrl+C
```

### Reiniciar o Sistema

Siga os passos 9.2 e 9.3 novamente.

### Atualizar Dependencias

```bash
# Backend:
pip install -r requirements.txt --upgrade

# Frontend:
cd frontend
npm update
```

### Ver Logs

**Backend**:
```bash
# Logs aparecem no terminal onde uvicorn esta rodando
# Ou veja os arquivos em:
tail -f data/logs/app.log  # macOS/Linux
type data\logs\app.log  # Windows
```

**Frontend**:
```bash
# Logs aparecem no terminal onde npm run dev esta rodando
# Ou no console do navegador (F12)
```

### Backup do Banco de Dados

```bash
# Copie o arquivo SQLite:
cp data/sentinel.db data/sentinel.db.backup  # macOS/Linux
copy data\sentinel.db data\sentinel.db.backup  # Windows
```

### Resetar o Banco de Dados

```bash
# CUIDADO: Isso DELETA TODOS OS DADOS!
rm data/sentinel.db  # macOS/Linux
del data\sentinel.db  # Windows

# Recrie:
python -c "from app.database.session import create_all_tables; create_all_tables()"
python scripts/create_default_admin.py
```

---

## Resumo de Comandos

**Iniciar Backend**:
```bash
cd AP_Controller
venv\Scripts\activate  # ou source venv/bin/activate
uvicorn app.main:app --reload
```

**Iniciar Frontend**:
```bash
cd AP_Controller/frontend
npm run dev
```

**Acessar**:
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Backend: http://localhost:8000

---

## Obtendo Ajuda

### Documentacao
- [Documentacao Completa](../README.md)
- [Guia da API](GUIA_API.md)
- [Troubleshooting Avancado](GUIA_USO_DIARIO.md)

### Suporte
- GitHub Issues: [Abrir Issue](https://github.com/seu-usuario/AP_Controller/issues)
- Email: suporte@sentinel.com (exemplo)

---

## Conclusao

Voce concluiu a instalacao do SENTINEL! O sistema esta rodando localmente e pronto para uso.

**Proximos passos recomendados**:
1. Explore todas as funcionalidades
2. Configure integracoes (Airbnb, Telegram, Email)
3. Customize os templates de documentos
4. Leia a documentacao de seguranca antes de fazer deploy

**IMPORTANTE**: Este sistema possui vulnerabilidades de seguranca conhecidas. NAO faca deploy em producao sem corrigir as vulnerabilidades criticas listadas em [Auditoria de Seguranca](../security/AUDITORIA_SEGURANCA_DETALHADA.md).

---

**Boa sorte com o SENTINEL!**

**Atualizado**: 2026-02-04
**Versao do Guia**: 1.0.0
