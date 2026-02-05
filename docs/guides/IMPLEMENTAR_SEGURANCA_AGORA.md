# 🔒 Implementar Segurança - Guia Rápido

## ✅ O QUE JÁ FOI CRIADO

Acabei de criar a base do sistema de segurança do SENTINEL:

### Arquivos Criados:
1. **`app/core/security.py`** - Funções de hash de senha e JWT
2. **`app/models/user.py`** - Model de usuário para autenticação
3. **`app/schemas/auth.py`** - Schemas Pydantic (validação de dados)
4. **`app/middleware/auth.py`** - Middleware de autenticação JWT
5. **`app/api/v1/auth.py`** - Endpoints de autenticação (login, registro, etc)
6. **`scripts/create_admin_user.py`** - Script para criar primeiro admin
7. **`app/config.py`** - Atualizado com configurações de segurança

### Funcionalidades Implementadas:
- ✅ Hash seguro de senhas (bcrypt)
- ✅ Tokens JWT (autenticação stateless)
- ✅ Validação forte de senhas
- ✅ Proteção de rotas por autenticação
- ✅ Diferentes níveis de permissão (user, admin)
- ✅ Endpoints: `/auth/register`, `/auth/login`, `/auth/me`, `/auth/change-password`

---

## 🚀 PRÓXIMOS PASSOS (Fazer AGORA)

### PASSO 1: Instalar Dependências (2 minutos)

```bash
# Ativar venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar novas dependências de segurança
pip install passlib[bcrypt] python-jose[cryptography] python-multipart

# Ou reinstalar tudo
pip install -r requirements.txt
```

---

### PASSO 2: Atualizar .env (1 minuto)

Adicione estas linhas ao seu arquivo `.env`:

```env
# === SEGURANÇA ===
SECRET_KEY=sua-chave-secreta-super-complexa-aqui-mude-isto-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === CORS ===
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# === RATE LIMITING ===
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

**⚠️ IMPORTANTE:** Gere uma SECRET_KEY forte! Use:

```python
# Gerar SECRET_KEY (rode no Python)
import secrets
print(secrets.token_urlsafe(32))
```

---

### PASSO 3: Criar Tabela de Usuários (1 minuto)

O banco SQLite precisa ter a tabela `users`. Vou criar um script de migration:

```python
# scripts/create_users_table.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models.user import User  # Importa model

print("Criando tabela de usuários...")
Base.metadata.create_all(bind=engine)
print("✅ Tabela 'users' criada com sucesso!")
```

Execute:
```bash
python scripts/create_users_table.py
```

---

### PASSO 4: Criar Primeiro Usuário Admin (2 minutos)

```bash
python scripts/create_admin_user.py
```

Preencha os dados:
- **Username:** admin (ou outro)
- **Email:** seu-email@example.com
- **Nome:** Seu Nome
- **Senha:** Senha123 (mínimo 8 chars, 1 maiúscula, 1 número)

---

### PASSO 5: Integrar Rotas no main.py (3 minutos)

Vou criar um arquivo para você adicionar ao `main.py`:

```python
# No app/main.py, adicionar:

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth  # NOVO

app = FastAPI(
    title="SENTINEL API",
    description="Sistema de Gestão de Apartamento",
    version="1.0.0"
)

# CORS Middleware (NOVO - segurança)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # URLs permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de autenticação (NOVO)
app.include_router(auth.router, prefix="/api/v1")

# ... suas outras rotas ...
```

---

### PASSO 6: Testar Autenticação (5 minutos)

#### 6.1 Iniciar o servidor
```bash
python -m uvicorn app.main:app --reload
```

#### 6.2 Acessar documentação
Abra: http://localhost:8000/docs

Você verá os novos endpoints:
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/change-password`

#### 6.3 Testar Login

**Pelo Swagger UI:**
1. Expanda `POST /api/v1/auth/login`
2. Click "Try it out"
3. Preencha:
   ```json
   {
     "username": "admin",
     "password": "Senha123"
   }
   ```
4. Click "Execute"
5. **Copie o `access_token`** da resposta

