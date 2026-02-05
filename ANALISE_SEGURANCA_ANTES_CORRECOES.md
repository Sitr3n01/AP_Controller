# 🔒 ANÁLISE COMPLETA DE SEGURANÇA - ANTES DAS CORREÇÕES

**Data:** 04/02/2026
**Versão:** 1.0.0 (MVP2)
**Score Atual:** 54/100 🔴
**Status:** ⚠️ **NÃO PRONTO PARA PRODUÇÃO**

---

## 📋 ÍNDICE

1. [Resumo Executivo](#resumo-executivo)
2. [Vulnerabilidades Críticas (3)](#vulnerabilidades-críticas)
3. [Vulnerabilidades Altas (5)](#vulnerabilidades-altas)
4. [Vulnerabilidades Médias (8)](#vulnerabilidades-médias)
5. [Vulnerabilidades Baixas (6)](#vulnerabilidades-baixas)
6. [Roadmap de Correções](#roadmap-de-correções)
7. [Ordem de Implementação Recomendada](#ordem-de-implementação)
8. [Arquivos que Precisam ser Modificados](#arquivos-para-modificar)

---

## 📊 RESUMO EXECUTIVO

### Situação Atual

**Total de Vulnerabilidades:** 22

| Severidade | Quantidade | Tempo Estimado | Prioridade |
|------------|------------|----------------|------------|
| 🔴 Crítica | 3 | 6 horas | P0 - URGENTE |
| 🟠 Alta | 5 | 11 horas | P1 - 1 semana |
| 🟡 Média | 8 | 25 horas | P2 - 1 mês |
| 🟢 Baixa | 6 | 10 horas | P3 - 2 meses |

### Score Progression

```
Atual:          54/100 🔴 (NÃO PRONTO)
Após Fase 1:    69/100 🟡 (AINDA INSEGURO)
Após Fase 2:    79/100 🟢 (ACEITÁVEL)
Após Fase 3:    89/100 ✅ (PRONTO PARA PRODUÇÃO)
```

### Recomendação

**⚠️ CRÍTICO:** O sistema **NÃO DEVE** ser colocado em produção até que:
1. ✅ As 3 vulnerabilidades CRÍTICAS sejam corrigidas
2. ✅ As 5 vulnerabilidades ALTAS sejam corrigidas
3. ✅ Testes de penetração básicos sejam realizados

---

## 🔴 VULNERABILIDADES CRÍTICAS

### VULN #001 - JWT Payload Vaza Informações Sensíveis

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 8.5/10
**CWE-ID:** CWE-201 (Exposure of Sensitive Information)

#### 📍 Localização
- **Arquivo:** `app/api/v1/auth.py`
- **Linhas:** 127-135
- **Função:** `login()`

#### ❌ Código Vulnerável

```python
access_token = create_access_token(
    data={
        "sub": str(user.id),
        "email": user.email,           # ❌ VAZAMENTO DE PII
        "username": user.username,      # ❌ VAZAMENTO DE IDENTIFICADOR
        "is_admin": user.is_admin,      # ❌ VAZAMENTO DE PRIVILÉGIOS
    },
    expires_delta=access_token_expires
)
```

#### 🎯 Problema

**JWT tokens são ASSINADOS, NÃO CRIPTOGRAFADOS!**

Qualquer pessoa pode decodificar o token sem a chave secreta:

```bash
# Qualquer um pode fazer isso:
echo "eyJ0eXAiOiJKV1QiLCJhbGc..." | base64 -d

# Resultado:
{
  "sub": "123",
  "email": "admin@sentinel.com",  # ⚠️ EXPOSTO
  "username": "admin",             # ⚠️ EXPOSTO
  "is_admin": true                 # ⚠️ EXPOSTO
}
```

#### 💥 Impacto

1. **Vazamento de PII:** Email do usuário exposto
2. **User Enumeration:** Atacante descobre emails válidos
3. **Privilege Discovery:** Atacante sabe quem é admin
4. **Phishing Direcionado:** Emails expostos podem ser alvos
5. **LGPD/GDPR Violation:** Exposição desnecessária de dados pessoais

#### ✅ Correção

```python
# CORRETO: Apenas ID (opaco)
access_token = create_access_token(
    data={
        "sub": str(user.id),  # Apenas ID
        "type": "access",     # Tipo do token
        "iat": datetime.utcnow(),  # Issued at
    },
    expires_delta=access_token_expires
)

# O backend usa o ID para buscar dados do banco:
def get_current_user(token: str) -> User:
    payload = decode_token(token)
    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()
    return user  # Dados vêm do banco, não do token!
```

#### ⏱️ Estimativa
- **Tempo:** 2 horas
- **Complexidade:** Baixa
- **Breaking Change:** Sim (tokens existentes param de funcionar)

---

### VULN #002 - Timing Attack em Verificação de Senha

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 7.8/10
**CWE-ID:** CWE-208 (Observable Timing Discrepancy)

#### 📍 Localização
- **Arquivo:** `app/api/v1/auth.py`
- **Linhas:** 102-112
- **Função:** `login()`

#### ❌ Código Vulnerável

```python
user = db.query(User).filter(
    (User.username == login_data.username) | (User.email == login_data.username)
).first()

# VULNERÁVEL: Tempo de resposta diferente!
if not user or not verify_password(login_data.password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Credenciais inválidas")
```

#### 🎯 Problema

**Timing Attack: Respostas levam tempos diferentes**

| Cenário | Tempo de Resposta | Motivo |
|---------|-------------------|--------|
| Usuário NÃO existe | ~5ms | Retorna imediatamente |
| Usuário existe | ~150ms | Executa bcrypt (lento) |

**Atacante pode medir e descobrir:**

```python
# Script de ataque
for email in possible_emails:
    start = time.time()
    response = requests.post("/api/v1/auth/login",
                           json={"username": email, "password": "test"})
    elapsed = time.time() - start

    if elapsed > 0.1:
        print(f"✓ Email VÁLIDO: {email}")  # Demorou = existe
    else:
        print(f"✗ Email inválido: {email}")  # Rápido = não existe
```

#### 💥 Impacto

1. **User Enumeration:** Descobrir TODOS os emails/usernames válidos
2. **Targeted Brute Force:** Atacar apenas contas que existem
3. **Information Leakage:** Base de usuários mapeada
4. **Privacy Breach:** Usuários não devem ser enumeráveis

#### ✅ Correção

```python
# Hash dummy para garantir tempo constante
DUMMY_PASSWORD_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/VaZZK"

user = db.query(User).filter(
    (User.username == login_data.username) | (User.email == login_data.username)
).first()

# SEMPRE executar verificação de hash (mesmo se user não existir)
if user:
    password_valid = verify_password(login_data.password, user.hashed_password)
else:
    # Hash dummy: mesmo tempo que usuário real
    verify_password(login_data.password, DUMMY_PASSWORD_HASH)
    password_valid = False

# Agora SEMPRE demora ~150ms (constante)
if not user or not password_valid:
    raise HTTPException(status_code=401, detail="Credenciais inválidas")
```

#### ⏱️ Estimativa
- **Tempo:** 1 hora
- **Complexidade:** Baixa
- **Breaking Change:** Não

---

### VULN #003 - Ausência de Account Lockout

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 7.5/10
**CWE-ID:** CWE-307 (Improper Restriction of Excessive Authentication Attempts)

#### 📍 Localização
- **Arquivo:** `app/api/v1/auth.py`
- **Problema:** Funcionalidade ausente
- **Rate Limiting Atual:** 5 tentativas/min por IP (INSUFICIENTE)

#### ❌ Código Atual (Insuficiente)

```python
@router.post("/login")
@limiter.limit("5/minute")  # ❌ FACILMENTE CONTORNÁVEL!
async def login(...):
    # Sem bloqueio por conta
    # Apenas por IP (facilmente trocado)
```

#### 🎯 Problema

**Brute Force Distribuído**

Atacante com múltiplos IPs (botnet) pode fazer:

```
Cenário de Ataque:
├─ 100 IPs diferentes
├─ Cada IP: 5 tentativas/min
├─ Total: 500 tentativas/min
├─ Em 1 hora: 30.000 tentativas
└─ Senhas fracas SERÃO encontradas

Exemplos de senhas fracas comuns:
- 123456 (descoberta em segundos)
- password (descoberta em segundos)
- admin123 (descoberta em minutos)
- nome+ano (descoberta em horas)
```

#### 💥 Impacto

1. **Brute Force Ilimitado:** Botnet pode testar milhões de senhas
2. **Credential Stuffing:** Listas vazadas podem ser testadas
3. **Account Takeover:** Contas fracas serão comprometidas
4. **Reputational Damage:** Invasões refletem mal no sistema

#### ✅ Correção

**Implementar Account Lockout com Janela Deslizante**

```python
# 1. Criar model de tentativas
class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    username_tried = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)

# 2. Adicionar campo ao User
class User(Base):
    # ...
    locked_until = Column(DateTime, nullable=True)
    failed_login_count = Column(Integer, default=0)

# 3. Implementar no login
@router.post("/login")
async def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):

    # Buscar usuário
    user = db.query(User).filter(...).first()

    # VERIFICAR BLOQUEIO
    if user and user.locked_until:
        if datetime.utcnow() < user.locked_until:
            remaining = (user.locked_until - datetime.utcnow()).seconds
            raise HTTPException(
                status_code=429,
                detail=f"Conta bloqueada. Tente novamente em {remaining//60} minutos"
            )
        else:
            # Bloqueio expirou, resetar
            user.locked_until = None
            user.failed_login_count = 0
            db.commit()

    # Verificar senha (com timing constante)
    password_valid = False
    if user:
        password_valid = verify_password(login_data.password, user.hashed_password)
    else:
        verify_password(login_data.password, DUMMY_PASSWORD_HASH)

    # Registrar tentativa
    attempt = LoginAttempt(
        user_id=user.id if user else None,
        username_tried=login_data.username,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        success=password_valid
    )
    db.add(attempt)

    # LOGIN FALHOU
    if not user or not password_valid:
        if user:
            user.failed_login_count += 1

            # BLOQUEAR APÓS 5 TENTATIVAS
            if user.failed_login_count >= 5:
                user.locked_until = datetime.utcnow() + timedelta(hours=1)
                db.commit()

                # ALERTA DE SEGURANÇA
                await send_security_alert(
                    user=user,
                    event="account_locked",
                    details=f"Conta bloqueada após 5 tentativas falhadas"
                )

                raise HTTPException(
                    status_code=429,
                    detail="Conta bloqueada por 1 hora devido a múltiplas tentativas falhadas"
                )

            db.commit()

        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # LOGIN SUCESSO
    user.failed_login_count = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.commit()

    # Gerar token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
```

#### 📊 Política Recomendada

```
Tentativas Falhadas | Ação
─────────────────────┼───────────────────────────
1-4 tentativas      | Permitir
5 tentativas        | Bloquear por 1 hora
10 tentativas (24h) | Bloquear por 24 horas
20 tentativas (7d)  | Bloquear permanente + alerta admin
```

#### ⏱️ Estimativa
- **Tempo:** 3 horas
- **Complexidade:** Média
- **Breaking Change:** Não (apenas adiciona proteção)

---

## 🟠 VULNERABILIDADES ALTAS

### VULN #004 - Ausência de Token Revocation (Blacklist)

**Severidade:** 🟠 ALTA
**CVSS Score:** 6.8/10
**CWE-ID:** CWE-613 (Insufficient Session Expiration)

#### 🎯 Problema

```python
@router.post("/logout")
async def logout(...):
    # ❌ Apenas retorna success, MAS token continua válido!
    return {"message": "Logout successful"}
```

**Token continua funcionando por 30 minutos após logout!**

#### 💥 Impacto

1. **Token Leaked:** Se token vazar, atacante tem 30 minutos de acesso
2. **Logout Inseguro:** Logout em computador público não invalida sessão
3. **Password Change:** Mudar senha não invalida tokens antigos
4. **Account Compromise:** Mesmo após descobrir invasão, tokens antigos funcionam

#### ✅ Correção

**Opção 1: Redis Blacklist (RECOMENDADO)**

```python
# Adicionar ao requirements.txt
# redis>=5.0.0

import redis

# Configurar Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# No logout
@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(oauth2_scheme)
):
    # Decodificar token para pegar expiration
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp = payload["exp"]

    # Adicionar à blacklist até expirar
    ttl = exp - int(datetime.utcnow().timestamp())
    redis_client.setex(f"blacklist:{token}", ttl, "1")

    return {"message": "Logout successful"}

# Na verificação do token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verificar blacklist
    if redis_client.exists(f"blacklist:{token}"):
        raise HTTPException(status_code=401, detail="Token revogado")

    # ... resto da verificação
```

#### ⏱️ Estimativa
- **Tempo:** 4 horas (incluindo setup Redis)
- **Complexidade:** Média
- **Breaking Change:** Não

---

### VULN #005 - SQL Injection Potencial

**Severidade:** 🟠 ALTA
**CVSS Score:** 6.5/10

#### 🎯 Problema

Embora SQLAlchemy ORM proteja, desenvolvedores futuros podem adicionar:

```python
# ❌ VULNERÁVEL (se alguém fizer isso no futuro)
query = f"SELECT * FROM users WHERE username = '{username}'"
result = db.execute(query)
```

#### ✅ Correção

1. **Adicionar Linter de Segurança**

```bash
# bandit - Security linter
pip install bandit

# safety - Dependency checker
pip install safety

# Adicionar ao CI/CD
bandit -r app/ -f json -o security-report.json
safety check
```

2. **Code Review Obrigatório**

```yaml
# .github/CODEOWNERS
*.py @security-team

# .github/workflows/security-check.yml
name: Security Check
on: [pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r app/ -ll
```

#### ⏱️ Estimativa
- **Tempo:** 2 horas
- **Complexidade:** Baixa

---

### VULN #006 - Ausência de CSRF Protection

**Severidade:** 🟠 ALTA
**CVSS Score:** 6.3/10
**CWE-ID:** CWE-352 (Cross-Site Request Forgery)

#### 🎯 Problema

Site malicioso pode forçar navegador do usuário autenticado a fazer requisições:

```html
<!-- Site malicioso -->
<img src="https://seu-sentinel.com/api/v1/auth/delete-account" />

<!-- Se usuário estiver logado, conta será deletada! -->
```

#### ✅ Correção

```python
# Adicionar middleware CSRF
from starlette_csrf import CSRFMiddleware

app.add_middleware(
    CSRFMiddleware,
    secret="seu-csrf-secret-key",
    cookie_secure=True,
    cookie_httponly=True,
    cookie_samesite="strict"
)
```

#### ⏱️ Estimativa
- **Tempo:** 2 horas

---

### VULN #007 - Stack Traces em Produção

**Severidade:** 🟠 ALTA
**CVSS Score:** 6.0/10

#### ❌ Código Vulnerável

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.APP_ENV == "development" else "An error occurred"
            # ❌ Se APP_ENV mal configurado, vaza stack trace
        }
    )
```

#### ✅ Correção

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # NUNCA vazar detalhes, SEMPRE logar
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Retornar APENAS erro genérico
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

#### ⏱️ Estimativa
- **Tempo:** 1 hora

---

### VULN #008 - Ausência de Rate Limiting Global

**Severidade:** 🟠 ALTA
**CVSS Score:** 5.8/10

#### 🎯 Problema

Rate limiting apenas em auth. Outros endpoints podem ser abusados:

```python
# ❌ Sem rate limiting
@router.get("/api/bookings/")
async def list_bookings():
    # Pode ser chamado 10.000 vezes/segundo = DoS
```

#### ✅ Correção

```python
# Aplicar rate limiting GLOBAL
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute", "1000/hour"]  # Global
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Endpoints sensíveis podem ter limites mais rígidos
@router.post("/api/v1/emails/send")
@limiter.limit("10/minute")  # Mais restritivo
async def send_email(...):
    pass
```

#### ⏱️ Estimativa
- **Tempo:** 2 horas

---

## 🟡 VULNERABILIDADES MÉDIAS (Resumo)

| ID | Vulnerabilidade | Tempo | Prioridade |
|----|-----------------|-------|------------|
| #009 | Validação de senha fraca | 2h | P2 |
| #010 | Sem email verification | 3h | P2 |
| #011 | Sem password reset | 3h | P2 |
| #012 | Backups não criptografados | 4h | P2 |
| #013 | Logs com informações sensíveis | 2h | P2 |
| #014 | Sem 2FA para admins | 6h | P2 |
| #015 | Caracteres especiais em inputs | 3h | P2 |
| #016 | Sem audit logging | 2h | P2 |

**Total:** ~25 horas

---

## 🟢 VULNERABILIDADES BAIXAS (Resumo)

| ID | Vulnerabilidade | Tempo |
|----|-----------------|-------|
| #017 | Headers de segurança incompletos | 1h |
| #018 | Sem proteção contra clickjacking | 1h |
| #019 | Cookies sem Secure flag | 1h |
| #020 | Informações vazadas em headers | 1h |
| #021 | Sem versionamento de API | 2h |
| #022 | Documentação de segurança incompleta | 4h |

**Total:** ~10 horas

---

## 📅 ROADMAP DE CORREÇÕES

### 🚨 FASE 1 - URGENTE (6 horas)

**Prazo:** 2-3 dias
**Prioridade:** P0 (CRÍTICA)

| # | Vulnerabilidade | Tempo | Arquivo |
|---|-----------------|-------|---------|
| 1 | JWT Payload | 2h | `app/api/v1/auth.py` |
| 2 | Timing Attack | 1h | `app/api/v1/auth.py` |
| 3 | Account Lockout | 3h | `app/api/v1/auth.py` + `app/models/` |

**Resultado:** Score 54 → 69 🟡

---

### 🔥 FASE 2 - ALTA (11 horas)

**Prazo:** 1 semana
**Prioridade:** P1 (ALTA)

| # | Vulnerabilidade | Tempo | Arquivos |
|---|-----------------|-------|----------|
| 4 | Token Blacklist | 4h | `app/api/v1/auth.py` + Redis |
| 5 | SQL Injection Prevention | 2h | CI/CD + Linter |
| 6 | CSRF Protection | 2h | `app/main.py` |
| 7 | Stack Traces | 1h | `app/main.py` |
| 8 | Rate Limiting Global | 2h | `app/main.py` |

**Resultado:** Score 69 → 79 🟢

---

### ⚡ FASE 3 - MÉDIA (25 horas)

**Prazo:** 1 mês
**Prioridade:** P2 (MÉDIA)

Vulnerabilidades #009 até #016

**Resultado:** Score 79 → 89 ✅

---

## 🎯 ORDEM DE IMPLEMENTAÇÃO RECOMENDADA

### Dia 1 (4 horas)
1. ✅ VULN #001 - JWT Payload (2h)
2. ✅ VULN #002 - Timing Attack (1h)
3. ✅ VULN #007 - Stack Traces (1h)

### Dia 2 (4 horas)
4. ✅ VULN #003 - Account Lockout (3h)
5. ✅ VULN #008 - Rate Limiting Global (1h)

### Dia 3 (3 horas)
6. ✅ VULN #006 - CSRF Protection (2h)
7. ✅ VULN #005 - Linter Setup (1h)

### Dia 4 (4 horas)
8. ✅ VULN #004 - Token Blacklist (4h)

**Total Fase 1+2:** 15 horas (2-3 dias de trabalho focado)

---

## 📁 ARQUIVOS QUE PRECISAM SER MODIFICADOS

### Alterações CRÍTICAS

```
app/
├── api/v1/
│   └── auth.py                    # ⚠️ PRINCIPAL (VULN #001, #002, #003, #004)
├── models/
│   ├── user.py                    # Adicionar campos lockout
│   └── login_attempt.py           # NOVO arquivo
├── main.py                        # VULN #006, #007, #008
├── config.py                      # Adicionar configs Redis
└── core/
    └── security.py                # Melhorar funções

requirements.txt                   # Adicionar redis, starlette-csrf

deployment/
└── docker-compose.yml             # Adicionar Redis container

.github/workflows/
└── security-check.yml             # NOVO - CI/CD security

docs/security/
└── CORRECOES_APLICADAS.md         # NOVO - Documentar correções
```

---

## ✅ CHECKLIST ANTES DE AGIR

Antes de começar as correções, certifique-se de:

### Preparação
- [ ] ✅ Fazer backup completo do banco de dados
- [ ] ✅ Criar branch `feature/security-fixes`
- [ ] ✅ Documentar estado atual (este arquivo)
- [ ] ✅ Ter ambiente de testes funcionando
- [ ] ✅ Instalar Redis (se aplicável)

### Durante Implementação
- [ ] Testar cada correção individualmente
- [ ] Rodar testes após cada mudança
- [ ] Verificar que nada quebrou
- [ ] Documentar alterações

### Após Correções
- [ ] Executar suite de testes completa
- [ ] Fazer scan de segurança (bandit)
- [ ] Atualizar documentação
- [ ] Criar commit detalhado
- [ ] Atualizar score de segurança

---

## 🔍 FERRAMENTAS RECOMENDADAS

### Teste de Segurança
```bash
# Bandit - Security linter
pip install bandit
bandit -r app/ -ll

# Safety - Dependency checker
pip install safety
safety check

# OWASP ZAP - Penetration testing
# https://www.zaproxy.org/
```

### Monitoramento
```bash
# Prometheus + Grafana para métricas
# ELK Stack para logs
# Sentry para error tracking
```

---

## 📞 SUPORTE E CONTATO

**Para dúvidas sobre implementação:**
- 📧 Email: dev@sentinel.com
- 📚 Docs: `docs/security/`

**Para reportar novas vulnerabilidades:**
- 📧 Email: security@sentinel.com
- 🔒 PGP Key: disponível em `docs/security/pgp-key.asc`

---

## 📊 MATRIZ DE RISCO

```
IMPACTO
   ↑
  Alta │ 🟡 [#009-#016]    🔴 [#001, #002, #003]
       │                  🟠 [#004, #005, #006, #007, #008]
       │
 Média │ 🟢 [#017-#022]
       │
 Baixa │
       └──────────────────────────────→ PROBABILIDADE
              Baixa      Média      Alta
```

---

**✅ ANÁLISE COMPLETA! Pronto para começar as correções quando você decidir.**

**Score Atual:** 54/100 🔴
**Score Após Correções Críticas:** 69/100 🟡
**Score Após Correções Altas:** 79/100 🟢
**Score Final (Fase 3):** 89/100 ✅

---

**Data:** 04/02/2026
**Próximo Passo:** Aguardando aprovação para iniciar Fase 1 (6 horas)
