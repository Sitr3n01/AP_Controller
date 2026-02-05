# 📘 Documentação Técnica Completa - SENTINEL

**Versão:** 1.0.0 (MVP2)
**Data:** 04/02/2026
**Autor:** Equipe SENTINEL

---

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura](#arquitetura)
3. [Stack Tecnológica](#stack-tecnológica)
4. [Estrutura de Diretórios](#estrutura-de-diretórios)
5. [Banco de Dados](#banco-de-dados)
6. [API REST](#api-rest)
7. [Autenticação e Segurança](#autenticação-e-segurança)
8. [Sincronização de Calendários](#sincronização-de-calendários)
9. [Sistema de Documentos](#sistema-de-documentos)
10. [Sistema de Email](#sistema-de-email)
11. [Bot do Telegram](#bot-do-telegram)
12. [Configurações](#configurações)
13. [Deploy](#deploy)
14. [Monitoramento](#monitoramento)
15. [Troubleshooting](#troubleshooting)

---

## 1. Visão Geral do Sistema

### Propósito

SENTINEL é um sistema completo de gerenciamento automatizado de apartamentos para aluguel de curta temporada. Integra-se com plataformas como Airbnb e Booking.com através de feeds iCal, detecta conflitos de reservas, gera documentos automaticamente e oferece notificações via Telegram e Email.

### Características Principais

- **Sincronização Automática**: Download e parse de feeds iCal a cada 30 minutos
- **Detecção Inteligente de Conflitos**: Identifica sobreposições e duplicatas
- **Geração de Documentos**: Templates DOCX com variáveis dinâmicas
- **Sistema de Email Universal**: Suporte IMAP/SMTP para Gmail, Outlook, Yahoo
- **Notificações Multi-canal**: Telegram + Email
- **API RESTful**: 54 endpoints documentados com FastAPI
- **Autenticação JWT**: Tokens seguros com bcrypt
- **Rate Limiting**: Proteção contra brute force
- **Dashboard Completo**: Estatísticas e métricas em tempo real

---

## 2. Arquitetura

### Padrão Arquitetural

**Arquitetura em Camadas (Layered Architecture)**

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│   (FastAPI Routers + Bot Telegram)      │
├─────────────────────────────────────────┤
│          Service Layer                  │
│   (Business Logic + Integrations)       │
├─────────────────────────────────────────┤
│          Data Access Layer              │
│        (SQLAlchemy Models)              │
├─────────────────────────────────────────┤
│          Infrastructure Layer           │
│    (Database + External APIs)           │
└─────────────────────────────────────────┘
```

### Componentes Principais

```
SENTINEL/
│
├── API REST (FastAPI)
│   ├── 8 Routers
│   ├── 54 Endpoints
│   └── Swagger UI em /docs
│
├── Services (Business Logic)
│   ├── CalendarService - Sincronização iCal
│   ├── ConflictDetector - Detecção de conflitos
│   ├── DocumentService - Geração de documentos
│   ├── EmailService - Envio/recebimento emails
│   ├── NotificationService - Multi-canal
│   └── BackupService - Backup automático
│
├── Database (SQLite)
│   ├── 8 Models (SQLAlchemy)
│   └── Relational Integrity
│
├── Bot Telegram
│   ├── 9 Comandos
│   └── Notificações Push
│
└── Frontend (React)
    ├── Dashboard
    ├── Calendário
    ├── Conflitos
    └── Estatísticas
```

---

## 3. Stack Tecnológica

### Backend

| Componente | Tecnologia | Versão | Propósito |
|------------|------------|--------|-----------|
| **Framework** | FastAPI | 0.115+ | API REST assíncrona |
| **Language** | Python | 3.11+ | Linguagem principal |
| **Database** | SQLite | 3.x | Banco de dados local |
| **ORM** | SQLAlchemy | 2.0+ | Mapeamento objeto-relacional |
| **Validation** | Pydantic | 2.10+ | Validação de dados |
| **Auth** | python-jose | 3.3+ | JWT tokens |
| **Password** | passlib[bcrypt] | 1.7+ | Hashing de senhas |
| **HTTP Client** | httpx | 0.28+ | Requisições HTTP assíncronas |
| **Calendar** | icalendar | 6.1+ | Parse de iCal feeds |
| **Documents** | python-docx | 1.2+ | Geração de DOCX |
| **Templates** | docxtpl + Jinja2 | Latest | Templates dinâmicos |
| **Email SMTP** | aiosmtplib | 3.0+ | Envio assíncrono |
| **Email IMAP** | aioimaplib | 1.0+ | Leitura assíncrona |
| **Telegram** | python-telegram-bot | 21.0+ | Bot Telegram |
| **Logging** | loguru | 0.7+ | Logs estruturados |
| **Rate Limit** | slowapi | 0.1+ | Proteção API |

### Frontend

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| **Framework** | React | 18.x |
| **Language** | TypeScript | 5.x |
| **Build Tool** | Vite | 5.x |
| **HTTP Client** | Axios | 1.x |
| **Router** | React Router | 6.x |
| **Icons** | Lucide React | Latest |
| **Charts** | Recharts | 2.x |
| **Calendar** | FullCalendar | 6.x |

### Infraestrutura

| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| **Web Server** | Uvicorn | ASGI server |
| **Reverse Proxy** | Nginx | Proxy reverso e SSL |
| **SSL** | Let's Encrypt | Certificados HTTPS |
| **Container** | Docker | Containerização |
| **Orchestration** | Docker Compose | Multi-container |
| **Process Manager** | Systemd | Gerenciamento de serviços |
| **Firewall** | UFW | Firewall Linux |
| **Intrusion Prevention** | Fail2ban | Proteção contra ataques |

---

## 4. Estrutura de Diretórios

```
AP_Controller/
│
├── app/                            # Aplicação Python
│   ├── __init__.py
│   ├── main.py                     # Entry point FastAPI
│   ├── config.py                   # Configurações (Pydantic Settings)
│   ├── constants.py                # Constantes globais
│   │
│   ├── api/                        # Endpoints API versionados
│   │   └── v1/
│   │       ├── auth.py             # Autenticação (login, register)
│   │       └── health.py           # Health checks
│   │
│   ├── core/                       # Lógica de negócio central
│   │   ├── backup.py               # Sistema de backup
│   │   ├── calendar_sync.py        # Engine de sincronização
│   │   ├── conflict_detector.py    # Detecção de conflitos
│   │   ├── environments.py         # Configurações por ambiente
│   │   └── security.py             # Utils de segurança
│   │
│   ├── database/                   # Camada de dados
│   │   ├── connection.py           # Engine SQLAlchemy
│   │   └── session.py              # Session management
│   │
│   ├── middleware/                 # Middlewares HTTP
│   │   ├── auth.py                 # Autenticação JWT
│   │   └── security_headers.py     # Security headers HTTP
│   │
│   ├── models/                     # SQLAlchemy Models
│   │   ├── base.py                 # Base declarativa
│   │   ├── booking.py              # Reservas
│   │   ├── booking_conflict.py     # Conflitos
│   │   ├── calendar_source.py      # Fontes de calendário
│   │   ├── guest.py                # Hóspedes
│   │   ├── property.py             # Imóveis
│   │   ├── sync_action.py          # Ações de sincronização
│   │   ├── sync_log.py             # Logs de sync
│   │   └── user.py                 # Usuários do sistema
│   │
│   ├── routers/                    # FastAPI Routers
│   │   ├── bookings.py             # CRUD de reservas
│   │   ├── calendar.py             # Sincronização de calendários
│   │   ├── conflicts.py            # Gerenciamento de conflitos
│   │   ├── documents.py            # Geração de documentos
│   │   ├── emails.py               # Sistema de email
│   │   ├── statistics.py           # Estatísticas e métricas
│   │   └── sync_actions.py         # Ações pendentes
│   │
│   ├── schemas/                    # Pydantic Schemas
│   │   ├── auth.py                 # Schemas de autenticação
│   │   ├── booking.py              # Schemas de reservas
│   │   ├── document.py             # Schemas de documentos
│   │   └── email.py                # Schemas de email
│   │
│   ├── services/                   # Services (business logic)
│   │   ├── booking_service.py      # Lógica de reservas
│   │   ├── calendar_service.py     # Sincronização
│   │   ├── document_service.py     # Geração de documentos
│   │   ├── email_service.py        # Email IMAP/SMTP
│   │   ├── notification_service.py # Notificações
│   │   └── sync_action_service.py  # Ações de sync
│   │
│   ├── telegram/                   # Bot Telegram
│   │   ├── __init__.py
│   │   └── bot.py                  # Implementação do bot
│   │
│   ├── templates/                  # Templates
│   │   └── email/
│   │       ├── booking_confirmation.html
│   │       └── checkin_reminder.html
│   │
│   └── utils/                      # Utilitários
│       ├── date_utils.py           # Manipulação de datas
│       └── logger.py               # Logger configurado
│
├── frontend/                       # Aplicação React
│   ├── src/
│   │   ├── components/             # Componentes React
│   │   ├── pages/                  # Páginas
│   │   ├── services/               # API clients
│   │   ├── utils/                  # Utilitários
│   │   ├── App.tsx                 # Componente raiz
│   │   └── main.tsx                # Entry point
│   ├── public/                     # Assets estáticos
│   ├── package.json
│   └── vite.config.ts
│
├── data/                           # Dados da aplicação
│   ├── sentinel.db                 # Banco SQLite
│   ├── generated_docs/             # Documentos gerados
│   ├── downloads/                  # Downloads temporários
│   └── logs/                       # Arquivos de log
│
├── deployment/                     # Configurações de deploy
│   ├── nginx/
│   │   └── nginx.conf              # Config Nginx
│   ├── systemd/
│   │   └── sentinel.service        # Service systemd
│   ├── fail2ban/
│   │   ├── sentinel.conf           # Filter fail2ban
│   │   └── jail.local              # Jail config
│   └── scripts/
│       ├── deploy_vps.sh           # Script de deploy
│       ├── setup_ssl.sh            # Configurar SSL
│       └── test_deployment.sh      # Testes
│
├── docs/                           # Documentação
│   ├── README.md                   # Índice principal
│   ├── PROJECT_STRUCTURE.md        # Estrutura do projeto
│   ├── status/                     # Status dos MVPs
│   ├── security/                   # Segurança
│   ├── guides/                     # Guias práticos
│   ├── architecture/               # Arquitetura técnica
│   ├── deployment/                 # Deploy
│   └── reports/                    # Relatórios
│
├── scripts/                        # Scripts utilitários
│   ├── create_users_table.py       # Criar tabela users
│   ├── create_default_admin.py     # Criar admin padrão
│   └── protect_routes.py           # Proteger rotas
│
├── .env.example                    # Template de configuração
├── .gitignore                      # Arquivos ignorados pelo Git
├── .dockerignore                   # Arquivos ignorados pelo Docker
├── Dockerfile                      # Imagem Docker
├── docker-compose.yml              # Orquestração Docker
├── requirements.txt                # Dependências Python
├── README.md                       # README principal
└── ORGANIZACAO_FINAL.md            # Resumo da organização
```

---

## 5. Banco de Dados

### Diagrama ER (Entity-Relationship)

```
┌────────────────┐
│    Property    │
│ ───────────── │
│ id (PK)        │
│ name           │
│ address        │
│ condo_name     │
└────────┬───────┘
         │ 1
         │
         │ N
┌────────┴────────────┐          ┌──────────────────┐
│  CalendarSource     │          │     Booking      │
│ ─────────────────── │          │ ──────────────── │
│ id (PK)             │          │ id (PK)          │
│ property_id (FK)    │          │ property_id (FK) │
│ platform            │ N     N  │ guest_id (FK)    │
│ ical_url            ├──────────┤ platform         │
│ is_active           │          │ check_in         │
└─────────────────────┘          │ check_out        │
                                 │ guest_name       │
                                 │ status           │
                                 └──────┬───────────┘
                                        │ 1
                                        │
                                        │ N
                             ┌──────────┴────────────┐
                             │  BookingConflict      │
                             │ ───────────────────── │
                             │ id (PK)               │
                             │ booking1_id (FK)      │
                             │ booking2_id (FK)      │
                             │ conflict_type         │
                             │ severity              │
                             │ is_resolved           │
                             └───────────────────────┘

┌─────────────┐          ┌─────────────┐
│    Guest    │          │    User     │
│ ─────────── │          │ ─────────── │
│ id (PK)     │          │ id (PK)     │
│ name        │          │ username    │
│ cpf         │          │ email       │
│ email       │          │ password    │
│ phone       │          │ is_active   │
└─────────────┘          │ role        │
                         └─────────────┘

┌─────────────────┐      ┌─────────────────┐
│    SyncLog      │      │   SyncAction    │
│ ─────────────── │      │ ─────────────── │
│ id (PK)         │      │ id (PK)         │
│ property_id(FK) │      │ booking_id (FK) │
│ started_at      │      │ action_type     │
│ completed_at    │      │ priority        │
│ success         │      │ status          │
│ duration_ms     │      │ due_date        │
└─────────────────┘      └─────────────────┘
```

### Models Detalhados

#### 1. Property (Imóvel)

```python
class Property(Base):
    __tablename__ = "properties"

    id: int (PK)
    name: str
    address: str
    condo_name: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Relacionamentos
    calendar_sources: List[CalendarSource]
    bookings: List[Booking]
    sync_logs: List[SyncLog]
```

#### 2. CalendarSource (Fonte de Calendário)

```python
class CalendarSource(Base):
    __tablename__ = "calendar_sources"

    id: int (PK)
    property_id: int (FK)
    platform: str  # "airbnb", "booking", "manual"
    ical_url: Optional[str]
    is_active: bool = True
    last_sync: Optional[datetime]
    created_at: datetime

    # Relacionamentos
    property: Property
```

#### 3. Booking (Reserva)

```python
class Booking(Base):
    __tablename__ = "bookings"

    id: int (PK)
    property_id: int (FK)
    guest_id: Optional[int] (FK)
    platform: str  # "airbnb", "booking", "manual"
    platform_booking_id: Optional[str]
    check_in: date
    check_out: date
    guest_name: str
    guest_email: Optional[str]
    guest_phone: Optional[str]
    num_guests: Optional[int]
    total_price: Optional[float]
    status: str  # "pending", "confirmed", "cancelled", "completed"
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Relacionamentos
    property: Property
    guest: Optional[Guest]
    conflicts_as_booking1: List[BookingConflict]
    conflicts_as_booking2: List[BookingConflict]
```

#### 4. BookingConflict (Conflito de Reserva)

```python
class BookingConflict(Base):
    __tablename__ = "booking_conflicts"

    id: int (PK)
    booking1_id: int (FK)
    booking2_id: int (FK)
    conflict_type: str  # "overlap", "duplicate"
    severity: str  # "critical", "high", "medium", "low"
    overlap_days: Optional[int]
    detected_at: datetime
    is_resolved: bool = False
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]

    # Relacionamentos
    booking1: Booking
    booking2: Booking
```

#### 5. Guest (Hóspede)

```python
class Guest(Base):
    __tablename__ = "guests"

    id: int (PK)
    name: str
    cpf: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    document_id: Optional[str]
    created_at: datetime

    # Relacionamentos
    bookings: List[Booking]
```

#### 6. User (Usuário do Sistema)

```python
class User(Base):
    __tablename__ = "users"

    id: int (PK)
    username: str (unique)
    email: str (unique)
    hashed_password: str
    is_active: bool = True
    role: str = "user"  # "admin", "user"
    created_at: datetime
    last_login: Optional[datetime]
```

#### 7. SyncLog (Log de Sincronização)

```python
class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: int (PK)
    property_id: int (FK)
    source_platform: str
    started_at: datetime
    completed_at: Optional[datetime]
    success: bool
    bookings_added: int = 0
    bookings_updated: int = 0
    bookings_cancelled: int = 0
    duration_ms: Optional[int]
    error_message: Optional[str]

    # Relacionamentos
    property: Property
```

#### 8. SyncAction (Ação de Sincronização)

```python
class SyncAction(Base):
    __tablename__ = "sync_actions"

    id: int (PK)
    booking_id: Optional[int] (FK)
    action_type: str  # "block_calendar", "send_notification", etc
    priority: str  # "critical", "high", "medium", "low"
    status: str  # "pending", "in_progress", "completed", "failed"
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime

    # Relacionamentos
    booking: Optional[Booking]
```

### Índices e Performance

```sql
-- Índices criados automaticamente
CREATE INDEX idx_bookings_dates ON bookings(check_in, check_out);
CREATE INDEX idx_bookings_property ON bookings(property_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_conflicts_booking1 ON booking_conflicts(booking1_id);
CREATE INDEX idx_conflicts_booking2 ON booking_conflicts(booking2_id);
CREATE INDEX idx_conflicts_resolved ON booking_conflicts(is_resolved);
CREATE INDEX idx_calendar_sources_property ON calendar_sources(property_id);
CREATE INDEX idx_calendar_sources_active ON calendar_sources(is_active);
```

---

## 6. API REST

### Estrutura de Endpoints

**Total:** 54 endpoints organizados em 8 routers

### Router: Auth (/api/v1/auth)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/auth/register` | Registrar novo usuário | ❌ |
| POST | `/api/v1/auth/login` | Login (retorna JWT) | ❌ |
| GET | `/api/v1/auth/me` | Dados do usuário atual | ✅ |
| POST | `/api/v1/auth/change-password` | Trocar senha | ✅ |
| POST | `/api/v1/auth/logout` | Logout | ✅ |
| DELETE | `/api/v1/auth/delete-account` | Deletar conta | ✅ |

### Router: Health (/api/v1/health)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/v1/health` | Health check básico | ❌ |
| GET | `/api/v1/health/detailed` | Health check detalhado | ✅ |

### Router: Bookings (/api/bookings)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/bookings/` | Listar reservas (paginado) | ✅ |
| GET | `/api/bookings/current` | Reserva atual | ✅ |
| GET | `/api/bookings/upcoming` | Próximas N reservas | ✅ |
| GET | `/api/bookings/{id}` | Detalhes de reserva | ✅ |
| POST | `/api/bookings/` | Criar reserva manual | ✅ |
| PUT | `/api/bookings/{id}` | Atualizar reserva | ✅ |
| DELETE | `/api/bookings/{id}` | Cancelar reserva | ✅ |
| GET | `/api/bookings/statistics/summary` | Estatísticas resumidas | ✅ |

### Router: Calendar (/api/calendar)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/calendar/events` | Eventos do calendário | ✅ |
| POST | `/api/calendar/sync` | Sincronizar agora | ✅ |
| GET | `/api/calendar/sync-status` | Status da sincronização | ✅ |

### Router: Conflicts (/api/conflicts)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/conflicts/` | Listar conflitos | ✅ |
| GET | `/api/conflicts/summary` | Resumo de conflitos | ✅ |
| POST | `/api/conflicts/{id}/resolve` | Resolver conflito | ✅ |
| POST | `/api/conflicts/detect` | Detectar conflitos manualmente | ✅ |

### Router: Documents (/api/v1/documents)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/documents/generate` | Gerar documento | ✅ |
| POST | `/api/v1/documents/generate-from-booking` | Gerar de reserva | ✅ |
| GET | `/api/v1/documents/list` | Listar documentos | ✅ |
| GET | `/api/v1/documents/download/{filename}` | Download | ✅ |
| DELETE | `/api/v1/documents/{filename}` | Deletar documento | ✅ |
| POST | `/api/v1/documents/generate-and-download` | Gerar e download | ✅ |

### Router: Emails (/api/v1/emails)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/emails/send` | Enviar email | ✅ |
| POST | `/api/v1/emails/send-template` | Enviar com template | ✅ |
| POST | `/api/v1/emails/send-booking-confirmation` | Confirmação reserva | ✅ |
| POST | `/api/v1/emails/send-checkin-reminder` | Lembrete check-in | ✅ |
| POST | `/api/v1/emails/send-bulk-reminders` | Lembretes em massa | ✅ |
| POST | `/api/v1/emails/fetch` | Buscar emails (IMAP) | ✅ |
| GET | `/api/v1/emails/test-connection` | Testar conexão | ✅ |

### Router: Statistics (/api/statistics)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/statistics/dashboard` | Dashboard completo | ✅ |
| GET | `/api/statistics/occupancy` | Taxa de ocupação | ✅ |
| GET | `/api/statistics/revenue` | Estatísticas de receita | ✅ |

### Router: Sync Actions (/api/sync-actions)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/sync-actions/` | Listar ações pendentes | ✅ |
| POST | `/api/sync-actions/{id}/complete` | Marcar como completa | ✅ |

---

## 7. Autenticação e Segurança

### Fluxo de Autenticação JWT

```
1. Login
   ┌─────────┐
   │ Client  │
   └────┬────┘
        │ POST /api/v1/auth/login
        │ { username, password }
        ↓
   ┌────┴──────────────┐
   │  Auth Endpoint    │
   │  ────────────     │
   │  1. Valida user   │
   │  2. Bcrypt verify │
   │  3. Gera JWT      │
   └────┬──────────────┘
        │ 200 OK
        │ { access_token, token_type, user }
        ↓
   ┌────┴────┐
   │ Client  │
   │ Stores  │
   │  Token  │
   └─────────┘

2. Request Autenticado
   ┌─────────┐
   │ Client  │
   └────┬────┘
        │ GET /api/bookings/
        │ Header: Authorization: Bearer <token>
        ↓
   ┌────┴──────────────────┐
   │  Auth Middleware      │
   │  ─────────────────    │
   │  1. Extract token     │
   │  2. Verify signature  │
   │  3. Decode payload    │
   │  4. Load user         │
   └────┬──────────────────┘
        │ User object
        ↓
   ┌────┴──────────────┐
   │  Router Handler   │
   │  Process request  │
   └────┬──────────────┘
        │ Response
        ↓
   ┌────┴────┐
   │ Client  │
   └─────────┘
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "username",
    "exp": 1709654400,
    "iat": 1709652600
  },
  "signature": "..."
}
```

### Security Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### Rate Limiting

```python
# Configuração atual
RATE_LIMIT_PER_MINUTE = 60  # requests por minuto

# Rotas com rate limiting específico
/api/v1/auth/register: 3/min
/api/v1/auth/login: 5/min
```

---

## 8. Sincronização de Calendários

### Fluxo de Sincronização

```
┌──────────────────────────────────────────────────────────┐
│                   SINCRONIZAÇÃO iCAL                     │
└──────────────────────────────────────────────────────────┘

1. TRIGGER (a cada 30min ou manual)
   │
   ↓
2. DOWNLOAD iCAL
   ├─→ Airbnb iCal URL
   └─→ Booking iCal URL
   │
   ↓
3. PARSE iCAL (icalendar lib)
   │ • Extrai eventos (VEVENT)
   │ • Parse datas (check-in/check-out)
   │ • Parse descrições
   │
   ↓
4. PROCESSAR EVENTOS
   │
   ├─→ NOVO?
   │   └─→ CREATE booking (status: confirmed)
   │
   ├─→ EXISTE?
   │   └─→ UPDATE booking (se mudanças)
   │
   └─→ CANCELADO?
       └─→ UPDATE status: cancelled
   │
   ↓
5. DETECTAR CONFLITOS
   │ • Compare todas as reservas
   │ • Identifica overlaps
   │ • Identifica duplicatas
   │
   ↓
6. CRIAR SYNC LOG
   │ • Duração
   │ • Bookings added/updated/cancelled
   │ • Success/Error
   │
   ↓
7. NOTIFICAR (se conflitos)
   ├─→ Telegram
   └─→ Email
```

### Algoritmo de Detecção de Conflitos

```python
def detect_conflicts(bookings: List[Booking]):
    """
    Detecta conflitos entre reservas

    Tipos de conflito:
    1. OVERLAP: Datas se sobrepõem
    2. DUPLICATE: Mesma reserva em 2 plataformas
    """

    conflicts = []

    # Comparar cada par de reservas
    for i, booking1 in enumerate(bookings):
        for booking2 in bookings[i+1:]:

            # Skip se mesma reserva ou já canceladas
            if booking1.id == booking2.id:
                continue
            if booking1.status == "cancelled" or booking2.status == "cancelled":
                continue

            # Verificar overlap de datas
            overlap = (
                booking1.check_in < booking2.check_out and
                booking2.check_in < booking1.check_out
            )

            if overlap:
                # Calcular dias de sobreposição
                overlap_start = max(booking1.check_in, booking2.check_in)
                overlap_end = min(booking1.check_out, booking2.check_out)
                overlap_days = (overlap_end - overlap_start).days

                # Verificar se é duplicata
                is_duplicate = (
                    abs((booking1.check_in - booking2.check_in).days) <= 1 and
                    abs((booking1.check_out - booking2.check_out).days) <= 1 and
                    similar_names(booking1.guest_name, booking2.guest_name)
                )

                conflict_type = "duplicate" if is_duplicate else "overlap"
                severity = calculate_severity(overlap_days, conflict_type)

                conflicts.append({
                    "booking1_id": booking1.id,
                    "booking2_id": booking2.id,
                    "conflict_type": conflict_type,
                    "severity": severity,
                    "overlap_days": overlap_days
                })

    return conflicts
```

---

## 9. Sistema de Documentos

### Fluxo de Geração

```
┌─────────────────────────────────────────────────────────┐
│              GERAÇÃO DE DOCUMENTOS                      │
└─────────────────────────────────────────────────────────┘

1. REQUEST
   │ POST /api/v1/documents/generate-from-booking
   │ { booking_id: 123, save_to_file: true }
   │
   ↓
2. BUSCAR DADOS
   │ • Booking data (datas, hóspede)
   │ • Property data (endereço, condomínio)
   │ • Guest data (CPF, documentos)
   │
   ↓
3. PREPARAR CONTEXTO
   │ {
   │   guest_name: "João Silva",
   │   guest_cpf: "123.456.789-00",
   │   check_in: "01/03/2026",
   │   check_out: "05/03/2026",
   │   property_name: "Apto 101",
   │   property_address: "Rua X, 123",
   │   condo_name: "Condomínio Y",
   │   date_today: "04/02/2026"
   │ }
   │
   ↓
4. CARREGAR TEMPLATE
   │ • templates/autorizacao_condominio.docx
   │ • DocxTemplate (docxtpl)
   │
   ↓
5. RENDERIZAR TEMPLATE
   │ • Substituir {{ variáveis }}
   │ • Aplicar formatação
   │
   ↓
6. SALVAR (opcional)
   │ • data/generated_docs/
   │ • autorizacao_123_20260204.docx
   │
   ↓
7. RETORNAR
   │ • Caminho do arquivo OU
   │ • Bytes para download direto
```

### Variáveis Disponíveis nos Templates

```python
{
    # Hóspede
    'guest_name': str,
    'guest_cpf': str,
    'guest_phone': str,
    'guest_email': str,

    # Reserva
    'check_in': str,  # DD/MM/YYYY
    'check_out': str,  # DD/MM/YYYY
    'booking_id': int,
    'total_nights': int,

    # Imóvel
    'property_name': str,
    'property_address': str,
    'condo_name': str,
    'owner_name': str,

    # Sistema
    'date_today': str,  # DD/MM/YYYY
    'condo_admin': str
}
```

---

## 10. Sistema de Email

### Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                  EMAIL SERVICE                           │
└──────────────────────────────────────────────────────────┘

┌────────────────┐         ┌────────────────┐
│  EmailService  │◄────────│   EmailConfig  │
└────────┬───────┘         └────────────────┘
         │
         ├─→ SMTP (aiosmtplib)
         │   • Envio assíncrono
         │   • TLS/SSL
         │   • Anexos
         │
         └─→ IMAP (aioimaplib)
             • Leitura assíncrona
             • Busca de emails
             • Folders (INBOX, SENT)
```

### Providers Pré-configurados

```python
PROVIDERS = {
    "gmail": {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "use_tls": True
    },
    "outlook": {
        "smtp_host": "smtp-mail.outlook.com",
        "smtp_port": 587,
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "use_tls": True
    },
    "yahoo": {
        "smtp_host": "smtp.mail.yahoo.com",
        "smtp_port": 587,
        "imap_host": "imap.mail.yahoo.com",
        "imap_port": 993,
        "use_tls": True
    }
}
```

### Fluxo de Envio

```
1. Criar EmailService
   ├─→ from_provider("gmail", username, password)
   └─→ Ou custom config
   │
   ↓
2. Renderizar Template (Jinja2)
   │ • booking_confirmation.html
   │ • Substituir variáveis
   │
   ↓
3. Construir MIMEMultipart
   │ • Subject
   │ • From/To/CC/BCC
   │ • HTML body
   │ • Attachments (opcional)
   │
   ↓
4. Conectar SMTP (async)
   │ • aiosmtplib.SMTP()
   │ • STARTTLS
   │ • Login
   │
   ↓
5. Enviar
   │ • send_message()
   │
   ↓
6. Retornar
   │ { success: true, message_id: "..." }
```

---

## 11. Bot do Telegram

### Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Iniciar bot | `/start` |
| `/help` | Lista de comandos | `/help` |
| `/menu` | Menu interativo | `/menu` |
| `/status` | Status do sistema | `/status` |
| `/reservas` | Lista reservas confirmadas | `/reservas` |
| `/hoje` | Check-ins e check-outs de hoje | `/hoje` |
| `/proximas` | Próximas 5 reservas | `/proximas` |
| `/conflitos` | Conflitos detectados | `/conflitos` |
| `/sync` | Sincronizar agora | `/sync` |

### Arquitetura do Bot

```
┌───────────────────────────────────────────────────────┐
│                  TELEGRAM BOT                         │
└───────────────────────────────────────────────────────┘

┌──────────────┐
│  TelegramBot │
└──────┬───────┘
       │
       ├─→ CommandHandler("/start")
       ├─→ CommandHandler("/status")
       ├─→ CommandHandler("/reservas")
       ├─→ CommandHandler("/sync")
       ├─→ CallbackQueryHandler (botões)
       │
       └─→ Database Context
           • get_db_context()
           • Read-only queries
```

### Notificações Push

```python
# Notificação de Conflito Crítico
async def notify_critical_conflict(conflict):
    message = f"""
    ⚠️ CONFLITO CRÍTICO DETECTADO!

    Reserva 1: {conflict.booking1.guest_name}
    • Check-in: {conflict.booking1.check_in}
    • Check-out: {conflict.booking1.check_out}
    • Plataforma: {conflict.booking1.platform}

    Reserva 2: {conflict.booking2.guest_name}
    • Check-in: {conflict.booking2.check_in}
    • Check-out: {conflict.booking2.check_out}
    • Plataforma: {conflict.booking2.platform}

    Sobreposição: {conflict.overlap_days} dias
    Tipo: {conflict.conflict_type}

    Resolva imediatamente em /conflitos
    """

    await bot.send_message(
        chat_id=admin_user_id,
        text=message,
        parse_mode="Markdown"
    )
```

---

## 12. Configurações

### Variáveis de Ambiente (.env)

```bash
# === APLICAÇÃO ===
APP_NAME=Sentinel
APP_ENV=production  # development, staging, production
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
TIMEZONE=America/Sao_Paulo

# === BANCO DE DADOS ===
DATABASE_URL=sqlite:///./data/sentinel.db

# === TELEGRAM BOT ===
TELEGRAM_BOT_TOKEN=123456:ABCdef...
TELEGRAM_ADMIN_USER_IDS=987654321,123456789

# === CALENDÁRIOS ===
AIRBNB_ICAL_URL=https://www.airbnb.com/calendar/ical/XXX.ics
BOOKING_ICAL_URL=https://admin.booking.com/.../XXX.ics
CALENDAR_SYNC_INTERVAL_MINUTES=30

# === EMAIL UNIVERSAL (MVP2) ===
EMAIL_PROVIDER=gmail  # gmail, outlook, yahoo, custom
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app-password
EMAIL_USE_TLS=true
CONTACT_PHONE=(62) 99999-9999
CONTACT_EMAIL=contato@sentinel.com

# === DOCUMENTOS (MVP2) ===
TEMPLATE_DIR=./templates
OUTPUT_DIR=./data/generated_docs
DEFAULT_TEMPLATE=autorizacao_condominio.docx

# === IMÓVEL ===
PROPERTY_NAME=Apartamento 2 Quartos - Goiânia
PROPERTY_ADDRESS=Rua Exemplo, 123, Setor Central
CONDO_NAME=Condomínio Exemplo
CONDO_ADMIN_NAME=Administração do Condomínio

# === SEGURANÇA ===
SECRET_KEY=CHANGE_THIS_TO_STRONG_KEY_32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === CORS ===
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# === RATE LIMITING ===
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# === FEATURES ===
ENABLE_AUTO_DOCUMENT_GENERATION=false
ENABLE_CONFLICT_NOTIFICATIONS=true
```

---

## 13. Deploy

### Opções de Deploy

1. **VPS Tradicional** (Ubuntu/Debian)
2. **Docker** (Containerizado)
3. **Docker Compose** (Multi-container)

### Deploy VPS (Resumido)

```bash
# 1. Clonar repositório
git clone https://github.com/Sitr3n01/AP_Controller.git
cd AP_Controller

# 2. Executar script de deploy
sudo ./deployment/scripts/deploy_vps.sh

# 3. Configurar SSL
sudo ./deployment/scripts/setup_ssl.sh seu-dominio.com

# 4. Testar
./deployment/scripts/test_deployment.sh
```

### Deploy Docker

```bash
# 1. Build
docker build -t sentinel:latest .

# 2. Run
docker run -d \
  --name sentinel \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.env:/app/.env \
  sentinel:latest
```

### Deploy Docker Compose

```bash
# 1. Configurar .env
cp .env.example .env
# Editar .env

# 2. Up
docker-compose up -d

# 3. Logs
docker-compose logs -f

# 4. Down
docker-compose down
```

---

## 14. Monitoramento

### Health Checks

```bash
# Basic Health Check
curl http://localhost:8000/health

# Detailed Health Check (autenticado)
curl -H "Authorization: Bearer TOKEN" \
     http://localhost:8000/api/v1/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1709654321,
  "version": "1.0.0",
  "database": "ok",
  "disk_usage": {
    "total_gb": 100,
    "used_gb": 50,
    "free_gb": 50,
    "percent": 50
  },
  "memory": {
    "total_mb": 8192,
    "available_mb": 4096,
    "percent": 50
  }
}
```

### Logs

```bash
# Logs do Uvicorn
tail -f data/logs/sentinel.log

# Logs do Systemd
sudo journalctl -u sentinel -f

# Logs do Docker
docker logs -f sentinel
```

### Métricas

- **Taxa de ocupação**: `/api/statistics/occupancy`
- **Reservas por mês**: `/api/statistics/revenue`
- **Conflitos ativos**: `/api/conflicts/summary`
- **Status de sincronização**: `/api/calendar/sync-status`

---

## 15. Troubleshooting

### Problemas Comuns

#### 1. Erro ao iniciar: "Port 8000 already in use"

```bash
# Encontrar processo
lsof -i :8000

# Matar processo
kill -9 <PID>
```

#### 2. Banco de dados corrompido

```bash
# Backup do banco
cp data/sentinel.db data/sentinel.db.backup

# Recriar tabelas
python -c "from app.database.session import create_all_tables; create_all_tables()"
```

#### 3. Token JWT inválido

```bash
# Gerar nova SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Atualizar .env
SECRET_KEY=nova-chave-gerada
```

#### 4. Email não enviando (Gmail)

```bash
# Verificar App Password
# 1. Vá em: https://myaccount.google.com/apppasswords
# 2. Gere nova senha de app
# 3. Use no .env (não a senha normal!)

EMAIL_PASSWORD=app-password-gerada
```

#### 5. Sincronização falhando

```bash
# Testar URL iCal
curl -I https://www.airbnb.com/calendar/ical/XXX.ics

# Verificar logs
grep "sync" data/logs/sentinel.log
```

---

## 📚 Referências

### Documentação Externa

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **python-telegram-bot**: https://python-telegram-bot.readthedocs.io/
- **icalendar**: https://icalendar.readthedocs.io/
- **docxtpl**: https://docxtpl.readthedocs.io/

### Documentação Interna

- **[Índice Geral](../README.md)**
- **[Guia de Instalação](../guides/GUIA_INSTALACAO.md)**
- **[Guia da API](../guides/GUIA_API.md)**
- **[Vulnerabilidades Críticas](../reports/VULNERABILIDADES_CRITICAS.md)**
- **[Bugs Encontrados](../reports/BUGS_ENCONTRADOS.md)**

---

**Última Atualização:** 04/02/2026
**Versão do Documento:** 1.0.0
**Mantenedor:** Equipe SENTINEL