**Ou pelo curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Senha123"}'
```

#### 6.4 Testar Rota Protegida

1. No Swagger UI, click no botão **"Authorize"** (cadeado verde)
2. Cole o token (sem "Bearer ")
3. Click "Authorize"
4. Agora teste `GET /api/v1/auth/me`

**Ou pelo curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

Deve retornar seus dados de usuário!

---

## 🔒 PROTEGER ROTAS EXISTENTES

Agora que temos autenticação, vamos proteger as rotas de reservas, calendário, etc.

### Exemplo: Proteger rota de bookings

```python
# Antes (sem proteção):
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

@router.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    # Qualquer um pode acessar ❌
    return db.query(Booking).all()


# Depois (com proteção):
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_active_user  # NOVO
from app.models.user import User  # NOVO

@router.get("/bookings")
def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # NOVO
):
    # Só usuários autenticados podem acessar ✅
    return db.query(Booking).all()
```

### Proteger rota apenas para admins:

```python
from app.middleware.auth import get_current_admin_user

@router.delete("/bookings/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)  # Só admins
):
    # Só admins podem deletar ✅
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
    return {"message": "Deletado com sucesso"}
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Imediato (HOJE - 30 min)
- [ ] Instalar dependências (`pip install ...`)
- [ ] Adicionar SECRET_KEY ao `.env`
- [ ] Criar tabela de usuários
- [ ] Criar primeiro admin
- [ ] Integrar rotas no `main.py`
- [ ] Testar login no Swagger UI

### Curto Prazo (Esta Semana)
- [ ] Proteger rotas sensíveis (bookings, properties, etc)
- [ ] Atualizar frontend para usar JWT
- [ ] Criar página de login no React
- [ ] Salvar token no localStorage
- [ ] Incluir token em todas requests

### Médio Prazo (Próximas 2 Semanas)
- [ ] Implementar rate limiting (slowapi)
- [ ] Adicionar logs de auditoria
- [ ] Configurar HTTPS local
- [ ] Validação de input em todos endpoints
- [ ] Testes de segurança

---

## 🧪 TESTAR SEGURANÇA

### Teste 1: Token Inválido
```bash
# Deve retornar 401 Unauthorized
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer token-invalido"
```

### Teste 2: Sem Token
```bash
# Deve retornar 401/403
curl -X GET "http://localhost:8000/api/v1/auth/me"
```

### Teste 3: Usuário Inativo
```python
# No banco, desative um usuário:
# UPDATE users SET is_active = 0 WHERE id = 2;

# Tentar login deve retornar 403 Forbidden
```

### Teste 4: Senha Fraca
```bash
# Tentar registrar com senha fraca deve retornar 422
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@test.com","password":"123"}'

# Erro: "Senha deve ter no mínimo 8 caracteres"
```

---

## 🎯 RESULTADO ESPERADO

Após completar estes passos, você terá:

✅ Sistema de autenticação JWT funcional
✅ Validação forte de senhas
✅ Proteção de rotas por permissão
✅ Primeiro usuário admin criado
✅ CORS configurado corretamente
✅ Base para adicionar mais segurança (rate limiting, HTTPS, etc)

---

## ❓ PROBLEMAS COMUNS

### Erro: "ModuleNotFoundError: No module named 'passlib'"
**Solução:** Instale as dependências
```bash
pip install passlib[bcrypt] python-jose[cryptography]
```

### Erro: "SECRET_KEY not set"
**Solução:** Adicione SECRET_KEY ao `.env`

### Erro: "Table 'users' doesn't exist"
**Solução:** Execute `python scripts/create_users_table.py`

### Token sempre retorna 401
**Solução:** Verifique se:
1. Token foi copiado corretamente
2. Header é `Authorization: Bearer TOKEN`
3. SECRET_KEY é a mesma usada para gerar o token

---

## 📚 PRÓXIMA FASE

Depois que autenticação estiver funcionando:

1. **Rate Limiting** - Limitar requests por IP/usuário
2. **Logging de Auditoria** - Registrar todas as ações
3. **HTTPS Local** - Certificado SSL para desenvolvimento
4. **Validação Avançada** - SQL injection, XSS protection
5. **Backup Automático** - Cron job para backups

Tudo isso está documentado em `docs/IMPLEMENTAR_SEGURANCA.md` 📖

---

**Tempo estimado total:** 30-60 minutos
**Dificuldade:** Média
**Impacto:** Alto (sistema muito mais seguro)

**Vamos começar! Execute os passos acima e me avise se encontrar algum problema.** 🚀
