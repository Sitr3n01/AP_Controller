# 🚀 Guia: Primeiro Upload para GitHub

## 📋 PRÉ-REQUISITOS

### 1. Git Instalado
```bash
# Verificar se Git está instalado
git --version

# Se não estiver, baixar em: https://git-scm.com/download/win
```

### 2. Conta no GitHub
- Acesse: https://github.com
- Faça login ou crie uma conta

### 3. Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. **Nome do repositório:** `sentinel-apartment-manager` (ou outro nome)
3. **Descrição:** Sistema de Gestão Automatizada de Apartamento
4. **Visibilidade:**
   - ⚠️  **PRIVATE** (RECOMENDADO) - Apenas você vê
   - ❌ Public - Qualquer pessoa vê (NÃO usar se tiver dados sensíveis)
5. **NÃO marcar:**
   - [ ] Add a README file
   - [ ] Add .gitignore
   - [ ] Choose a license
6. Clicar em **"Create repository"**

---

## 🔧 CONFIGURAÇÃO INICIAL (Apenas 1ª vez)

### 1. Configurar Git (se ainda não fez)
```bash
# Seu nome (aparece nos commits)
git config --global user.name "Seu Nome"

# Seu email (mesmo do GitHub)
git config --global user.email "seu-email@example.com"

# Verificar
git config --list
```

---

## 📦 COMANDOS PARA UPLOAD

### OPÇÃO A: Via Terminal Git Bash

Abra **Git Bash** na pasta do projeto:
```bash
# Navegar até a pasta (se necessário)
cd /c/Users/zegil/Documents/GitHub/AP_Controller

# 1. Inicializar repositório Git
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Criar primeiro commit
git commit -m "Initial commit: SENTINEL MVP1 - Sistema completo de gestão de apartamento

- Backend completo com FastAPI
- Frontend com React + Vite
- Dashboard e estatísticas com gráficos
- Bot do Telegram
- Sistema de calendário e conflitos
- Documentação completa
- Scripts de automação"

# 4. Renomear branch para 'main' (padrão do GitHub)
git branch -M main

# 5. Conectar com repositório remoto do GitHub
# ⚠️  SUBSTITUIR pela URL do seu repositório!
git remote add origin https://github.com/SEU_USUARIO/sentinel-apartment-manager.git

# 6. Enviar para o GitHub
git push -u origin main
```

### OPÇÃO B: Via CMD do Windows

Abra **CMD** ou **PowerShell** na pasta:
```cmd
# Navegar até a pasta
cd C:\Users\zegil\Documents\GitHub\AP_Controller

# 1. Inicializar repositório
git init

# 2. Adicionar arquivos
git add .

# 3. Commit inicial
git commit -m "Initial commit: SENTINEL MVP1 completo"

# 4. Branch main
git branch -M main

# 5. Conectar com GitHub (SUBSTITUIR URL!)
git remote add origin https://github.com/SEU_USUARIO/sentinel-apartment-manager.git

# 6. Push
git push -u origin main
```

---

## 🔐 AUTENTICAÇÃO NO GITHUB

Quando fizer `git push`, o GitHub pedirá autenticação:

### Método 1: Personal Access Token (RECOMENDADO)

1. **Gerar Token:**
   - Acesse: https://github.com/settings/tokens
   - Click em "Generate new token" → "Generate new token (classic)"
   - **Note:** "SENTINEL Access Token"
   - **Expiration:** 90 days (ou No expiration)
   - **Select scopes:** Marcar `repo` (acesso completo ao repositório)
   - Clicar em "Generate token"
   - **COPIAR O TOKEN** (aparece apenas uma vez!)

2. **Usar Token:**
   ```bash
   # Quando pedir senha, colar o TOKEN (não a senha da conta)
   Username: seu-usuario
   Password: ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  # Token
   ```

### Método 2: GitHub CLI (Alternativa)

```bash
# Instalar GitHub CLI: https://cli.github.com/

# Fazer login
gh auth login

# Seguir instruções interativas
# Escolher: HTTPS → Login with a web browser
```

### Método 3: SSH Keys (Avançado)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu-email@example.com"

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub

