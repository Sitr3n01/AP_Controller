# 🛡️ Guia Prático: Implementar Segurança para VPS

## ⏱️ Tempo Estimado
- **Fase 1 (Essencial):** 4-6 horas
- **Fase 2 (Importante):** 2-3 horas
- **Fase 3 (Recomendado):** 3-4 horas
- **Total:** ~10-13 horas

---

## 🎯 FASE 1: ESSENCIAL (Antes de Deploy)

### 1. Implementar Autenticação JWT (2 horas)

#### 1.1. Instalar Dependências
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### 1.2. Criar Módulo de Segurança
**Criar:** `app/core/security.py`
```python
"""
Módulo de segurança - Autenticação JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings

# Configurações
SECRET_KEY = settings.SECRET_KEY  # Adicionar no .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verifica e decodifica JWT token"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    """Hash de senha com bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha"""
    return pwd_context.verify(plain_password, hashed_password)
```

#### 1.3. Adicionar Variáveis no .env
```env
# === SEGURANÇA ===
SECRET_KEY=GERAR_COM_OPENSSL_RAND_HEX_32
API_USERNAME=admin
API_PASSWORD=SENHA_FORTE_AQUI
```

**Gerar SECRET_KEY:**
```bash
openssl rand -hex 32
```

#### 1.4. Atualizar app/config.py
```python
class Settings(BaseSettings):
    # ... existing fields ...

    # === SEGURANÇA ===
    SECRET_KEY: str = Field(..., description="Secret key para JWT")
    API_USERNAME: str = Field("admin", description="Username da API")
    API_PASSWORD: str = Field(..., description="Senha da API (hash)")
```

#### 1.5. Criar Endpoint de Login
**Criar:** `app/routers/auth.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from app.core.security import create_access_token, verify_password
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security_basic = HTTPBasic()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login(credentials: HTTPBasicCredentials = Depends(security_basic)):
    """
    Login com Basic Auth, retorna JWT token
    """
    # Verificar credenciais
    if credentials.username != settings.API_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Verificar senha (assumindo que está em hash no .env)
    # Para primeira vez, gerar hash:
    # from app.core.security import hash_password
    # print(hash_password("sua_senha"))
    if not verify_password(credentials.password, settings.API_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Criar token
    access_token = create_access_token(data={"sub": credentials.username})

    return {"access_token": access_token, "token_type": "bearer"}
```

#### 1.6. Proteger Endpoints
**Exemplo em bookings.py:**
```python
from app.core.security import verify_token

@router.get("/", response_model=BookingListResponse)
def list_bookings(
    property_id: int = Query(...),
    token: dict = Depends(verify_token),  # ✅ ADICIONAR
    db: Session = Depends(get_db)
):
    # Agora protegido!
    pass
```

**Aplicar em TODOS os routers:**
- `app/routers/bookings.py`
- `app/routers/conflicts.py`
- `app/routers/statistics.py`
- `app/routers/sync_actions.py`
- `app/routers/calendar.py`

#### 1.7. Registrar Router de Auth
**Em app/main.py:**
```python
from app.routers import bookings, conflicts, statistics, sync_actions, calendar, auth

# Incluir routers
app.include_router(auth.router)  # ✅ ADICIONAR
app.include_router(bookings.router)
# ... resto
```

---

### 2. Configurar HTTPS (1 hora)

#### 2.1. Obter Certificado SSL
```bash
# Instalar certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obter certificado Let's Encrypt
sudo certbot certonly --standalone -d seu-dominio.com

# Certificados ficarão em:
# /etc/letsencrypt/live/seu-dominio.com/fullchain.pem
# /etc/letsencrypt/live/seu-dominio.com/privkey.pem
```

#### 2.2. Configurar Uvicorn com SSL (Opção 1)
```python
# app/main.py
if __name__ == "__main__":
    import uvicorn

    if settings.APP_ENV == "production":
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",  # Aceitar de qualquer IP
            port=443,
            ssl_keyfile="/etc/letsencrypt/live/seu-dominio.com/privkey.pem",
            ssl_certfile="/etc/letsencrypt/live/seu-dominio.com/fullchain.pem",
            reload=False,
        )
    else:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
```

