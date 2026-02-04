# Arquitetura Geral - LUMINA

Visao geral da arquitetura do sistema LUMINA.

---

## Visao Geral

LUMINA e um sistema de gestao de imoveis para aluguel de curta temporada (Airbnb/Booking.com) construido com arquitetura moderna em camadas.

### Stack Tecnologico

**Backend**:
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- Pydantic para validacao
- JWT para autenticacao
- Bcrypt para senhas

**Database**:
- SQLite (desenvolvimento)
- PostgreSQL (producao recomendado)

**Frontend** (em desenvolvimento):
- React 18+
- Vite
- TailwindCSS
- Axios

**Integracoes**:
- Telegram Bot API
- iCal (Airbnb/Booking)
- IMAP/SMTP (email)
- python-docx (documentos)

---

## Arquitetura em Camadas

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (Frontend React + Telegram Bot)        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           API Layer                     │
│  (FastAPI Routers + Middleware)         │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Business Logic Layer            │
│  (Services + Core Logic)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Data Access Layer              │
│  (SQLAlchemy Models + Database)         │
└─────────────────────────────────────────┘
```

---

## Componentes Principais

### 1. API Layer (app/api/)

**Responsabilidades**:
- Autenticacao e autorizacao
- Validacao de requests
- Health checks
- Documentacao Swagger

**Endpoints**:
- `/health` - Health check
- `/api/v1/auth/*` - Autenticacao
- `/api/v1/bookings/*` - Reservas
- `/api/v1/properties/*` - Imoveis
- `/api/v1/calendar/*` - Sincronizacao
- `/api/v1/conflicts/*` - Conflitos
- `/api/v1/statistics/*` - Estatisticas
- `/api/v1/documents/*` - Documentos
- `/api/v1/emails/*` - Emails

---

### 2. Routers (app/routers/)

**Responsabilidades**:
- Definir endpoints REST
- Chamar services
- Retornar responses

**Arquivos**:
- `bookings.py` - CRUD de reservas
- `properties.py` - CRUD de imoveis
- `calendar.py` - Sincronizacao
- `conflicts.py` - Gestao de conflitos
- `statistics.py` - Metricas e stats
- `sync_actions.py` - Historico de sync
- `documents.py` - Geracao de docs
- `emails.py` - Envio de emails

---

### 3. Services (app/services/)

**Responsabilidades**:
- Logica de negocio
- Integracao com APIs externas
- Processamento de dados
- Validacoes complexas

**Arquivos**:
- `calendar_service.py` - Sincronizacao iCal
- `booking_service.py` - Logica de reservas
- `notification_service.py` - Notificacoes
- `sync_action_service.py` - Logs de sync
- `document_service.py` - Geracao de documentos
- `email_service.py` - Envio de emails

---

### 4. Models (app/models/)

**Responsabilidades**:
- Definir estrutura do banco
- Relacionamentos entre tabelas
- Constraints e validacoes

**Entidades**:
- `User` - Usuarios do sistema
- `Property` - Imoveis
- `Booking` - Reservas
- `Guest` - Hospedes
- `BookingConflict` - Conflitos
- `CalendarSource` - Fontes de calendario
- `SyncLog` - Logs de sincronizacao
- `SyncAction` - Acoes de sync

**Relacionamentos**:
```
Property ──< Booking >── Guest
    │
    └──< BookingConflict
    │
    └──< CalendarSource
    │
    └──< SyncLog
```

---

### 5. Core (app/core/)

**Responsabilidades**:
- Funcionalidades criticas
- Seguranca
- Configuracoes
- Utilitarios

**Arquivos**:
- `security.py` - JWT, hashing, auth
- `backup.py` - Backup automatico
- `environments.py` - Gestao de ambientes
- `conflict_detector.py` - Deteccao de conflitos
- `calendar_sync.py` - Sync core logic

---

### 6. Middleware (app/middleware/)

**Responsabilidades**:
- Interceptar requests/responses
- Adicionar headers
- Rate limiting
- Logging

**Arquivos**:
- `auth.py` - Verificacao JWT
- `security_headers.py` - Headers de seguranca

---

### 7. Telegram Bot (app/telegram/)

**Responsabilidades**:
- Comandos interativos
- Notificacoes push
- Interface mobile

**Arquivos**:
- `bot.py` - Bot principal
- `notifications.py` - Sistema de notificacoes

---

## Fluxo de Dados

### 1. Criacao de Reserva Manual

```
Frontend/API Call
     ↓
Router (bookings.py)
     ↓
BookingService.create_booking()
     ↓
Validation (Pydantic)
     ↓
Database (SQLAlchemy)
     ↓
Check Conflicts
     ↓
Send Notification (Telegram/Email)
     ↓
Return Response
```

### 2. Sincronizacao de Calendario

```
Cron/Manual Trigger
     ↓
CalendarService.sync_all()
     ↓
For each Property:
  ├─ Fetch iCal URL
  ├─ Parse .ics file
  ├─ Extract bookings
  ├─ Save to database
  └─ Detect conflicts
     ↓
Send Notifications
     ↓
Log Sync Action
```

### 3. Deteccao de Conflitos

```
New Booking Created/Updated
     ↓
ConflictDetector.check_conflicts()
     ↓
Query overlapping bookings
     ↓
For each overlap:
  ├─ Calculate severity
  ├─ Create Conflict record
  └─ Send alert
     ↓
Return conflicts
```

### 4. Geracao de Documento

```
API Call (generate-from-booking)
     ↓
DocumentService.generate()
     ↓
Fetch Booking + Guest + Property
     ↓
Load Template (.docx)
     ↓
Fill template with data (Jinja2)
     ↓
Save document
     ↓
Return file path
```

---

## Seguranca

### Autenticacao
```
Login Request
     ↓
Validate credentials
     ↓
Generate JWT token
     ↓
Return token
     ↓
Client stores token
     ↓
Future requests include token in header:
Authorization: Bearer <token>
     ↓
Middleware validates token
     ↓
Extract user from token
     ↓
Allow request
```

### Rate Limiting
```
Request arrives
     ↓
Middleware checks IP + endpoint
     ↓
Query rate limit store (memory/Redis)
     ↓
If exceeded: return 429
If OK: continue
     ↓
Update counter
```

---

## Escalabilidade

### Horizontal Scaling

Para escalar horizontalmente:

1. **Database**: Migrar para PostgreSQL
2. **Cache**: Adicionar Redis para:
   - Token blacklist
   - Rate limiting
   - Session storage
3. **Load Balancer**: Nginx ou cloud LB
4. **Multiple Instances**: Docker Swarm ou Kubernetes

```
                    ┌─────────────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
      ┌────▼────┐     ┌────▼────┐    ┌────▼────┐
      │ API #1  │     │ API #2  │    │ API #3  │
      └────┬────┘     └────┬────┘    └────┬────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────▼───────┐
                    │  PostgreSQL  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    Redis     │
                    └──────────────┘
```

### Vertical Scaling

- Aumentar CPU/RAM do servidor
- Otimizar queries (indexes)
- Connection pooling

---

## Monitoramento

### Health Checks
- `/health` - Status da API
- Database connectivity
- External services status

### Logs
- Structured logging (Loguru)
- Levels: DEBUG, INFO, WARNING, ERROR
- Rotation por tamanho e tempo

### Metricas
- Request count
- Response time
- Error rate
- Active users
- Bookings per day

---

## Backup e Disaster Recovery

### Backup Automatico
- Cron diario
- Gzip compression
- Retencao de 30 dias
- Armazenamento local + cloud

### Disaster Recovery
- Backups regulares
- Procedures de restore
- Documentacao completa
- Testes periodicos

---

## Deploy

### Desenvolvimento
```bash
uvicorn app.main:app --reload
```

### Producao
```bash
# Docker
docker-compose up -d

# VPS
systemctl start lumina
nginx proxy
```

---

## Proximos Passos

### Curto Prazo
- Completar frontend React
- Corrigir vulnerabilidades de seguranca
- Testes automatizados

### Medio Prazo
- Multi-tenancy
- API de webhooks
- Mobile app

### Longo Prazo
- IA para precos dinamicos
- Analytics avancado
- Marketplace de servicos

---

**Veja tambem**:
- [Estrutura do Projeto](../PROJECT_STRUCTURE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Banco de Dados](BANCO_DE_DADOS.md)

**Atualizado**: 2026-02-04