# Adicionar em: https://github.com/settings/keys
# Depois usar URL SSH:
git remote set-url origin git@github.com:SEU_USUARIO/sentinel-apartment-manager.git
```

---

## ⚠️  ANTES DO UPLOAD - CHECKLIST DE SEGURANÇA

### ✅ VERIFICAR (Muito Importante!)

```bash
# 1. Verificar que .env NÃO será enviado
git status

# Se .env aparecer na lista:
# ❌ PARAR! .env não deve ir para GitHub!
# ✅ Verificar que está no .gitignore

# 2. Ver o que será enviado
git status

# Deve mostrar:
# modified:   (arquivos modificados)
# new file:   (arquivos novos)
#
# NÃO deve mostrar:
# .env
# credentials.json
# token.json
# data/sentinel.db

# 3. Ver diferenças
git diff --cached
```

### 🔍 Arquivos que NÃO devem ir para GitHub:
- ❌ `.env` (senhas, tokens)
- ❌ `credentials.json` (credenciais)
- ❌ `token.json` (tokens OAuth)
- ❌ `data/sentinel.db` (banco de dados)
- ❌ `data/logs/*.log` (logs)
- ❌ `venv/` (virtual environment)
- ❌ `frontend/node_modules/` (dependências node)
- ❌ `__pycache__/` (cache Python)

### ✅ Arquivos que DEVEM ir:
- ✅ `.env.example` (exemplo sem dados reais)
- ✅ `.gitignore` (configurações Git)
- ✅ `app/` (código backend)
- ✅ `frontend/src/` (código frontend)
- ✅ `docs/` (documentação)
- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ Scripts `.bat`

---

## 📝 COMANDOS ÚTEIS

### Ver Status
```bash
# Ver arquivos modificados
git status

# Ver diferenças
git diff

# Ver histórico de commits
git log --oneline
```

### Adicionar Arquivos Específicos
```bash
# Adicionar apenas alguns arquivos
git add app/
git add frontend/src/
git add docs/
git add README.md

# Ou adicionar tudo (se .gitignore estiver correto)
git add .
```

### Desfazer (Se errar)
```bash
# Remover arquivo da staging area (antes do commit)
git reset HEAD arquivo.txt

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Desfazer tudo (CUIDADO!)
git reset --hard HEAD
```

### Atualizar .gitignore
```bash
# Se esqueceu algo no .gitignore:
echo ".env" >> .gitignore
echo "data/sentinel.db" >> .gitignore

# Remover arquivos já trackeados
git rm --cached .env
git rm --cached data/sentinel.db

# Commit
git add .gitignore
git commit -m "Update .gitignore"
git push
```

---

## 🎯 PASSO A PASSO COMPLETO

### 1. Preparação (5 min)
```bash
# Abrir Git Bash na pasta do projeto
cd /c/Users/zegil/Documents/GitHub/AP_Controller

# Verificar que está na pasta certa
pwd
ls
```

### 2. Inicializar Git (1 min)
```bash
git init
```

### 3. Verificar .gitignore (2 min)
```bash
# Ver conteúdo do .gitignore
cat .gitignore

# Deve conter pelo menos:
# .env
# venv/
# data/sentinel.db
# __pycache__/
# node_modules/
```

### 4. Adicionar Arquivos (1 min)
```bash
git add .
```

### 5. Verificar o que será enviado (2 min)
```bash
git status

# ❌ Se .env aparecer na lista:
# Parar e adicionar ao .gitignore!

# ✅ Se não aparecer:
# Prosseguir
```

### 6. Criar Commit (1 min)
```bash
git commit -m "Initial commit: SENTINEL MVP1 completo

Sistema de gestão automatizada de apartamento com:
- Backend FastAPI completo
- Frontend React + Vite
- Dashboard e estatísticas
- Bot do Telegram
- Calendário visual e conflitos
- Documentação completa"
```

### 7. Criar Repositório no GitHub (3 min)
- Acessar https://github.com/new
- Nome: `sentinel-apartment-manager`
- Visibilidade: **Private** ⚠️
- Clicar "Create repository"

### 8. Conectar com GitHub (1 min)
```bash
# SUBSTITUIR pela URL do seu repositório!
git remote add origin https://github.com/SEU_USUARIO/sentinel-apartment-manager.git

# Verificar
git remote -v
```

### 9. Enviar para GitHub (2 min)
```bash
git branch -M main
git push -u origin main

# Quando pedir credenciais:
# Username: seu-usuario
# Password: seu-token (não a senha!)
```

### 10. Verificar no GitHub (1 min)
- Acessar: https://github.com/SEU_USUARIO/sentinel-apartment-manager
- ✅ Arquivos devem estar lá
- ❌ .env NÃO deve aparecer

---

## 🔄 PRÓXIMOS UPLOADS (Depois do primeiro)

```bash
# 1. Ver mudanças
git status

# 2. Adicionar mudanças
git add .

# 3. Commit
git commit -m "Descrição das mudanças"

# 4. Enviar
git push
```

---

## 🆘 TROUBLESHOOTING

### Erro: "fatal: not a git repository"
```bash
# Solução: Inicializar Git
git init
```

### Erro: "fatal: remote origin already exists"
```bash
# Solução: Remover e adicionar novamente
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/seu-repo.git
```

### Erro: "Authentication failed"
```bash
# Solução: Usar Personal Access Token
# Gerar em: https://github.com/settings/tokens
# Usar token como senha
```

### Erro: "Updates were rejected"
```bash
# Solução: Pull primeiro
git pull origin main --allow-unrelated-histories
git push
```

### Erro: ".env foi enviado por engano!"
```bash
# URGENTE: Remover .env do GitHub

# 1. Remover do tracking
git rm --cached .env

# 2. Adicionar ao .gitignore
echo ".env" >> .gitignore

# 3. Commit
git add .gitignore
git commit -m "Remove .env from tracking"

# 4. Push
git push

# 5. IMPORTANTE: Trocar TODOS os tokens/senhas
# porque o .env ainda está no histórico!

# Para limpar histórico (avançado):
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

---

## 📊 ESTRUTURA QUE SERÁ ENVIADA

```
sentinel-apartment-manager/
├── app/                      ✅ Backend Python
├── frontend/
│   ├── src/                 ✅ Código React
│   ├── package.json         ✅
│   └── vite.config.js       ✅
├── docs/                     ✅ Documentação
├── scripts/                  ✅ Scripts utils
├── .env.example              ✅ Exemplo
├── .gitignore                ✅ Config Git
├── README.md                 ✅ README
├── requirements.txt          ✅ Dependências
├── INICIAR_SISTEMA.bat       ✅ Scripts
└── (outros arquivos...)      ✅

NÃO ENVIADOS (pelo .gitignore):
├── .env                      ❌ Secrets
├── venv/                     ❌ Virtual env
├── node_modules/             ❌ Node modules
├── data/sentinel.db          ❌ Banco de dados
├── __pycache__/              ❌ Cache
└── *.log                     ❌ Logs
```

---

## ✅ CHECKLIST FINAL

Antes de executar `git push`:

- [ ] Git está instalado (`git --version`)
- [ ] Repositório criado no GitHub
- [ ] Visibilidade: **Private** ⚠️
- [ ] `.gitignore` está correto
- [ ] `.env` NÃO está no `git status`
- [ ] `data/sentinel.db` NÃO está no `git status`
- [ ] `venv/` NÃO está no `git status`
- [ ] `node_modules/` NÃO está no `git status`
- [ ] Token do GitHub gerado (se necessário)
- [ ] Remote configurado (`git remote -v`)

---

## 🎉 SUCESSO!

Após o push bem-sucedido:

1. **Verificar no GitHub:**
   - https://github.com/SEU_USUARIO/sentinel-apartment-manager

2. **Próximos passos:**
   - Manter repositório privado
   - Fazer commits regulares
   - Nunca commitar .env

3. **Backup:**
   - Agora seu código está seguro no GitHub!
   - Pode clonar em outro computador
   - Histórico de versões preservado

---

**🎯 Repositório criado com sucesso!**

**Próximo upload:** `git add . && git commit -m "mensagem" && git push`