#### 2.3. Ou Nginx como Reverse Proxy (Opção 2 - RECOMENDADO)
**Criar:** `/etc/nginx/sites-available/sentinel`
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$host$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Hide nginx version
    server_tokens off;

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Frontend (se estático)
    location / {
        root /var/www/sentinel/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Block access to sensitive files
    location ~ /\.(env|git|gitignore)$ {
        deny all;
        return 404;
    }

    # Block access to backup files
    location ~ \.(bak|tmp|old)$ {
        deny all;
        return 404;
    }
}
```

**Ativar:**
```bash
sudo ln -s /etc/nginx/sites-available/sentinel /etc/nginx/sites-enabled/
sudo nginx -t  # Testar config
sudo systemctl reload nginx
```

---

### 3. Configurar Firewall (30 min)

```bash
# Instalar UFW
sudo apt install ufw

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (redirect)
sudo ufw allow 443/tcp   # HTTPS

# Ativar
sudo ufw enable

# Verificar status
sudo ufw status verbose
```

**Segurança Extra SSH:**
```bash
# Editar /etc/ssh/sshd_config
sudo nano /etc/ssh/sshd_config

# Adicionar/modificar:
PermitRootLogin no
PasswordAuthentication no  # Apenas chaves SSH
Port 2222  # Mudar porta padrão

# Reiniciar SSH
sudo systemctl restart sshd

# Atualizar firewall
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp
```

---

### 4. Rate Limiting (1 hora)

#### 4.1. Instalar SlowAPI
```bash
pip install slowapi
```

#### 4.2. Configurar em app/main.py
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Criar limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Adicionar ao app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

#### 4.3. Aplicar em Endpoints Críticos
```python
from slowapi import Limiter
from fastapi import Request

