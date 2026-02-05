# 🔄 Guia de Migração: MVP Single-Tenant → Multi-Tenant SaaS

## 📋 VISÃO GERAL

Este guia detalha como migrar o SENTINEL MVP1 (single-tenant) para arquitetura multi-tenant SaaS, permitindo servir múltiplos clientes em uma única infraestrutura.

**Tempo estimado:** 3-4 semanas
**Complexidade:** Alta
**Impacto:** Transformacional

---

## 🎯 OBJETIVOS DA MIGRAÇÃO

### Antes (MVP Single-Tenant)
- ❌ Um único usuário/apartamento
- ❌ Banco de dados compartilhado sem isolamento
- ❌ Sem autenticação multi-usuário
- ❌ Deploy manual em servidor único
- ❌ Escalabilidade limitada

### Depois (Multi-Tenant SaaS)
- ✅ Múltiplos clientes (tenants) isolados
- ✅ Dados completamente segregados
- ✅ Autenticação JWT com tenant_id
- ✅ Auto-scaling e alta disponibilidade
- ✅ Escalabilidade ilimitada

---

## 📊 ESTRATÉGIA DE MIGRAÇÃO

### Opção Escolhida: Database-Per-Tenant

**Vantagens:**
- ✅ Isolamento total de dados (máxima segurança)
- ✅ Backup/restore individual por cliente
- ✅ Compliance facilitado (LGPD/GDPR)
- ✅ Migrações independentes
- ✅ Performance previsível por tenant

**Desvantagens:**
- ⚠️ Mais complexo de gerenciar (mitigado com automação)
- ⚠️ Custos de infraestrutura maiores (mas escalável)

**Por que não Schema-Per-Tenant ou Shared-Schema?**
- Schema-per-tenant: complexidade de migrations, limite de schemas do PostgreSQL
- Shared-schema: risco de vazamento de dados, performance imprevisível

---

## 🗺️ ROADMAP DE MIGRAÇÃO

### Fase 1: Preparação (Semana 1)
- [ ] Criar branch `feature/multi-tenant`
- [ ] Setup ambiente de desenvolvimento multi-tenant
- [ ] Criar banco de dados de controle (tenant registry)
- [ ] Planejar estrutura de dados

### Fase 2: Backend Core (Semana 2)
- [ ] Implementar sistema de tenants
- [ ] Criar middleware de tenant resolution
- [ ] Adicionar autenticação JWT com tenant_id
- [ ] Implementar conexões dinâmicas ao banco

### Fase 3: Migração de Dados (Semana 3)
- [ ] Criar scripts de migração
- [ ] Migrar dados do MVP para tenant demo
- [ ] Validar integridade dos dados
- [ ] Criar tenant de teste

### Fase 4: Frontend e Testes (Semana 4)
- [ ] Adaptar frontend para multi-tenant
- [ ] Criar página de cadastro/onboarding
- [ ] Testes de isolamento
- [ ] Deploy em staging

---

## 🏗️ ARQUITETURA MULTI-TENANT

### Estrutura de Bancos de Dados

```
PostgreSQL Server
├── sentinel_control (DB de controle)
│   ├── tenants (registro de clientes)
│   ├── users (usuários globais)
│   └── subscriptions (assinaturas)
│
├── tenant_abc123 (DB do cliente 1)
│   ├── properties
│   ├── bookings
│   ├── calendar_events
│   └── ... (todas as tabelas do MVP)
│
├── tenant_def456 (DB do cliente 2)
│   ├── properties
│   ├── bookings
│   └── ...
│
└── tenant_ghi789 (DB do cliente 3)
    └── ...
```

### Fluxo de Request Multi-Tenant

```
1. Request chega → https://api.sentinel.com.br/api/bookings
                   Header: Authorization: Bearer <JWT>

2. Middleware extrai tenant_id do JWT
   → tenant_id = "abc123"

3. Connection Manager seleciona DB correto
   → Conecta em "tenant_abc123"

4. Query executa no banco do tenant
   → SELECT * FROM bookings WHERE property_id = ?

5. Response retorna apenas dados do tenant
   → Impossível acessar dados de outros tenants
```

