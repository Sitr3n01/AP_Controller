# 🚨 FASE 1: Segurança Urgente - FAZER ANTES DE VPS

## ⚠️ ATENÇÃO

**SEU SISTEMA ESTÁ 70% INSEGURO PARA PRODUÇÃO!**

Acabei de fazer uma auditoria completa. Veja o relatório em `docs/AUDITORIA_SEGURANCA_ATUAL.md`.

**Principais problemas:**
- 🔴 Rotas desprotegidas (qualquer um pode acessar/modificar dados)
- 🔴 HTTP sem criptografia (senhas visíveis na rede)
- 🔴 Sem rate limiting (vulnerável a ataques de força bruta)
- 🔴 SECRET_KEY default (tokens podem ser forjados)

**Tempo para corrigir:** 4-6 horas
**Prioridade:** CRÍTICA (não lançar sem isso)

---

## 🎯 TAREFAS URGENTES

### TAREFA 1: Instalar Dependências (2 minutos)

```bash
# Ativar venv
venv\Scripts\activate

# Instalar dependências de segurança
pip install passlib[bcrypt] python-jose[cryptography] python-multipart slowapi

# Verificar instalação
pip list | grep -E "passlib|jose|slowapi"
```

---

### TAREFA 2: Gerar SECRET_KEY Forte (1 minuto)

```bash
# Gerar chave
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar resultado e adicionar ao .env
```

Edite `.env` e adicione/atualize:
```env
# === SEGURANÇA ===
SECRET_KEY=COLE_A_CHAVE_GERADA_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === CORS ===
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# === RATE LIMITING ===
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

---

### TAREFA 3: Criar Tabela de Usuários (1 minuto)

```bash
python scripts/create_users_table.py
```

---

### TAREFA 4: Criar Primeiro Admin (2 minutos)

```bash
python scripts/create_admin_user.py
```

Preencha:
- **Username:** admin
- **Email:** seu-email@example.com
- **Senha:** SenhaForte123

---

### TAREFA 5: Integrar Autenticação no main.py (5 minutos)

Edite `app/main.py`:

**1. Importar módulos (no topo do arquivo):**
```python
from app.api.v1 import auth  # ADICIONAR
from slowapi import Limiter, _rate_limit_exceeded_handler  # ADICIONAR
from slowapi.util import get_remote_address  # ADICIONAR
from slowapi.errors import RateLimitExceeded  # ADICIONAR
```

**2. Configurar rate limiter (antes de criar app):**
```python
# Configurar rate limiting
limiter = Limiter(key_func=get_remote_address)
```

**3. Atualizar criação do app:**
```python
app = FastAPI(
    title="SENTINEL API",
    description="API para gerenciamento automatizado de apartamento",
    version="1.0.0",
    lifespan=lifespan
)

# Adicionar rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**4. Atualizar CORS (substituir bloco existente):**
```python
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # USAR SETTINGS
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # ESPECIFICAR
    allow_headers=["Authorization", "Content-Type"],  # ESPECIFICAR
)
```

**5. Incluir router de auth (após outros routers):**
```python
# Incluir routers
app.include_router(bookings.router)
app.include_router(conflicts.router)
app.include_router(statistics.router)
app.include_router(sync_actions.router)
app.include_router(calendar.router)
app.include_router(auth.router, prefix="/api/v1")  # ADICIONAR
```

---

### TAREFA 6: Proteger Rotas de Bookings (10 minutos)

Edite `app/routers/bookings.py`:

**1. Adicionar imports:**
```python
from app.middleware.auth import get_current_active_user, get_current_admin_user
from app.models.user import User
```

**2. Proteger TODAS as rotas:**

```python
# ANTES
@router.get("/", response_model=BookingListResponse)
def list_bookings(
    property_id: int = Query(...),
    db: Session = Depends(get_db)
):

# DEPOIS
@router.get("/", response_model=BookingListResponse)
def list_bookings(
    property_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # ADICIONAR
):
```

**3. Fazer o mesmo para TODAS as rotas em bookings.py**

Para rotas de DELETE, use `get_current_admin_user` (apenas admins):
```python
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)  # APENAS ADMINS
):
```

---

### TAREFA 7: Proteger Rotas de Conflicts (5 minutos)

Edite `app/routers/conflicts.py`:

Mesma lógica do bookings - adicionar `current_user: User = Depends(get_current_active_user)` em todas as rotas.