@router.post("/api/calendar/sync")
@limiter.limit("5/minute")  # Apenas 5 syncs por minuto
async def sync_calendar(
    request: Request,  # ✅ Necessário para limiter
    token: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    pass


@router.post("/api/auth/login")
@limiter.limit("10/minute")  # Proteção contra brute force
async def login(request: Request, credentials: HTTPBasicCredentials):
    pass
```

---

### 5. CORS Restritivo (15 min)

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seu-dominio.com",  # ✅ APENAS seu domínio
        "https://www.seu-dominio.com",
    ] if settings.APP_ENV == "production" else [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ✅ Específico
    allow_headers=["Content-Type", "Authorization"],  # ✅ Específico
)
```

---

### 6. Desabilitar Docs em Produção (5 min)

```python
# app/main.py
app = FastAPI(
    title="SENTINEL API",
    description="API para gerenciamento automatizado de apartamento",
    version="1.0.0",
    lifespan=lifespan,
    # ✅ Desabilitar docs em produção
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
    openapi_url="/openapi.json" if settings.APP_ENV != "production" else None,
)
```

---

### 7. Sanitizar Endpoint /api/info (10 min)

```python
@app.get("/api/info")
async def api_info(token: dict = Depends(verify_token)):  # ✅ PROTEGER
    """Informações da API - PROTEGIDO"""
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        # ❌ REMOVER informações sensíveis:
        # "property_name": settings.PROPERTY_NAME,
        # "timezone": settings.TIMEZONE,
        # "sync_interval_minutes": settings.CALENDAR_SYNC_INTERVAL_MINUTES,
    }
```

---

### 8. Backup Automático (30 min)

#### 8.1. Criar Script de Backup
**Criar:** `/opt/sentinel/backup.sh`
```bash
#!/bin/bash

# Configurações
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/sentinel"
DB_PATH="/opt/sentinel/data/sentinel.db"
LOG_FILE="/var/log/sentinel-backup.log"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco de dados
echo "[$DATE] Starting backup..." >> $LOG_FILE
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/sentinel_$DATE.db'" 2>> $LOG_FILE

if [ $? -eq 0 ]; then
    # Comprimir
    gzip "$BACKUP_DIR/sentinel_$DATE.db"
    echo "[$DATE] Backup completed: sentinel_$DATE.db.gz" >> $LOG_FILE

    # Upload para S3 (opcional)
    # aws s3 cp "$BACKUP_DIR/sentinel_$DATE.db.gz" s3://seu-bucket/backups/

    # Limpar backups antigos (manter 30 dias)
    find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
    echo "[$DATE] Old backups cleaned" >> $LOG_FILE
else
    echo "[$DATE] ERROR: Backup failed!" >> $LOG_FILE
    # Enviar alerta (opcional)
    # curl -X POST -H 'Content-Type: application/json' \
    #   -d '{"text":"Backup SENTINEL falhou!"}' \
    #   https://hooks.slack.com/services/SEU_WEBHOOK
fi
```

**Dar permissão:**
```bash
chmod +x /opt/sentinel/backup.sh
```

#### 8.2. Configurar Cron
```bash
# Editar crontab
sudo crontab -e

# Adicionar (backup diário às 3h)
0 3 * * * /opt/sentinel/backup.sh

# Verificar
sudo crontab -l
```

---

## 🎯 FASE 2: IMPORTANTE (Primeira Semana)

### 9. Fail2Ban (30 min)

```bash
# Instalar
sudo apt install fail2ban

# Criar filtro customizado
sudo nano /etc/fail2ban/filter.d/sentinel-api.conf
```

```ini
[Definition]
failregex = ^.*"POST /api/auth/login.*" 401.*$
            ^.*Unauthorized.*<HOST>.*$
ignoreregex =
```

**Configurar jail:**
```bash
sudo nano /etc/fail2ban/jail.local
```

```ini
[sentinel-api]
enabled = true
port = http,https
filter = sentinel-api
logpath = /opt/sentinel/data/logs/*.log
maxretry = 5
findtime = 600
bantime = 3600
action = iptables-multiport[name=sentinel, port="http,https"]
```

**Ativar:**
```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status sentinel-api
```

---

### 10. Logging de Auditoria (1 hora)

**Criar:** `app/core/audit.py`
```python
from app.utils.logger import get_logger
from datetime import datetime

audit_logger = get_logger("audit")


def log_action(user: str, action: str, resource: str, details: dict = None):
    """Registra ação para auditoria"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "action": action,
        "resource": resource,
        "details": details or {}
    }

    audit_logger.info(f"AUDIT: {log_data}")


# Usar nos endpoints:
from app.core.audit import log_action

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    token: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = token.get("sub")
    log_action(user, "DELETE", f"booking/{booking_id}")
    # ... resto do código
```

---

### 11. Monitoramento com Sentry (30 min)

```bash
pip install sentry-sdk
```

```python
# app/main.py
import sentry_sdk

if settings.APP_ENV == "production":
    sentry_sdk.init(
        dsn="https://sua-dsn@sentry.io/projeto",
        traces_sample_rate=1.0,
        environment=settings.APP_ENV,
    )
```

---

## 📋 CHECKLIST FINAL

### Antes de Deploy
- [ ] Autenticação JWT implementada
- [ ] SECRET_KEY gerada e configurada
- [ ] Todos endpoints protegidos
- [ ] HTTPS configurado (certbot)
- [ ] Firewall ativo (UFW)
- [ ] Rate limiting implementado
- [ ] CORS restritivo
- [ ] Docs desabilitados em produção
- [ ] /api/info sanitizado
- [ ] Backup automático configurado

### Primeira Semana
- [ ] Nginx configurado
- [ ] Fail2ban ativo
- [ ] Logging de auditoria
- [ ] Monitoramento (Sentry/similar)
- [ ] Teste de penetração básico

### Verificações
```bash
# Testar autenticação
curl -X POST https://seu-dominio.com/api/auth/login \
  -u admin:senha

# Testar endpoint protegido (deve falhar sem token)
curl https://seu-dominio.com/api/bookings?property_id=1
# Esperado: 401 Unauthorized

# Testar com token
curl -H "Authorization: Bearer SEU_TOKEN" \
  https://seu-dominio.com/api/bookings?property_id=1
# Esperado: 200 OK com dados

# Verificar HTTPS
curl -I https://seu-dominio.com
# Esperado: HTTP/2 200

# Verificar rate limiting
for i in {1..200}; do
  curl https://seu-dominio.com/api/bookings?property_id=1
done
# Esperado: 429 Too Many Requests após limite
```

---

**Tempo Total Estimado:** 4-6 horas (Fase 1)
**Próximo:** Implementar Fase 2 na primeira semana