---

## 💻 IMPLEMENTAÇÃO PASSO A PASSO

### PASSO 1: Criar Banco de Controle

```sql
-- sentinel_control/schema.sql
CREATE DATABASE sentinel_control;

\c sentinel_control;

-- Tabela de Tenants (Clientes)
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(50) UNIQUE NOT NULL,  -- abc123, def456
    company_name VARCHAR(200) NOT NULL,
    database_name VARCHAR(100) UNIQUE NOT NULL,  -- tenant_abc123

    -- Assinatura
    plan VARCHAR(50) NOT NULL,  -- free, starter, professional, enterprise
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, suspended, canceled
    trial_ends_at TIMESTAMP,
    subscription_ends_at TIMESTAMP,

    -- Configurações
    settings JSONB DEFAULT '{}',

    -- Metadados
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CHECK (slug ~ '^[a-z0-9]{6,50}$'),
    CHECK (status IN ('active', 'trial', 'suspended', 'canceled'))
);

-- Índices
CREATE INDEX idx_tenants_slug ON tenants(slug);
CREATE INDEX idx_tenants_status ON tenants(status);

-- Tabela de Usuários (Global)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,

    full_name VARCHAR(200),
    role VARCHAR(50) NOT NULL DEFAULT 'user',  -- admin, user, viewer

    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,

    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Índices
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);

-- Tabela de Assinaturas
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    plan VARCHAR(50) NOT NULL,  -- free, starter, professional, enterprise
    status VARCHAR(20) NOT NULL,  -- active, canceled, past_due

    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,

    price_monthly DECIMAL(10, 2),

    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Auditoria de Ações
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),

    action VARCHAR(100) NOT NULL,  -- login, create_booking, delete_property
    resource_type VARCHAR(50),  -- booking, property, user
    resource_id VARCHAR(100),

    ip_address INET,
    user_agent TEXT,

    details JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id, created_at);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at);
```

---

### PASSO 2: Criar Models do Sistema de Tenants

```python
# app/models/tenant.py
from sqlalchemy import Column, String, DateTime, Boolean, JSON, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {'schema': 'public'}  # sentinel_control database

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    company_name = Column(String(200), nullable=False)
    database_name = Column(String(100), unique=True, nullable=False)

    # Subscription
    plan = Column(String(50), nullable=False, default='trial')
    status = Column(String(20), nullable=False, default='trial')
    trial_ends_at = Column(DateTime, nullable=True)
    subscription_ends_at = Column(DateTime, nullable=True)

    # Settings
    settings = Column(JSON, default={})

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="tenant", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("slug ~ '^[a-z0-9]{6,50}$'", name='slug_format'),
        CheckConstraint("status IN ('active', 'trial', 'suspended', 'canceled')", name='valid_status'),
    )

    @property
    def is_active(self) -> bool:
        """Verifica se tenant está ativo"""
        if self.status == 'canceled':
            return False

        if self.status == 'trial' and self.trial_ends_at:
            return datetime.utcnow() < self.trial_ends_at

        if self.subscription_ends_at:
            return datetime.utcnow() < self.subscription_ends_at

        return self.status == 'active'

    @property
    def remaining_trial_days(self) -> int:
        """Dias restantes de trial"""
        if not self.trial_ends_at:
            return 0

        delta = self.trial_ends_at - datetime.utcnow()
        return max(0, delta.days)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(200))
    role = Column(String(50), nullable=False, default='user')

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="users")


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)

    plan = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)

    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False)

    price_monthly = Column(Numeric(10, 2))

    stripe_subscription_id = Column(String(255))
    stripe_customer_id = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="subscriptions")
```

---

### PASSO 3: Tenant Resolution Middleware

