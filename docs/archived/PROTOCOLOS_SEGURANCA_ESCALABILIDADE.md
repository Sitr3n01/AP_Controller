# 🔐 Protocolos de Segurança para Escalabilidade

## 📋 ÍNDICE

1. [Análise de Escalabilidade](#análise-de-escalabilidade)
2. [Arquitetura de Segurança Multi-Tenant](#arquitetura-multi-tenant)
3. [Protocolos de Autenticação](#protocolos-de-autenticação)
4. [Isolamento de Dados](#isolamento-de-dados)
5. [Compliance e Regulamentações](#compliance-e-regulamentações)
6. [Infraestrutura Escalável](#infraestrutura-escalável)
7. [Monitoramento e Auditoria](#monitoramento-e-auditoria)
8. [Plano de Resposta a Incidentes](#plano-de-resposta-a-incidentes)

---

## 🎯 ANÁLISE DE ESCALABILIDADE

### Estado Atual vs. Escalado

| Aspecto | ATUAL (1 apartamento) | ESCALADO (N clientes) |
|---------|----------------------|------------------------|
| Usuários | 1 proprietário | Centenas/Milhares |
| Apartamentos | 1 | Múltiplos por cliente |
| Dados | ~1-50 reservas/mês | Milhões de reservas |
| Segurança | Baixa (local) | CRÍTICA (multi-tenant) |
| Compliance | Nenhum | LGPD, GDPR obrigatório |
| Isolamento | Não necessário | ESSENCIAL |
| Backup | Manual | Automatizado + DR |
| Monitoramento | Básico | 24/7 + Alertas |

---

## 🏗️ ARQUITETURA MULTI-TENANT

### Modelo de Isolamento

**Opção 1: Database per Tenant (MAIS SEGURO)**
```
Cliente A → DB_cliente_a
Cliente B → DB_cliente_b
Cliente C → DB_cliente_c
```

**Prós:**
- ✅ Isolamento total de dados
- ✅ Compliance facilitado
- ✅ Backup individual
- ✅ Performance previsível
- ✅ Migração fácil se cliente sair

**Contras:**
- ❌ Mais custos de infraestrutura
- ❌ Mais complexo gerenciar múltiplos DBs
- ❌ Atualizações de schema mais demoradas

**Opção 2: Shared Database, Schema per Tenant (INTERMEDIÁRIO)**
```
Database Único
├── schema_cliente_a
├── schema_cliente_b
└── schema_cliente_c
```

**Prós:**
- ✅ Bom isolamento
- ✅ Menos recursos que opção 1
- ✅ Migração relativamente fácil

**Contras:**
- ❌ Noisy neighbor problem
- ❌ Backup mais complexo
- ❌ Risco de vazamento entre schemas

**Opção 3: Shared Database, Shared Schema (MENOS SEGURO)**
```
Database Único
└── Tables
    └── tenant_id column em todas
```

**Prós:**
- ✅ Mais barato
- ✅ Mais simples de gerenciar
- ✅ Atualizações rápidas

**Contras:**
- ❌ Alto risco de vazamento de dados
- ❌ Compliance difícil
- ❌ Performance unpredictable
- ❌ Backup/restore complicado

**RECOMENDAÇÃO:** **Opção 1 (Database per Tenant)** para SENTINEL

---

## 🔒 PROTOCOLOS DE AUTENTICAÇÃO

### 1. Autenticação Multi-Nível

#### Nível 1: Autenticação de Aplicação
```python
# JWT com claims adicionais
{
  "sub": "user_id_123",
  "tenant_id": "tenant_abc",  # CRÍTICO: Identificar tenant
  "role": "owner",  # owner, manager, viewer
  "properties": ["prop_1", "prop_2"],  # Propriedades que pode acessar
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique_token_id"
}
```

**Implementação:**
```python
# app/core/security.py

from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: str
    tenant_id: str
    role: str
    properties: List[str]

def create_access_token(
    user_id: str,
    tenant_id: str,
    role: str,
    properties: List[str],
    expires_delta: Optional[timedelta] = None
):
    """Cria JWT com informações de tenant"""
    to_encode = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "properties": properties,
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_and_tenant(
    token: str,
    required_tenant_id: str
) -> TokenData:
    """Verifica token E valida tenant_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extrair dados
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")
        properties = payload.get("properties", [])

        # CRÍTICO: Validar tenant
        if tenant_id != required_tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Acesso negado: Tenant não autorizado"
            )

        return TokenData(
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
            properties=properties
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
```

#### Nível 2: Row-Level Security (RLS)
```python
# Middleware para injetar tenant_id em todas as queries
from starlette.middleware.base import BaseHTTPMiddleware

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Extrair tenant do token
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if token:
            try:
                token_data = verify_token(token)
                request.state.tenant_id = token_data.tenant_id
                request.state.user_id = token_data.user_id
                request.state.role = token_data.role
            except:
                pass

        response = await call_next(request)
        return response


# Dependency para forçar filtro de tenant
from fastapi import Request, HTTPException

def get_current_tenant(request: Request) -> str:
    """Retorna tenant_id do request ou falha"""
    tenant_id = getattr(request.state, "tenant_id", None)

    if not tenant_id:
        raise HTTPException(
            status_code=401,
            detail="Tenant não identificado"
        )

    return tenant_id


# Usar em TODOS os endpoints
@router.get("/bookings")
def list_bookings(
    request: Request,
    property_id: int,
    tenant_id: str = Depends(get_current_tenant),  # SEMPRE
    db: Session = Depends(get_db)
):
    # Query SEMPRE filtra por tenant
    bookings = db.query(Booking).filter(
        Booking.tenant_id == tenant_id,  # CRÍTICO
        Booking.property_id == property_id
    ).all()

    return bookings
```

#### Nível 3: Database-Level Security
```sql
-- PostgreSQL Row-Level Security (RLS)
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Policy: Usuário só vê dados do seu tenant
CREATE POLICY tenant_isolation ON bookings
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Aplicar a TODAS as tabelas
ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE calendar_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE booking_conflicts ENABLE ROW LEVEL SECURITY;
-- etc...
```

```python
# Setar tenant no início de cada request
from sqlalchemy import text

def set_tenant_context(db: Session, tenant_id: str):
    """Define tenant_id no contexto do DB"""
    db.execute(text(f"SET app.current_tenant_id = '{tenant_id}'"))
```

---

## 🛡️ ISOLAMENTO DE DADOS

### 1. Schema de Database Multi-Tenant

**Adicionar tenant_id em TODAS as tabelas:**

```python
# app/models/base.py
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TenantBase:
    """Base class para modelos multi-tenant"""
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)


# app/models/property.py
class Property(Base, TenantBase):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # ADICIONAR
    name = Column(String)
    # ... resto dos campos

    # Índice composto para performance
    __table_args__ = (
        Index('idx_property_tenant', 'tenant_id', 'id'),
    )


# Aplicar em TODOS os models:
# - Booking
# - CalendarSource
# - BookingConflict
# - SyncAction
# - Guest (MVP2)
# - etc.
```

### 2. Validação de Tenant em Queries

```python
# app/core/tenant_validator.py

class TenantValidator:
    """Valida que queries não vazem dados entre tenants"""

    @staticmethod
    def validate_query(query, tenant_id: str):
        """Garante que query tem filtro de tenant"""
        # Verificar se query tem WHERE tenant_id
        query_str = str(query.statement.compile())

        if f"tenant_id = '{tenant_id}'" not in query_str:
            raise SecurityException(
                "Query sem filtro de tenant detectada!"
            )

        return query


# Usar em queries críticas
@router.get("/bookings")
def list_bookings(
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    query = db.query(Booking).filter(Booking.tenant_id == tenant_id)

    # Validar antes de executar
    TenantValidator.validate_query(query, tenant_id)

    return query.all()
```

### 3. Segregação de Arquivos

```python
# Cada tenant tem sua pasta isolada
def get_tenant_storage_path(tenant_id: str, file_type: str) -> Path:
    """Retorna path isolado por tenant"""
    base = Path("/storage/tenants")
    tenant_path = base / tenant_id / file_type

    # Criar se não existir
    tenant_path.mkdir(parents=True, exist_ok=True)

    # Validar que não sai do sandbox
    if not str(tenant_path).startswith(str(base)):
        raise SecurityException("Path traversal detectado!")

    return tenant_path


# Exemplo de uso
def save_document(tenant_id: str, filename: str, content: bytes):
    """Salva documento no storage do tenant"""
    storage_path = get_tenant_storage_path(tenant_id, "documents")
    file_path = storage_path / filename

    # Validar filename (evitar path traversal)
    if ".." in filename or "/" in filename:
        raise ValueError("Filename inválido")

    file_path.write_bytes(content)
```

---

## 📜 COMPLIANCE E REGULAMENTAÇÕES

### 1. LGPD (Lei Geral de Proteção de Dados - Brasil)

**Dados que coletamos:**
- ✅ Nomes de hóspedes
- ✅ Datas de hospedagem
- ✅ Valores de reservas
- ✅ Plataforma de origem
- ⚠️  Potencialmente: CPF, telefone, email (MVP2)

**Obrigações:**
1. **Consentimento** - Obter autorização para processar dados
2. **Finalidade** - Usar dados apenas para gestão de reservas
3. **Transparência** - Informar o que fazemos com os dados
4. **Segurança** - Proteger dados de vazamentos
5. **Direitos do Titular** - Permitir acesso, correção, exclusão
6. **Retenção** - Deletar dados após período necessário

**Implementação:**

```python
# app/models/data_consent.py

class DataConsent(Base, TenantBase):
    """Registro de consentimento LGPD"""
    __tablename__ = "data_consents"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    guest_id = Column(Integer, ForeignKey("guests.id"))

    # Consentimentos específicos
    consent_data_processing = Column(Boolean, default=False)
    consent_data_storage = Column(Boolean, default=False)
    consent_marketing = Column(Boolean, default=False)  # Futuro

    # Rastreabilidade
    consented_at = Column(DateTime, default=datetime.utcnow)
    consent_ip = Column(String)  # IP de onde consentiu
    consent_method = Column(String)  # web, telegram, etc.

    # Revogação
    revoked_at = Column(DateTime, nullable=True)
    revoked_reason = Column(Text, nullable=True)


# Endpoint para exercer direitos LGPD
@router.post("/api/lgpd/request")
async def lgpd_data_request(
    request_type: str,  # access, rectify, delete, portability
    guest_email: str,
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """Processa solicitação de direitos LGPD"""

    if request_type == "access":
        # Retornar todos os dados do titular
        guest = db.query(Guest).filter(
            Guest.tenant_id == tenant_id,
            Guest.email == guest_email
        ).first()

        if not guest:
            raise HTTPException(404, "Dados não encontrados")

        # Retornar em formato legível
        return {
            "data": guest.to_dict(),
            "bookings": [b.to_dict() for b in guest.bookings]
        }

    elif request_type == "delete":
        # Anonimizar ou deletar dados
        guest = db.query(Guest).filter(
            Guest.tenant_id == tenant_id,
            Guest.email == guest_email
        ).first()

        if guest:
            # Anonimizar ao invés de deletar (manter histórico)
            guest.name = "DADOS REMOVIDOS"
            guest.email = f"anonimizado_{guest.id}@deleted.local"
            guest.phone = None
            guest.cpf = None
            guest.deleted_at = datetime.utcnow()
            db.commit()

        return {"status": "deleted"}

    elif request_type == "portability":
        # Exportar dados em formato portável
        # ... implementar
        pass
```

### 2. GDPR (Se tiver clientes na Europa)

**Adicional ao LGPD:**
- Data Protection Officer (DPO) obrigatório
- Notificação de breach em 72h
- Privacy by Design
- Impact Assessment para novos processos

### 3. PCI-DSS (Se processar pagamentos)

**Não aplicável** - Não processamos cartões diretamente
- Airbnb e Booking fazem o processamento
- Apenas recebemos valores já processados

---

## 🏢 INFRAESTRUTURA ESCALÁVEL

### 1. Arquitetura de Deployment

```
                    ┌─────────────┐
                    │  CloudFlare │  (DDoS Protection + CDN)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  WAF        │  (Web Application Firewall)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Load Balancer│  (Nginx/HAProxy)
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐        ┌────▼────┐      ┌────▼────┐
   │ App 1   │        │ App 2   │      │ App N   │  (Auto-scaling)
   └────┬────┘        └────┬────┘      └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Redis     │  (Cache + Sessions)
                    └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐        ┌────▼────┐      ┌────▼────┐
   │  DB 1   │        │  DB 2   │      │  DB N   │  (Database per Tenant)
   │(Tenant A)│       │(Tenant B)│     │(Tenant C)│
   └─────────┘        └─────────┘      └─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   S3/Blob   │  (Backups + Arquivos)
                    └─────────────┘
```

### 2. Configuração de Segurança por Camada

#### CloudFlare
```yaml
# Configurações CloudFlare
security_level: high
challenge_passage: 30  # minutos
browser_integrity_check: true
email_obfuscation: true
server_side_exclude: true
hotlink_protection: true

# Rate limiting
rate_limits:
  - path: "/api/*"
    requests: 100
    period: 60  # segundos
    action: challenge

  - path: "/api/auth/login"
    requests: 5
    period: 300
    action: block
```

#### WAF (ModSecurity)
```nginx
# nginx.conf com ModSecurity
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;

# OWASP Core Rule Set
Include /etc/nginx/modsec/coreruleset/*.conf

# Custom rules
SecRule ARGS "@rx <script" \
    "id:1001,\
    phase:2,\
    block,\
    log,\
    msg:'XSS Attack Detected'"

SecRule ARGS "@rx (\%27)|(\')|(\-\-)|(\%23)|(#)" \
    "id:1002,\
    phase:2,\
    block,\
    log,\
    msg:'SQL Injection Detected'"
```

#### Load Balancer (Nginx)
```nginx
# /etc/nginx/nginx.conf

upstream sentinel_app {
    least_conn;  # Algoritmo de balanceamento

    server app1.internal:8000 max_fails=3 fail_timeout=30s;
    server app2.internal:8000 max_fails=3 fail_timeout=30s;
    server app3.internal:8000 max_fails=3 fail_timeout=30s;

    # Health check
    check interval=3000 rise=2 fall=5 timeout=1000;
}

server {
    listen 443 ssl http2;
    server_name api.sentinel.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.sentinel.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.sentinel.com/privkey.pem;
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

    location /api/auth/login {
        limit_req zone=login_limit burst=3 nodelay;
        proxy_pass http://sentinel_app;
        include proxy_params;
    }

    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://sentinel_app;
        include proxy_params;
    }

    # Block common attacks
    location ~ (\.env|\.git|\.svn) {
        deny all;
        return 404;
    }
}
```

### 3. Auto-Scaling

**AWS Auto Scaling Group:**
```yaml
# autoscaling-config.yaml
AutoScalingGroup:
  MinSize: 2
  MaxSize: 10
  DesiredCapacity: 3
  HealthCheckType: ELB
  HealthCheckGracePeriod: 300

  ScalingPolicies:
    - Name: ScaleUpOnCPU
      AdjustmentType: ChangeInCapacity
      ScalingAdjustment: 2
      Cooldown: 300
      MetricAggregationType: Average
      StepAdjustments:
        - MetricIntervalLowerBound: 0
          MetricIntervalUpperBound: 10
          ScalingAdjustment: 1
        - MetricIntervalLowerBound: 10
          ScalingAdjustment: 2

      Alarms:
        - AlarmName: HighCPUUtilization
          ComparisonOperator: GreaterThanThreshold
          EvaluationPeriods: 2
          MetricName: CPUUtilization
          Threshold: 70

    - Name: ScaleDownOnCPU
      AdjustmentType: ChangeInCapacity
      ScalingAdjustment: -1
      Cooldown: 300

      Alarms:
        - AlarmName: LowCPUUtilization
          ComparisonOperator: LessThanThreshold
          EvaluationPeriods: 5
          MetricName: CPUUtilization
          Threshold: 30
```

---

## 📊 MONITORAMENTO E AUDITORIA

### 1. Logging Estruturado

```python
# app/core/audit_logger.py

import structlog
from datetime import datetime
from typing import Any, Dict

# Configurar structlog
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

audit_log = structlog.get_logger("audit")

class AuditLogger:
    """Logger de auditoria para compliance"""

    @staticmethod
    def log_access(
        tenant_id: str,
        user_id: str,
        resource: str,
        action: str,
        ip_address: str,
        user_agent: str,
        result: str,  # success, denied, error
        details: Dict[str, Any] = None
    ):
        """Registra acesso a recursos"""
        audit_log.info(
            "resource_access",
            tenant_id=tenant_id,
            user_id=user_id,
            resource=resource,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            result=result,
            details=details or {},
            timestamp=datetime.utcnow().isoformat()
        )

    @staticmethod
    def log_data_change(
        tenant_id: str,
        user_id: str,
        table: str,
        record_id: str,
        operation: str,  # insert, update, delete
        old_values: Dict = None,
        new_values: Dict = None
    ):
        """Registra mudanças em dados"""
        audit_log.info(
            "data_change",
            tenant_id=tenant_id,
            user_id=user_id,
            table=table,
            record_id=record_id,
            operation=operation,
            old_values=old_values or {},
            new_values=new_values or {},
            timestamp=datetime.utcnow().isoformat()
        )

    @staticmethod
    def log_security_event(
        event_type: str,  # auth_failure, token_expired, suspicious_activity
        severity: str,  # low, medium, high, critical
        tenant_id: str = None,
        user_id: str = None,
        ip_address: str = None,
        details: Dict[str, Any] = None
    ):
        """Registra eventos de segurança"""
        audit_log.warning(
            "security_event",
            event_type=event_type,
            severity=severity,
            tenant_id=tenant_id,
            user_id=user_id,
            ip_address=ip_address,
            details=details or {},
            timestamp=datetime.utcnow().isoformat()
        )


# Middleware de auditoria
class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.utcnow()

        # Extrair informações
        tenant_id = getattr(request.state, "tenant_id", None)
        user_id = getattr(request.state, "user_id", None)
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")

        # Processar request
        try:
            response = await call_next(request)
            result = "success" if response.status_code < 400 else "error"
        except Exception as e:
            result = "error"
            raise
        finally:
            # Log de auditoria
            AuditLogger.log_access(
                tenant_id=tenant_id or "anonymous",
                user_id=user_id or "anonymous",
                resource=request.url.path,
                action=request.method,
                ip_address=ip_address,
                user_agent=user_agent,
                result=result,
                details={
                    "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
                }
            )

        return response
```

### 2. Métricas e Alertas

**Prometheus + Grafana:**

```python
# app/core/metrics.py

from prometheus_client import Counter, Histogram, Gauge
import time

# Métricas de negócio
bookings_created = Counter('bookings_created_total', 'Total de reservas criadas', ['tenant_id', 'platform'])
conflicts_detected = Counter('conflicts_detected_total', 'Total de conflitos detectados', ['tenant_id', 'severity'])
sync_duration = Histogram('sync_duration_seconds', 'Duração da sincronização', ['tenant_id'])

# Métricas de segurança
failed_logins = Counter('failed_logins_total', 'Total de logins falhos', ['tenant_id', 'reason'])
unauthorized_access = Counter('unauthorized_access_total', 'Tentativas de acesso não autorizado', ['tenant_id', 'resource'])

# Métricas de sistema
active_tenants = Gauge('active_tenants', 'Número de tenants ativos')
db_connections = Gauge('db_connections', 'Conexões ativas no DB', ['tenant_id'])


# Exemplo de uso
@router.post("/bookings")
async def create_booking(
    booking_data: BookingCreate,
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    booking = create_booking_service(booking_data, tenant_id, db)

    # Incrementar métrica
    bookings_created.labels(
        tenant_id=tenant_id,
        platform=booking_data.platform
    ).inc()

    return booking
```

**Alertas (Prometheus AlertManager):**

```yaml
# alerts.yaml
groups:
  - name: security_alerts
    interval: 30s
    rules:
      # Alerta de múltiplos logins falhos
      - alert: BruteForceAttack
        expr: rate(failed_logins_total[5m]) > 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Possível ataque de força bruta"
          description: "Mais de 10 logins falhos em 5 minutos para tenant {{ $labels.tenant_id }}"

      # Alerta de acessos não autorizados
      - alert: UnauthorizedAccessSpike
        expr: rate(unauthorized_access_total[5m]) > 5
        for: 2m
        labels:
          severity: high
        annotations:
          summary: "Spike de acessos não autorizados"
          description: "Múltiplas tentativas de acesso não autorizado para tenant {{ $labels.tenant_id }}"

      # Alerta de muitos conflitos
      - alert: HighConflictRate
        expr: rate(conflicts_detected_total{severity="critical"}[1h]) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Taxa alta de conflitos críticos"
          description: "Tenant {{ $labels.tenant_id }} com muitos conflitos críticos"
```

### 3. SIEM (Security Information and Event Management)

**Integração com ELK Stack:**

```python
# app/core/siem.py

from elasticsearch import Elasticsearch
from datetime import datetime

class SIEMLogger:
    def __init__(self):
        self.es = Elasticsearch(['https://elk.internal:9200'])

    def log_security_event(self, event: dict):
        """Envia evento de segurança para SIEM"""
        event['@timestamp'] = datetime.utcnow().isoformat()
        event['event_type'] = 'security'

        self.es.index(
            index=f"sentinel-security-{datetime.utcnow().strftime('%Y.%m')}",
            document=event
        )

    def search_suspicious_activity(
        self,
        tenant_id: str,
        hours: int = 24
    ):
        """Busca atividades suspeitas"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"tenant_id": tenant_id}},
                        {"term": {"result": "denied"}},
                        {"range": {
                            "@timestamp": {
                                "gte": f"now-{hours}h"
                            }
                        }}
                    ]
                }
            },
            "aggs": {
                "by_ip": {
                    "terms": {"field": "ip_address"}
                }
            }
        }

        return self.es.search(
            index="sentinel-security-*",
            body=query
        )
```

---

## 🚨 PLANO DE RESPOSTA A INCIDENTES

### 1. Classificação de Incidentes

| Severidade | Tempo de Resposta | Exemplos |
|------------|-------------------|----------|
| **P0 - Crítico** | < 15 minutos | Vazamento de dados, Sistema fora do ar |
| **P1 - Alto** | < 1 hora | Brute force attack, Falha de autenticação |
| **P2 - Médio** | < 4 horas | Performance degradada, Erro intermitente |
| **P3 - Baixo** | < 24 horas | Bug menor, Request de feature |

### 2. Procedimentos de Resposta

**Incidente P0: Vazamento de Dados**

```
1. CONTENÇÃO (0-15 min)
   □ Desativar acesso ao sistema
   □ Isolar banco de dados afetado
   □ Bloquear IPs suspeitos no firewall
   □ Revogar todos tokens JWT ativos

2. INVESTIGAÇÃO (15-60 min)
   □ Identificar origem do vazamento
   □ Determinar quais dados foram expostos
   □ Identificar tenants afetados
   □ Coletar logs e evidências

3. ERRADICAÇÃO (1-4 horas)
   □ Corrigir vulnerabilidade
   □ Atualizar credenciais comprometidas
   □ Aplicar patches de segurança

4. RECUPERAÇÃO (4-24 horas)
   □ Restaurar sistema com correções
   □ Validar segurança
   □ Reativar acesso gradualmente

5. NOTIFICAÇÃO (24-72 horas)
   □ Notificar clientes afetados
   □ Notificar ANPD (LGPD) - 72h
   □ Comunicado público (se necessário)

6. PÓS-INCIDENTE (1 semana)
   □ Post-mortem detalhado
   □ Atualizar runbooks
   □ Treinamento da equipe
   □ Implementar prevenções
```

### 3. Contacts de Emergência

```yaml
# emergency_contacts.yaml

incident_commander:
  name: "Tech Lead"
  phone: "+55 XX XXXXX-XXXX"
  email: "lead@sentinel.com"

security_team:
  - name: "Security Engineer"
    phone: "+55 XX XXXXX-XXXX"
    email: "security@sentinel.com"

legal_team:
  - name: "Legal Counsel"
    phone: "+55 XX XXXXX-XXXX"
    email: "legal@sentinel.com"

external:
  - name: "Cyber Security Firm"
    phone: "+55 XX XXXXX-XXXX"
    email: "response@cybersec.com"

  - name: "ANPD (LGPD)"
    email: "atendimento@anpd.gov.br"
    website: "https://www.gov.br/anpd"
```

---

## 📈 ROADMAP DE IMPLEMENTAÇÃO

### Fase 1: Fundação (Mês 1-2)
- [ ] Implementar autenticação JWT com tenant_id
- [ ] Adicionar tenant_id em todas as tabelas
- [ ] Implementar middleware de tenant
- [ ] Database per tenant (setup inicial)
- [ ] Logging estruturado
- [ ] HTTPS obrigatório

### Fase 2: Hardening (Mês 3)
- [ ] Row-Level Security no PostgreSQL
- [ ] WAF (ModSecurity)
- [ ] Rate limiting por tenant
- [ ] Backup automatizado por tenant
- [ ] Monitoramento básico (Prometheus)

### Fase 3: Compliance (Mês 4)
- [ ] Sistema de consentimento LGPD
- [ ] Endpoints de direitos do titular
- [ ] Anonimização de dados
- [ ] Política de retenção
- [ ] Documentação de privacidade

### Fase 4: Scale (Mês 5-6)
- [ ] Load balancer
- [ ] Auto-scaling
- [ ] CDN (CloudFlare)
- [ ] Redis para cache
- [ ] Database read replicas

### Fase 5: Advanced Security (Mês 7-8)
- [ ] SIEM (ELK Stack)
- [ ] Anomaly detection
- [ ] Penetration testing
- [ ] Bug bounty program
- [ ] SOC 2 compliance (se necessário)

---

## 💰 CUSTOS ESTIMADOS

### Infrastructure (Monthly)

| Componente | Custo/mês (USD) | Observação |
|------------|-----------------|------------|
| VPS (3x app servers) | $150 | DigitalOcean/AWS |
| Database (RDS Multi-AZ) | $200 | PostgreSQL |
| Load Balancer | $30 | AWS ELB |
| CDN (CloudFlare Pro) | $20 | Pro plan |
| Monitoring (Datadog) | $100 | APM + Logs |
| Backup (S3) | $50 | 1TB/mês |
| WAF | $50 | AWS WAF |
| **TOTAL** | **~$600/mês** | Base para 100 tenants |

### Security Tools (Monthly)

| Tool | Custo/mês | Observação |
|------|-----------|------------|
| Sentry (Error tracking) | $26 | Team plan |
| Penetration Testing | $500 | Quarterly |
| SSL Certificates | $0 | Let's Encrypt |
| **TOTAL** | **~$150/mês** | + $500 trimestral |

**TOTAL MENSAL: ~$750**
**TOTAL ANUAL: ~$11.000 + $2.000 = $13.000**

---

## ✅ CHECKLIST DE SEGURANÇA PARA ESCALA

### Autenticação e Autorização
- [ ] JWT com tenant_id
- [ ] Verificação de tenant em cada request
- [ ] Row-Level Security no DB
- [ ] Revogação de tokens
- [ ] 2FA para admins
- [ ] OAuth2/SSO para clientes

### Isolamento de Dados
- [ ] Database per tenant OU schemas separados
- [ ] tenant_id em todas as tabelas
- [ ] Validação de tenant em queries
- [ ] Storage segregado por tenant
- [ ] Backups separados por tenant

### Compliance
- [ ] Consentimento LGPD
- [ ] Política de privacidade
- [ ] Termos de uso
- [ ] DPO designado
- [ ] Processo de DSAR (Data Subject Access Request)
- [ ] Retenção e exclusão de dados

### Infraestrutura
- [ ] HTTPS everywhere
- [ ] WAF configurado
- [ ] DDoS protection
- [ ] Load balancing
- [ ] Auto-scaling
- [ ] Disaster recovery

### Monitoramento
- [ ] Logs centralizados
- [ ] Métricas de negócio
- [ ] Alertas de segurança
- [ ] Dashboards de saúde
- [ ] Auditoria completa

### Resposta a Incidentes
- [ ] Runbooks documentados
- [ ] Contatos de emergência
- [ ] Processo de escalação
- [ ] Backup e restore testados
- [ ] Post-mortem template

---

**Status:** 📋 **PLANEJAMENTO COMPLETO**
**Próximo Passo:** Implementar Fase 1 do Roadmap
**Estimativa:** 8 meses para full compliance e scale