---

### TAREFA 8: Proteger Rotas de Statistics (5 minutos)

Edite `app/routers/statistics.py`:

Adicionar proteção em todas as rotas.

---

### TAREFA 9: Proteger Rotas de Calendar e Sync (5 minutos)

Edite `app/routers/calendar.py` e `app/routers/sync_actions.py`:

Adicionar proteção, especialmente em rotas que modificam dados (POST, PUT, DELETE).

---

### TAREFA 10: Adicionar Rate Limiting em Login (5 minutos)

Edite `app/api/v1/auth.py`:

**1. Importar:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request  # Adicionar
```

**2. Criar limiter:**
```python
limiter = Limiter(key_func=get_remote_address)
```

**3. Adicionar rate limit em login:**
```python
@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # ADICIONAR - apenas 5 tentativas por minuto
def login(
    request: Request,  # ADICIONAR
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    # ... resto do código
```

**4. Fazer o mesmo para register:**
```python
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")  # ADICIONAR
def register(
    request: Request,  # ADICIONAR
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # ... resto do código
```

---

### TAREFA 11: Testar (10 minutos)

```bash
# Iniciar servidor
python -m uvicorn app.main:app --reload
```

**1. Acessar Swagger UI:**
http://localhost:8000/docs

**2. Testar login:**
- Ir em `POST /api/v1/auth/login`
- Click "Try it out"
- Username: `admin`
- Password: `SenhaForte123`
- Click "Execute"
- **Copiar o `access_token`**

**3. Autorizar no Swagger:**
- Click no botão verde "Authorize" (cadeado)
- Colar o token
- Click "Authorize"

**4. Testar rota protegida:**
- Ir em `GET /api/bookings/`
- Deve funcionar COM token
- Remover autorização e tentar de novo → deve retornar 401

**5. Testar rate limiting:**
- Logout do Swagger (desautorizar)
- Tentar fazer login 6 vezes seguidas
- Na 6ª tentativa deve retornar 429 "Too Many Requests"

---

## ✅ CHECKLIST DE CONCLUSÃO

- [ ] Dependências instaladas (passlib, jose, slowapi)
- [ ] SECRET_KEY gerada e no .env
- [ ] Tabela users criada
- [ ] Primeiro admin criado
- [ ] main.py atualizado com auth router
- [ ] CORS usando settings.cors_origins_list
- [ ] Rate limiter configurado
- [ ] Rotas de bookings protegidas
- [ ] Rotas de conflicts protegidas
- [ ] Rotas de statistics protegidas
- [ ] Rotas de calendar protegidas
- [ ] Rate limiting em login (5/min)
- [ ] Rate limiting em register (3/min)
- [ ] Login funciona e retorna token
- [ ] Rota sem token retorna 401
- [ ] 6ª tentativa de login retorna 429

---

## 🎯 RESULTADO ESPERADO

Após completar esta fase:

✅ **Segurança básica implementada**
✅ **Todas as rotas protegidas**
✅ **Rate limiting funcional**
✅ **Score: 60/100 → 75/100**

**Ainda falta:**
- HTTPS (fazer no VPS com Nginx + Let's Encrypt)
- Logs de auditoria
- Backups automáticos
- Validação completa de input

**Mas o sistema já estará SEGURO O SUFICIENTE para uso local/teste.**

Para VPS, ainda precisa HTTPS! Veja `docs/DEVOPS_INFRAESTRUTURA.md`.

---

## 📚 PRÓXIMOS PASSOS

Depois de completar Fase 1:

1. **Se vai lançar em VPS:** Seguir guia de HTTPS em `DEVOPS_INFRAESTRUTURA.md`
2. **Se vai continuar local:** Implementar Fase 2 (auditoria, backups)
3. **Testar com frontend:** Atualizar React para usar JWT

---

**Tempo total estimado:** 60-90 minutos
**Prioridade:** 🔴 URGENTE
**Bloqueador para VPS:** SIM

**Dúvidas? Consulte:**
- `docs/AUDITORIA_SEGURANCA_ATUAL.md` - Relatório completo
- `docs/IMPLEMENTAR_SEGURANCA.md` - Guia detalhado
- `IMPLEMENTAR_SEGURANCA_AGORA.md` - Guia passo a passo

**Bora começar! Primeira tarefa: instalar dependências** 🚀