```python
# app/middleware/tenant.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import jwt
from typing import Optional

from app.core.config import settings
from app.models.tenant import Tenant
from app.database import SessionLocal

class TenantMiddleware:
    """
    Middleware que resolve o tenant atual baseado no JWT.
    Adiciona tenant_id e database_name ao request.state
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        # Rotas públicas que não precisam de tenant
        public_routes = ["/", "/health", "/docs", "/openapi.json", "/api/auth/register", "/api/auth/login"]
        if request.url.path in public_routes or request.url.path.startswith("/static"):
            await self.app(scope, receive, send)
            return

        try:
            # Extrair token do header Authorization
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token de autenticação não fornecido"
                )

            token = auth_header.replace("Bearer ", "")

            # Decodificar JWT
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            tenant_id = payload.get("tenant_id")
            if not tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido: tenant_id não encontrado"
                )

            # Buscar tenant no banco de controle
            db = SessionLocal()  # Conexão com sentinel_control
            try:
                tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

                if not tenant:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Tenant não encontrado"
                    )

                if not tenant.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Assinatura expirada ou cancelada"
                    )

                # Adicionar informações do tenant ao request.state
                scope["state"] = {
                    "tenant_id": str(tenant.id),
                    "tenant_slug": tenant.slug,
                    "database_name": tenant.database_name,
                    "tenant_plan": tenant.plan,
                    "user_id": payload.get("sub"),  # user_id do JWT
                }

            finally:
                db.close()

        except jwt.ExpiredSignatureError:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token expirado"}
            )
            await response(scope, receive, send)
            return

        except jwt.InvalidTokenError:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido"}
            )
            await response(scope, receive, send)
            return

        except HTTPException as e:
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
```

---

### PASSO 4: Database Connection Manager

```python
# app/database/tenant_manager.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Dict, Optional
import threading

from app.core.config import settings

class TenantDatabaseManager:
    """
    Gerencia conexões dinâmicas aos bancos de dados dos tenants.
    Mantém pool de conexões por tenant para performance.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._engines: Dict[str, any] = {}
        self._session_makers: Dict[str, sessionmaker] = {}
        self._initialized = True

    def get_engine(self, database_name: str):
        """
        Retorna engine para o banco de dados do tenant.
        Cria e cacheia se não existir.
        """
        if database_name not in self._engines:
            # Criar engine para o tenant
            database_url = settings.DATABASE_URL.replace(
                settings.DATABASE_NAME,  # sentinel (default)
                database_name  # tenant_abc123
            )

            engine = create_engine(
                database_url,
                pool_size=5,  # Conexões por tenant
                max_overflow=10,
                pool_pre_ping=True,  # Verificar conexão antes de usar
                pool_recycle=3600,  # Reciclar conexões a cada 1h
                echo=settings.DEBUG,
            )

            self._engines[database_name] = engine
            self._session_makers[database_name] = sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False
            )

        return self._engines[database_name]

    def get_session(self, database_name: str) -> Session:
        """Retorna sessão para o banco do tenant"""
        if database_name not in self._session_makers:
            self.get_engine(database_name)

        return self._session_makers[database_name]()

    @contextmanager
    def get_db(self, database_name: str):
        """
        Context manager para sessão do banco do tenant.

        Usage:
            with tenant_manager.get_db('tenant_abc123') as db:
                bookings = db.query(Booking).all()
        """
        db = self.get_session(database_name)
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def close_tenant_connections(self, database_name: str):
        """Fecha todas as conexões de um tenant específico"""
        if database_name in self._engines:
            self._engines[database_name].dispose()
            del self._engines[database_name]
            del self._session_makers[database_name]

    def close_all_connections(self):
        """Fecha todas as conexões (shutdown)"""
        for engine in self._engines.values():
            engine.dispose()

        self._engines.clear()
        self._session_makers.clear()


# Singleton global
tenant_db_manager = TenantDatabaseManager()


# Dependency para usar em rotas FastAPI
def get_tenant_db(request: Request):
    """
    Dependency que retorna DB session do tenant atual.

    Usage em rotas:
        @app.get("/api/bookings")
        def list_bookings(db: Session = Depends(get_tenant_db)):
            return db.query(Booking).all()
    """
    database_name = request.state.database_name

    with tenant_db_manager.get_db(database_name) as db:
        yield db
```

