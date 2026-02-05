# 🔍 Auditoria de Segurança - Estado Atual do SENTINEL

**Data:** 2024-02-04
**Versão:** MVP1 + Módulo de Autenticação
**Objetivo:** Lançamento em VPS

---

## 📊 RESUMO EXECUTIVO

### Status Geral: 🟡 PARCIALMENTE SEGURO

- ✅ **Implementado:** Sistema de autenticação JWT básico
- ⚠️ **Pendente:** Rate limiting, HTTPS, validações completas, logs de auditoria
- ❌ **Ausente:** Proteção de rotas existentes, firewall, backups automáticos

### Riscos Principais:
1. 🔴 **CRÍTICO:** Rotas existentes não protegidas (qualquer um pode acessar)
2. 🔴 **CRÍTICO:** CORS muito permissivo (localhost aceito)
3. 🟡 **ALTO:** Sem rate limiting (vulnerável a DoS)
4. 🟡 **ALTO:** Sem HTTPS (dados trafegam em texto plano)
5. 🟡 **ALTO:** SECRET_KEY default (inseguro)

---

## ✅ O QUE JÁ ESTÁ IMPLEMENTADO

### 1. Autenticação JWT ✅
**Arquivos:**
- `app/core/security.py` - Hash bcrypt + JWT
- `app/models/user.py` - Model de usuário
- `app/schemas/auth.py` - Validação Pydantic
- `app/middleware/auth.py` - Middleware de autenticação
- `app/api/v1/auth.py` - Endpoints de auth

**Funcionalidades:**
- ✅ Hash seguro de senhas (bcrypt)
- ✅ Tokens JWT stateless
- ✅ Validação forte de senhas (8+ chars, maiúscula, número)
- ✅ Endpoints: register, login, me, change-password, delete-account
- ✅ Middleware para proteger rotas (`get_current_user`, `get_current_admin_user`)

**Avaliação:** ⭐⭐⭐⭐☆ (Bem implementado, mas não integrado)

---

### 2. Configurações de Segurança ✅
**Arquivo:** `app/config.py`

**Configurações adicionadas:**
```python
SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"  # ⚠️ Precisa mudar!
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
RATE_LIMIT_ENABLED: bool = True  # ⚠️ Não implementado ainda
RATE_LIMIT_PER_MINUTE: int = 60
```

**Avaliação:** ⭐⭐⭐☆☆ (Configurado, mas valores default inseguros)

---

### 3. CORS Básico ✅
**Arquivo:** `app/main.py` (linhas 107-118)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # ⚠️ Muito permissivo
    allow_headers=["*"],  # ⚠️ Muito permissivo
)
```

**Problemas:**
- ❌ Origins hardcoded (não usa `settings.cors_origins_list`)
- ⚠️ `allow_methods=["*"]` aceita qualquer método HTTP
- ⚠️ `allow_headers=["*"]` aceita qualquer header

**Avaliação:** ⭐⭐☆☆☆ (Funcional, mas inseguro para produção)

---

### 4. Logging Básico ✅
**Arquivo:** `app/utils/logger.py` (existe)

**Implementado:**
- ✅ Loguru para logs estruturados
- ✅ Rotação de logs (assumido)
- ✅ Diferentes níveis (INFO, ERROR, DEBUG)

**Faltando:**
- ❌ Logs de auditoria (quem fez o quê, quando)
- ❌ Logs de tentativas de login falhadas
- ❌ Logs de ações sensíveis (delete, update)
- ❌ Correlação de logs por request ID

**Avaliação:** ⭐⭐⭐☆☆ (Básico funcional, precisa auditoria)

---

### 5. Validação de Input (Parcial) ⚠️

**Implementado:**
- ✅ Pydantic schemas em `app/schemas/auth.py`
- ✅ Validação de email, username, senha

**Faltando:**
- ❌ Validação em rotas de bookings
- ❌ Sanitização de SQL (usando ORM, mas pode ter raw queries)
- ❌ Validação de file uploads (se houver)
- ❌ Proteção contra XSS em inputs

**Avaliação:** ⭐⭐☆☆☆ (Apenas em endpoints de auth)

---

## ❌ O QUE ESTÁ FALTANDO (CRÍTICO)

### 1. 🔴 PROTEÇÃO DE ROTAS EXISTENTES

**Problema:** TODAS as rotas de negócio estão DESPROTEGIDAS!

**Rotas vulneráveis:**
- `GET /api/bookings/` - Qualquer um pode listar reservas
- `POST /api/bookings/` - Qualquer um pode criar reservas
- `DELETE /api/bookings/{id}` - Qualquer um pode deletar
- `GET /api/conflicts/` - Qualquer um vê conflitos
- `GET /api/statistics/dashboard` - Qualquer um vê estatísticas
- `POST /api/calendar/sync` - Qualquer um pode forçar sync

**Impacto:** 🔴 CRÍTICO
**Risco:** Vazamento de dados, manipulação de reservas, DoS

**Solução:**
```python
# Exemplo: app/routers/bookings.py
from app.middleware.auth import get_current_active_user
from app.models.user import User

