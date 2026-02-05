# 🚀 Como Iniciar o Sistema SENTINEL

## Método 1: Inicialização Automática (RECOMENDADO)

### Passo Único:
1. Vá até a pasta do projeto:
   ```
   C:\Users\zegil\Documents\GitHub\AP_Controller
   ```

2. Dê duplo clique no arquivo:
   ```
   INICIAR_SISTEMA.bat
   ```

3. O script irá:
   - ✅ Verificar ambiente Python
   - ✅ Verificar banco de dados (cria se não existir)
   - ✅ Instalar dependências do frontend (se necessário)
   - ✅ Iniciar backend em uma janela
   - ✅ Iniciar frontend em outra janela
   - ✅ Abrir navegador automaticamente

**Pronto! O sistema estará rodando em:**
- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

---

## Método 2: Inicialização Manual

### 1. Abrir Terminal 1 - Backend

```batch
# Abrir CMD ou PowerShell
cd C:\Users\zegil\Documents\GitHub\AP_Controller

# Ativar ambiente virtual
venv\Scripts\activate

# Iniciar backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Abrir Terminal 2 - Frontend

```batch
# Abrir NOVO CMD ou PowerShell
cd C:\Users\zegil\Documents\GitHub\AP_Controller\frontend

# Instalar dependências (primeira vez)
npm install

# Iniciar frontend
npm run dev
```

### 3. Abrir Navegador
Acesse: http://localhost:5173

---

## 🛑 Como Parar o Sistema

### Se usou INICIAR_SISTEMA.bat:
- Feche as 2 janelas que foram abertas:
  - "SENTINEL - Backend API"
  - "SENTINEL - Frontend React"

### Se iniciou manualmente:
- Pressione `Ctrl + C` em cada terminal aberto

---

## ⚠️ Problemas Comuns

### "Node.js não encontrado"
**Solução:** Instale Node.js
1. Acesse: https://nodejs.org/
2. Baixe a versão LTS (18.x ou superior)
3. Instale e reinicie o terminal

### "Ambiente virtual não encontrado"
**Solução:** Execute o setup primeiro
```batch
scripts\setup_windows.bat
```

### "Banco de dados não encontrado"
**Solução:** Inicialize o banco
```batch
venv\Scripts\activate
python scripts\init_db.py
```

### "Porta 8000 já em uso"
**Solução:** Mate o processo anterior
```batch
# Encontrar processo na porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID pelo número encontrado)
taskkill /PID <numero> /F
```

### "Porta 5173 já em uso"
**Solução:** Mata o processo ou use outra porta
```batch
# Matar processo na porta 5173
npx kill-port 5173

# OU edite frontend/vite.config.js e mude a porta
```

---

## 📝 Primeira Configuração

Após iniciar o sistema pela primeira vez:

1. Acesse http://localhost:5173
2. Vá em **Configurações** (ícone de engrenagem na sidebar)
3. Na aba **Fácil**, configure:
   - Nome do imóvel
   - Endereço
   - URLs iCal do Airbnb e Booking
4. Clique em **Salvar Configurações**
5. Volte ao **Dashboard** para ver as estatísticas

---

## 🔄 Próximas Vezes

Depois da primeira configuração, basta:
1. Duplo clique em `INICIAR_SISTEMA.bat`
2. Aguardar as janelas abrirem
3. Acessar http://localhost:5173

---

## 📞 Precisa de Ajuda?

- Verifique os logs no terminal do backend
- Verifique o console do navegador (F12)
- Leia `docs/FRONTEND_GUIDE.md` para mais detalhes
- Leia `docs/STATUS_ATUAL.md` para ver o que está implementado

---

**Última atualização:** 04/02/2025