---

### PASSO 5: Criar Tenant Service

```python
# app/services/tenant_service.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
import secrets
import string
from typing import Optional
from datetime import datetime, timedelta

from app.models.tenant import Tenant, User, Subscription
from app.database import Base
from app.core.config import settings
from app.core.security import get_password_hash

class TenantService:
    """
    Serviço para gerenciar criação e configuração de tenants.
    """

    def __init__(self, control_db: Session):
        """
        Args:
            control_db: Session do banco sentinel_control
        """
        self.control_db = control_db

    def generate_slug(self, company_name: str) -> str:
        """
        Gera slug único para o tenant.

        Exemplo:
            "Minha Empresa" → "minhaempresa" + random chars → "minhaempresa7a2b"
        """
        # Normalizar nome
        base_slug = company_name.lower()
        base_slug = ''.join(c for c in base_slug if c.isalnum())
        base_slug = base_slug[:20]  # Limitar tamanho

        # Adicionar caracteres aleatórios
        random_suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        slug = f"{base_slug}{random_suffix}"

        # Verificar unicidade
        while self.control_db.query(Tenant).filter(Tenant.slug == slug).first():
            random_suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            slug = f"{base_slug}{random_suffix}"

        return slug

    def create_tenant_database(self, database_name: str):
        """
        Cria banco de dados PostgreSQL para o tenant.
        Executa todas as migrations.
        """
        # Conectar ao PostgreSQL (sem database específico)
        admin_url = settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
        admin_engine = create_engine(admin_url, isolation_level='AUTOCOMMIT')

        # Criar database
        with admin_engine.connect() as conn:
            # Verificar se já existe
            result = conn.execute(text(
                f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"
            ))

            if not result.fetchone():
                conn.execute(text(f'CREATE DATABASE {database_name}'))

        admin_engine.dispose()

        # Criar tabelas no novo banco
        tenant_url = settings.DATABASE_URL.replace(
            settings.DATABASE_NAME,
            database_name
        )
        tenant_engine = create_engine(tenant_url)

        # Criar todas as tabelas (usando models do MVP)
        Base.metadata.create_all(bind=tenant_engine)

        tenant_engine.dispose()

    def create_tenant(
        self,
        company_name: str,
        admin_email: str,
        admin_password: str,
        admin_name: str,
        plan: str = "trial"
    ) -> Tenant:
        """
        Cria novo tenant completo:
        1. Registro no sentinel_control
        2. Banco de dados dedicado
        3. Usuário admin
        4. Subscription trial

        Returns:
            Tenant criado
        """
        # 1. Gerar slug e database_name
        slug = self.generate_slug(company_name)
        database_name = f"tenant_{slug}"

        # 2. Criar registro do tenant
        tenant = Tenant(
            slug=slug,
            company_name=company_name,
            database_name=database_name,
            plan=plan,
            status='trial' if plan == 'trial' else 'active',
            trial_ends_at=datetime.utcnow() + timedelta(days=14) if plan == 'trial' else None,
        )

        self.control_db.add(tenant)
        self.control_db.flush()  # Gerar ID

        # 3. Criar banco de dados do tenant
        try:
            self.create_tenant_database(database_name)
        except Exception as e:
            self.control_db.rollback()
            raise Exception(f"Erro ao criar banco de dados: {str(e)}")

        # 4. Criar usuário admin
        admin_user = User(
            tenant_id=tenant.id,
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            full_name=admin_name,
            role='admin',
            is_active=True,
            is_verified=True,
        )

        self.control_db.add(admin_user)

        # 5. Criar subscription
        subscription = Subscription(
            tenant_id=tenant.id,
            plan=plan,
            status='trialing' if plan == 'trial' else 'active',
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=14 if plan == 'trial' else 30),
            price_monthly=0 if plan == 'trial' else self._get_plan_price(plan),
        )

        self.control_db.add(subscription)

        # Commit tudo
        self.control_db.commit()
        self.control_db.refresh(tenant)

        return tenant

    def _get_plan_price(self, plan: str) -> float:
        """Retorna preço do plano"""
        prices = {
            'free': 0,
            'trial': 0,
            'starter': 49.00,
            'professional': 149.00,
            'enterprise': 0,  # Custom
        }
        return prices.get(plan, 0)

    def delete_tenant(self, tenant_id: str):
        """
        Deleta tenant completamente:
        1. Remove banco de dados
        2. Remove registros do sentinel_control
        """
        tenant = self.control_db.query(Tenant).filter(Tenant.id == tenant_id).first()

        if not tenant:
            raise ValueError("Tenant não encontrado")

        database_name = tenant.database_name

        # 1. Deletar banco de dados
        admin_url = settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
        admin_engine = create_engine(admin_url, isolation_level='AUTOCOMMIT')

        with admin_engine.connect() as conn:
            # Encerrar conexões ativas
            conn.execute(text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{database_name}'
                AND pid <> pg_backend_pid()
            """))

            # Deletar database
            conn.execute(text(f'DROP DATABASE IF EXISTS {database_name}'))

        admin_engine.dispose()

        # 2. Deletar registros (cascade deleta users e subscriptions)
        self.control_db.delete(tenant)
        self.control_db.commit()
```