@router.get("/", response_model=BookingListResponse)
def list_bookings(
    property_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # ADICIONAR
):
    # Agora só usuários autenticados podem acessar
    ...
```

**Tempo para corrigir:** 30-60 minutos

---

### 2. 🔴 RATE LIMITING

**Problema:** Sem proteção contra ataques de força bruta e DoS

**Vulnerabilidades:**
- Tentativas ilimitadas de login
- Spam de requests à API
- Força bruta em senhas
- Enumeration de usuários

**Impacto:** 🔴 CRÍTICO
**Risco:** Servidor sobrecarregado, credenciais comprometidas

**Solução:** Implementar `slowapi`

```python
# Instalar
pip install slowapi

# app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Usar em rotas sensíveis
@router.post("/auth/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
def login(...):
    ...
```

**Tempo para implementar:** 1-2 horas

---

### 3. 🔴 HTTPS/TLS

**Problema:** Servidor roda em HTTP (porta 8000)

**Vulnerabilidades:**
- Senhas trafegam em texto plano
- Tokens JWT interceptáveis (man-in-the-middle)
- Dados de reservas visíveis na rede

**Impacto:** 🔴 CRÍTICO
**Risco:** Credenciais roubadas, sessões sequestradas

**Solução para VPS:**

1. **Nginx como reverse proxy com SSL:**
```nginx
server {
    listen 443 ssl http2;
    server_name sentinel.seudominio.com;

    ssl_certificate /etc/letsencrypt/live/sentinel.seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sentinel.seudominio.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Let's Encrypt (grátis):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d sentinel.seudominio.com
```

**Tempo para implementar:** 1 hora (com Nginx)

---

### 4. 🟡 SECRET_KEY DEFAULT

**Problema:** `SECRET_KEY = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"`

**Vulnerabilidades:**
- Tokens JWT podem ser forjados
- Qualquer um com acesso ao código pode gerar tokens válidos

**Impacto:** 🟡 ALTO
**Risco:** Autenticação comprometida

**Solução:**
```bash
# Gerar chave forte
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Adicionar ao .env
SECRET_KEY=XjT8v9k2Lm4Pq7Rw3Yz6Bc5Nd1Hf0Gx
```

**Tempo para corrigir:** 2 minutos

---

### 5. 🟡 VALIDAÇÃO DE INPUT INCOMPLETA

**Problema:** Apenas endpoints de auth têm validação Pydantic

**Rotas sem validação:**
- `POST /api/bookings/` - Pode aceitar dados malformados
- `PUT /api/bookings/{id}` - Sem validação de campos
- Outros endpoints de criação/atualização

**Impacto:** 🟡 MÉDIO
**Risco:** SQL injection (baixo com ORM), dados corrompidos

**Solução:** Criar schemas Pydantic para todas as operações

```python
# app/schemas/booking.py
from pydantic import BaseModel, Field, validator

class BookingCreate(BaseModel):
    guest_name: str = Field(..., min_length=2, max_length=200)
    check_in_date: date
    check_out_date: date

    @validator('check_out_date')
    def check_out_after_check_in(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out deve ser após check-in')
        return v
```

**Tempo para implementar:** 2-3 horas

---

### 6. 🟡 LOGS DE AUDITORIA

**Problema:** Sem registro de ações sensíveis

**Faltando:**
- Quem criou/atualizou/deletou cada registro
- Tentativas de login falhadas
- Mudanças de senha
- Acessos não autorizados

**Impacto:** 🟡 MÉDIO
**Risco:** Impossível rastrear ataques ou uso indevido

**Solução:** Criar tabela de auditoria

```python
# app/models/audit_log.py
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100))  # login, create_booking, delete_booking
    resource_type = Column(String(50))  # booking, user, property
    resource_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)
```

**Tempo para implementar:** 3-4 horas

---

### 7. 🟢 BACKUPS AUTOMÁTICOS

**Problema:** Sem sistema de backup

**Risco:** Perda de dados em caso de falha

**Solução:**
```bash
#!/bin/bash
# scripts/backup_db.sh
DATE=$(date +%Y-%m-%d_%H-%M-%S)
cp data/sentinel.db backups/sentinel_$DATE.db
find backups/ -name "*.db" -mtime +7 -delete  # Deletar backups >7 dias

# Agendar com cron
0 2 * * * /path/to/scripts/backup_db.sh
```

**Tempo para implementar:** 30 minutos

---

### 8. 🟢 FIREWALL (VPS)

**Problema:** Todas as portas abertas por padrão

**Solução com UFW:**
```bash
# Permitir apenas SSH, HTTP e HTTPS
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

**Tempo para implementar:** 5 minutos

---

### 9. 🟢 HEADERS DE SEGURANÇA

**Problema:** Sem headers de segurança HTTP

**Faltando:**
- `Strict-Transport-Security` (HSTS)
- `X-Frame-Options` (proteção contra clickjacking)
- `X-Content-Type-Options` (proteção contra MIME sniffing)
- `Content-Security-Policy` (proteção contra XSS)

**Solução (Nginx):**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

**Tempo para implementar:** 10 minutos

---

## 📋 PLANO DE AÇÃO PARA VPS

### FASE 1: ESSENCIAL (ANTES DE LANÇAR) - 4-6 horas

Sem isso, **NÃO LANCE EM VPS!**

1. **✅ Proteger rotas existentes** (1h)
   - Adicionar `Depends(get_current_active_user)` em TODAS as rotas de negócio
   - Testar que rotas sem token retornam 401

2. **✅ Gerar SECRET_KEY forte** (2 min)
   - Gerar nova chave
   - Atualizar `.env` no servidor

3. **✅ Implementar rate limiting** (2h)
   - Instalar slowapi
   - Adicionar limites em login, register, API
   - Testar bloqueio após limite

4. **✅ Configurar HTTPS com Let's Encrypt** (1h)
   - Instalar Nginx
   - Configurar reverse proxy
   - Obter certificado SSL
   - Forçar redirect HTTP → HTTPS

5. **✅ Atualizar CORS para produção** (10 min)
   - Remover localhost
   - Adicionar domínio real
   - Usar `settings.cors_origins_list`

6. **✅ Configurar firewall UFW** (5 min)
   - Permitir apenas 22, 80, 443
   - Bloquear todo o resto

**Total:** ~4-6 horas

---

### FASE 2: IMPORTANTE (PRIMEIROS 7 DIAS) - 6-8 horas

1. **Validação completa de input** (3h)
   - Criar schemas Pydantic para bookings, properties
   - Adicionar validações customizadas
   - Testar com inputs maliciosos

2. **Logs de auditoria** (4h)
   - Criar tabela audit_logs
   - Implementar middleware de logging
   - Registrar ações sensíveis

3. **Backups automáticos** (1h)
   - Script de backup
   - Cron job diário
   - Testar restore

**Total:** ~8 horas

---

### FASE 3: RECOMENDADO (PRIMEIRO MÊS) - 4-6 horas

1. **Headers de segurança** (30 min)
   - Adicionar headers no Nginx
   - Testar com https://securityheaders.com/

2. **Monitoring** (3h)
   - Prometheus + Grafana básico
   - Alertas de CPU/RAM
   - Uptime monitoring

3. **Testes de segurança** (2h)
   - SQL injection
   - XSS
   - CSRF
   - Força bruta

**Total:** ~6 horas

---

## 🎯 CHECKLIST PRÉ-LANÇAMENTO VPS

### Segurança Essencial
- [ ] SECRET_KEY gerada e forte
- [ ] TODAS as rotas protegidas com JWT
- [ ] Rate limiting implementado (login: 5/min, API: 60/min)
- [ ] HTTPS configurado (Let's Encrypt)
- [ ] Firewall UFW ativo (apenas 22, 80, 443)
- [ ] CORS atualizado para domínio real
- [ ] `.env` com credenciais reais (não commitar!)
- [ ] Primeiro usuário admin criado

### Configuração VPS
- [ ] Python 3.11+ instalado
- [ ] Nginx instalado e configurado
- [ ] Supervisor/systemd para manter app rodando
- [ ] Banco de dados inicializado
- [ ] Logs sendo salvos em `/var/log/sentinel/`

### Testes Finais
- [ ] Login funciona via HTTPS
- [ ] Rotas sem token retornam 401
- [ ] Rate limit bloqueia após limite
- [ ] Certificado SSL válido
- [ ] Backup manual testado e funcional

---

## 📊 SCORE DE SEGURANÇA

### Antes da Auditoria: 🔴 30/100
- Autenticação: 0/20 (não implementada)
- Autorização: 0/15 (rotas abertas)
- Criptografia: 0/20 (HTTP)
- Rate Limiting: 0/10
- Validação: 5/10 (parcial)
- Logs: 5/10 (básico)
- Backup: 0/5
- Configuração: 20/20 (estrutura boa)

### Depois de Implementar Fase 1: 🟡 75/100
- Autenticação: 18/20 ✅
- Autorização: 15/15 ✅
- Criptografia: 20/20 ✅
- Rate Limiting: 10/10 ✅
- Validação: 5/10 ⚠️
- Logs: 5/10 ⚠️
- Backup: 2/5 ⚠️
- Configuração: 20/20 ✅

### Objetivo Fase 3: 🟢 95/100
- Autenticação: 20/20 ✅
- Autorização: 15/15 ✅
- Criptografia: 20/20 ✅
- Rate Limiting: 10/10 ✅
- Validação: 10/10 ✅
- Logs: 10/10 ✅
- Backup: 5/5 ✅
- Configuração: 20/20 ✅

---

## ⚡ PRIORIDADES IMEDIATAS

### HOJE (Antes de qualquer coisa):
1. Gerar SECRET_KEY forte
2. Proteger rotas de bookings, conflicts, statistics
3. Testar que autenticação funciona

### ESTA SEMANA (Antes de VPS):
1. Implementar rate limiting
2. Configurar validação de input completa
3. Preparar scripts de deploy

### NO VPS (Dia 1):
1. Configurar HTTPS
2. Configurar firewall
3. Primeiro backup manual

---

## 💡 CONCLUSÃO

**Estado atual:** Sistema funcionalmente completo, mas **INSEGURO para produção**.

**Risco de lançar agora:**
- 🔴 Dados podem ser acessados/modificados por qualquer pessoa
- 🔴 Credenciais podem ser interceptadas (HTTP)
- 🔴 Sistema vulnerável a DoS

**Recomendação:**
1. **NÃO LANCE EM VPS SEM IMPLEMENTAR FASE 1**
2. Fase 1 leva 4-6 horas e elimina riscos críticos
3. Fase 2 e 3 podem ser feitas após lançamento

**Próximo passo:** Implementar Fase 1 (começar protegendo as rotas)

---

**Auditoria realizada por:** Claude Sonnet 4.5
**Data:** 2024-02-04
**Próxima revisão:** Após implementação da Fase 1