---

### PASSO 6: API de Registro (Onboarding)

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from datetime import timedelta

from app.database import get_db  # sentinel_control
from app.services.tenant_service import TenantService
from app.core.security import create_access_token
from app.models.tenant import User, Tenant

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    company_name: str
    admin_name: str
    admin_email: EmailStr
    admin_password: str

    @validator('admin_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v

    @validator('company_name')
    def validate_company(cls, v):
        if len(v) < 3:
            raise ValueError('Nome da empresa deve ter no mínimo 3 caracteres')
        return v

class RegisterResponse(BaseModel):
    tenant_id: str
    tenant_slug: str
    access_token: str
    token_type: str = "bearer"
    trial_ends_at: str

@router.post("/register", response_model=RegisterResponse)
def register_tenant(
    data: RegisterRequest,
    db: Session = Depends(get_db)  # sentinel_control
):
    """
    Registra novo tenant (cliente) no sistema.

    Fluxo:
    1. Valida dados
    2. Cria tenant + database
    3. Cria usuário admin
    4. Retorna JWT para login automático
    """
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == data.admin_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Criar tenant
    tenant_service = TenantService(db)

    try:
        tenant = tenant_service.create_tenant(
            company_name=data.company_name,
            admin_email=data.admin_email,
            admin_password=data.admin_password,
            admin_name=data.admin_name,
            plan='trial'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )

    # Buscar usuário criado
    admin_user = db.query(User).filter(
        User.tenant_id == tenant.id,
        User.email == data.admin_email
    ).first()

    # Gerar JWT
    access_token = create_access_token(
        data={
            "sub": str(admin_user.id),
            "tenant_id": str(tenant.id),
            "email": admin_user.email,
            "role": admin_user.role,
        },
        expires_delta=timedelta(days=7)
    )

    return RegisterResponse(
        tenant_id=str(tenant.id),
        tenant_slug=tenant.slug,
        access_token=access_token,
        trial_ends_at=tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else "",
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    tenant_id: str
    tenant_slug: str

@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login de usuário existente"""
    from app.core.security import verify_password

    # Buscar usuário
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    # Verificar tenant
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()

    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Assinatura expirada ou cancelada"
        )

    # Atualizar last_login
    user.last_login_at = datetime.utcnow()
    db.commit()

    # Gerar JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "tenant_id": str(tenant.id),
            "email": user.email,
            "role": user.role,
        },
        expires_delta=timedelta(days=7)
    )

    return LoginResponse(
        access_token=access_token,
        user_id=str(user.id),
        tenant_id=str(tenant.id),
        tenant_slug=tenant.slug,
    )
```

---

### PASSO 7: Adaptar Rotas Existentes

```python
# Exemplo: app/api/v1/bookings.py (ANTES)
from app.database import get_db

@router.get("/api/bookings")
def list_bookings(db: Session = Depends(get_db)):  # ❌ Banco único
    return db.query(Booking).all()  # ❌ Retorna TODOS os bookings


# Exemplo: app/api/v1/bookings.py (DEPOIS)
from app.database.tenant_manager import get_tenant_db

@router.get("/api/bookings")
def list_bookings(
    request: Request,
    db: Session = Depends(get_tenant_db)  # ✅ Banco do tenant
):
    # ✅ Só retorna bookings do tenant atual
    # request.state.tenant_id foi injetado pelo middleware
    return db.query(Booking).all()
```

**Mudanças necessárias em TODAS as rotas:**
1. Trocar `get_db` por `get_tenant_db`
2. Adicionar `request: Request` nos parâmetros (se precisar acessar tenant_id)
3. Remover filtros manuais por property_id (isolamento automático por DB)

---

### PASSO 8: Script de Migração de Dados

```python
# scripts/migrate_mvp_to_tenant.py
"""
Script para migrar dados do MVP single-tenant para o primeiro tenant demo.

Usage:
    python scripts/migrate_mvp_to_tenant.py
"""
import sys
from pathlib import Path

# Adicionar app ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.tenant_service import TenantService
from app.models import Property, Booking, CalendarEvent  # Models do MVP

def migrate():
    # 1. Conectar ao sentinel_control
    control_engine = create_engine(settings.DATABASE_URL_CONTROL)
    ControlSession = sessionmaker(bind=control_engine)
    control_db = ControlSession()

    # 2. Criar tenant demo
    tenant_service = TenantService(control_db)

    print("🚀 Criando tenant demo...")
    tenant = tenant_service.create_tenant(
        company_name="Demo MVP",
        admin_email="admin@demo.com",
        admin_password="demo123456",
        admin_name="Admin Demo",
        plan="professional"
    )

    print(f"✅ Tenant criado: {tenant.slug}")
    print(f"   Database: {tenant.database_name}")

    # 3. Conectar ao banco do MVP (antigo)
    mvp_engine = create_engine(settings.DATABASE_URL)  # sentinel.db
    MVPSession = sessionmaker(bind=mvp_engine)
    mvp_db = MVPSession()

    # 4. Conectar ao banco do tenant (novo)
    tenant_url = settings.DATABASE_URL.replace(
        settings.DATABASE_NAME,
        tenant.database_name
    )
    tenant_engine = create_engine(tenant_url)
    TenantSession = sessionmaker(bind=tenant_engine)
    tenant_db = TenantSession()

    # 5. Migrar Properties
    print("\n📦 Migrando Properties...")
    properties = mvp_db.query(Property).all()

    for prop in properties:
        # Criar cópia no banco do tenant
        new_prop = Property(
            id=prop.id,
            name=prop.name,
            address=prop.address,
            airbnb_property_id=prop.airbnb_property_id,
            booking_property_id=prop.booking_property_id,
            created_at=prop.created_at,
            updated_at=prop.updated_at,
        )
        tenant_db.add(new_prop)

    tenant_db.commit()
    print(f"✅ {len(properties)} properties migradas")

    # 6. Migrar Bookings
    print("\n📦 Migrando Bookings...")
    bookings = mvp_db.query(Booking).all()

    for booking in bookings:
        new_booking = Booking(
            id=booking.id,
            property_id=booking.property_id,
            platform=booking.platform,
            platform_booking_id=booking.platform_booking_id,
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            status=booking.status,
            total_price=booking.total_price,
            created_at=booking.created_at,
            updated_at=booking.updated_at,
        )
        tenant_db.add(new_booking)

    tenant_db.commit()
    print(f"✅ {len(bookings)} bookings migradas")

    # 7. Migrar Calendar Events
    print("\n📦 Migrando Calendar Events...")
    events = mvp_db.query(CalendarEvent).all()

    for event in events:
        new_event = CalendarEvent(
            id=event.id,
            property_id=event.property_id,
            booking_id=event.booking_id,
            event_type=event.event_type,
            start_date=event.start_date,
            end_date=event.end_date,
            title=event.title,
            description=event.description,
            created_at=event.created_at,
        )
        tenant_db.add(new_event)

    tenant_db.commit()
    print(f"✅ {len(events)} eventos migrados")

    # 8. Fechar conexões
    mvp_db.close()
    tenant_db.close()
    control_db.close()

    print("\n" + "="*50)
    print("✅ MIGRAÇÃO CONCLUÍDA!")
    print("="*50)
    print(f"\nTenant: {tenant.company_name}")
    print(f"Slug: {tenant.slug}")
    print(f"Database: {tenant.database_name}")
    print(f"\nCredenciais:")
    print(f"  Email: admin@demo.com")
    print(f"  Senha: demo123456")
    print("\nFaça login em: http://localhost:3000/login")

if __name__ == "__main__":
    migrate()
```

---

## 🧪 TESTES DE ISOLAMENTO

```python
# tests/test_tenant_isolation.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.tenant_service import TenantService
from app.database import get_db

@pytest.fixture
def tenant1():
    """Cria tenant 1 para testes"""
    db = next(get_db())
    service = TenantService(db)

    tenant = service.create_tenant(
        company_name="Tenant 1",
        admin_email="admin1@test.com",
        admin_password="test123456",
        admin_name="Admin 1"
    )

    yield tenant

    # Cleanup
    service.delete_tenant(tenant.id)

@pytest.fixture
def tenant2():
    """Cria tenant 2 para testes"""
    db = next(get_db())
    service = TenantService(db)

    tenant = service.create_tenant(
        company_name="Tenant 2",
        admin_email="admin2@test.com",
        admin_password="test123456",
        admin_name="Admin 2"
    )

    yield tenant

    service.delete_tenant(tenant.id)

def test_tenant_isolation(tenant1, tenant2):
    """
    Testa que Tenant 1 NÃO pode acessar dados do Tenant 2.
    """
    client = TestClient(app)

    # 1. Login no Tenant 1
    response = client.post("/api/auth/login", json={
        "email": "admin1@test.com",
        "password": "test123456"
    })
    token1 = response.json()["access_token"]

    # 2. Criar property no Tenant 1
    response = client.post(
        "/api/properties",
        json={"name": "Property Tenant 1"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 201
    property1_id = response.json()["id"]

    # 3. Login no Tenant 2
    response = client.post("/api/auth/login", json={
        "email": "admin2@test.com",
        "password": "test123456"
    })
    token2 = response.json()["access_token"]

    # 4. Tentar acessar property do Tenant 1 usando token do Tenant 2
    response = client.get(
        f"/api/properties/{property1_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    # ✅ DEVE retornar 404 (não encontrado) ou 403 (proibido)
    assert response.status_code in [404, 403]

    # 5. Listar properties do Tenant 2 (deve estar vazio)
    response = client.get(
        "/api/properties",
        headers={"Authorization": f"Bearer {token2}"}
    )

    # ✅ DEVE retornar lista vazia
    assert response.json() == []

def test_jwt_tenant_mismatch(tenant1):
    """
    Testa que não é possível usar JWT de um tenant para acessar outro.
    """
    client = TestClient(app)

    # Login
    response = client.post("/api/auth/login", json={
        "email": "admin1@test.com",
        "password": "test123456"
    })
    token = response.json()["access_token"]

    # Manipular JWT (trocar tenant_id)
    import jwt
    from app.core.config import settings

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    payload["tenant_id"] = "00000000-0000-0000-0000-000000000000"  # Tenant inexistente

    fake_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Tentar usar token manipulado
    response = client.get(
        "/api/properties",
        headers={"Authorization": f"Bearer {fake_token}"}
    )

    # ✅ DEVE retornar 404 (tenant não encontrado)
    assert response.status_code == 404
```

---

## 📋 CHECKLIST DE MIGRAÇÃO

### Preparação
- [ ] Criar branch `feature/multi-tenant`
- [ ] Backup completo do banco MVP
- [ ] Criar `sentinel_control` database
- [ ] Executar schema.sql no sentinel_control
- [ ] Testar em ambiente local

### Backend
- [ ] Criar models (Tenant, User, Subscription)
- [ ] Implementar TenantMiddleware
- [ ] Implementar TenantDatabaseManager
- [ ] Criar TenantService
- [ ] Criar API de registro/login
- [ ] Adaptar TODAS as rotas para usar get_tenant_db
- [ ] Adicionar validações de tenant ativo

### Migração de Dados
- [ ] Executar script migrate_mvp_to_tenant.py
- [ ] Validar dados migrados
- [ ] Criar tenant de testes
- [ ] Popular com dados fake

### Frontend
- [ ] Criar página de registro (/register)
- [ ] Adaptar página de login
- [ ] Salvar tenant_id no localStorage
- [ ] Incluir tenant_id em todas as requests
- [ ] Adicionar indicador de tenant na UI

### Testes
- [ ] Testes de isolamento de tenants
- [ ] Testes de JWT com tenant_id
- [ ] Testes de onboarding completo
- [ ] Testes de performance (múltiplos tenants)
- [ ] Testes de segurança (SQL injection, etc)

### Deploy
- [ ] Configurar PostgreSQL em produção
- [ ] Criar sentinel_control em prod
- [ ] Deploy do backend multi-tenant
- [ ] Deploy do frontend adaptado
- [ ] Configurar monitoramento
- [ ] Testar criação de tenant em prod

---

## 🚨 AVISOS IMPORTANTES

### ⚠️ Segurança
- **NUNCA** permitir queries cross-tenant
- **SEMPRE** validar tenant_id no JWT
- **SEMPRE** verificar se tenant está ativo
- Implementar rate limiting por tenant
- Logs de auditoria para ações sensíveis

### ⚠️ Performance
- Monitorar número de conexões ao PostgreSQL
- Ajustar pool_size baseado em número de tenants
- Considerar Redis para cache compartilhado
- Implementar paginação em todas as listagens

### ⚠️ Backup
- Backup automático do sentinel_control (CRÍTICO)
- Backup individual por tenant (facilita restore)
- Testar procedimento de restore regularmente

### ⚠️ Custos
- Cada tenant = 1 database no PostgreSQL
- Monitorar uso de storage
- Considerar archiving de tenants inativos
- Planejar cleanup de trials expirados

---

## 📊 ESTIMATIVA DE RECURSOS

### Desenvolvimento
- **Semana 1:** 30-40 horas (preparação + models)
- **Semana 2:** 30-40 horas (middleware + services)
- **Semana 3:** 20-30 horas (migração + validação)
- **Semana 4:** 20-30 horas (frontend + testes)
- **Total:** 100-140 horas

### Infraestrutura (para 100 tenants)
- **PostgreSQL:** ~20GB storage
- **RAM:** 4-8GB dedicados ao Postgres
- **CPU:** 2-4 cores
- **Conexões:** ~500 simultâneas (5 por tenant)

---

## ✅ CONCLUSÃO

Após essa migração, o SENTINEL estará pronto para:
- ✅ Servir milhares de clientes simultaneamente
- ✅ Isolamento completo de dados (compliance LGPD)
- ✅ Onboarding automatizado (self-service)
- ✅ Escalabilidade horizontal ilimitada
- ✅ Monetização via SaaS

**Próximo passo:** Implementar billing com Stripe para cobranças recorrentes.

---

**Documentação criada em:** 2024
**Versão:** 1.0
**Status:** Pronto para implementação
