# 📁 SENTINEL - Estrutura do Projeto

## 🗂️ Organização de Diretórios

```
AP_Controller/
│
├── app/                                # 🎯 Aplicação Principal
│   ├── api/                           # Endpoints da API
│   │   └── v1/                        # API versão 1
│   │       ├── auth.py                # Autenticação (login, register, logout)
│   │       └── health.py              # Health checks e métricas
│   │
│   ├── core/                          # Núcleo da aplicação
│   │   ├── security.py                # JWT, bcrypt, tokens
│   │   ├── backup.py                  # Sistema de backup automático
│   │   └── environments.py            # Configurações por ambiente
│   │
│   ├── database/                      # Camada de dados
│   │   ├── connection.py              # Engine SQLAlchemy
│   │   └── session.py                 # Sessões e context managers
│   │
│   ├── middleware/                    # Middlewares HTTP
│   │   ├── auth.py                    # Middleware de autenticação
│   │   └── security_headers.py        # Security headers (HSTS, CSP, etc)
│   │
│   ├── models/                        # Modelos ORM (SQLAlchemy)
│   │   ├── base.py                    # Base declarativa
│   │   ├── user.py                    # Modelo de usuário
│   │   ├── property.py                # Modelo de imóvel
│   │   ├── booking.py                 # Modelo de reserva
│   │   └── conflict.py                # Modelo de conflito
│   │
│   ├── routers/                       # Routers de negócio
│   │   ├── bookings.py                # CRUD de reservas
│   │   ├── conflicts.py               # Gestão de conflitos
│   │   ├── statistics.py              # Estatísticas e dashboards
│   │   ├── calendar.py                # Calendário visual
│   │   └── sync_actions.py            # Ações de sincronização
│   │
│   ├── schemas/                       # Schemas Pydantic
│   │   ├── auth.py                    # Schemas de autenticação
│   │   ├── booking.py                 # Schemas de reserva
│   │   ├── conflict.py                # Schemas de conflito
│   │   └── ...
│   │
│   ├── services/                      # Lógica de negócio
│   │   ├── calendar_service.py        # Sincronização de calendários
│   │   ├── conflict_detector.py       # Detecção de conflitos
│   │   ├── stats_service.py           # Cálculo de estatísticas
│   │   └── ...
│   │
│   ├── utils/                         # Utilitários
│   │   └── logger.py                  # Sistema de logs (Loguru)
│   │
│   ├── config.py                      # Configurações centralizadas
│   └── main.py                        # 🚀 Ponto de entrada FastAPI
│
├── data/                              # 💾 Dados Persistentes (gitignored)
│   ├── sentinel.db                    # Banco de dados SQLite
│   ├── sentinel.db-shm                # Shared memory (temp)
│   ├── sentinel.db-wal                # Write-ahead log (temp)
│   ├── backups/                       # Backups automáticos
│   │   ├── daily/                     # Backups diários (7 dias)
│   │   ├── weekly/                    # Backups semanais (4 semanas)
│   │   └── monthly/                   # Backups mensais (6 meses)
│   ├── logs/                          # Logs da aplicação
│   │   └── sentinel_YYYYMMDD.log      # Logs rotativos
│   ├── downloads/                     # Downloads temporários
│   └── generated_docs/                # Documentos gerados
│
├── deployment/                        # ⚙️ Configurações de Deployment
│   ├── nginx/                         # Nginx reverse proxy
│   │   ├── nginx.conf                 # Configuração principal
│   │   └── ssl/                       # Certificados SSL (gitignored)
│   │
│   ├── systemd/                       # Systemd service
│   │   └── sentinel.service           # Service file Linux
│   │
│   ├── fail2ban/                      # Proteção brute-force
│   │   ├── sentinel.conf              # Filtro de logs
│   │   └── jail.local                 # Configuração de jail
│   │
│   └── scripts/                       # Scripts de deployment
│       ├── deploy_vps.sh              # Deployment automático VPS
│       ├── setup_ssl.sh               # Setup SSL/HTTPS
│       └── test_deployment.sh         # Testes end-to-end
│
├── docs/                              # 📚 Documentação
│   ├── deployment/                    # Guias de deployment
│   │   ├── DEPLOYMENT_VPS.md          # Guia completo VPS
│   │   ├── DOCKER_DEPLOYMENT.md       # Guia Docker
│   │   └── README_VPS_DEPLOYMENT.md   # Quick start
│   │
│   ├── security/                      # Documentação de segurança
│   │   ├── AUDITORIA_SEGURANCA_DETALHADA.md  # Auditoria profunda
│   │   ├── SEGURANCA_IMPLEMENTADA.md         # Fase 1
│   │   ├── SEGURANCA_FASE2_VPS.md            # Fase 2
│   │   └── SEGURANCA_FASE1_URGENTE.md        # Plano inicial
│   │
│   ├── guides/                        # Guias de uso
│   │   ├── COMO_INICIAR.md            # Primeiros passos
│   │   ├── CHECKLIST_PRODUCAO.md      # Checklist
│   │   ├── IMPLEMENTAR_SEGURANCA_AGORA.md
│   │   ├── PRIMEIRO_UPLOAD_GITHUB.md
│   │   ├── PROXIMOS_PASSOS.md
│   │   └── TORNAR_UTILIZAVEL.md
│   │
│   └── PROJECT_STRUCTURE.md           # Este arquivo
│
├── scripts/                           # 🔧 Scripts Utilitários
│   ├── create_users_table.py         # Criar tabela de usuários
│   ├── create_default_admin.py       # Criar usuário admin padrão
│   ├── protect_routes.py             # Proteger rotas (deprecated)
│   └── ...
│
├── templates/                         # 📄 Templates de Documentos
│   └── autorizacao_condominio.docx    # Template de autorização
│
├── venv/                              # 🐍 Ambiente Virtual Python (gitignored)
│
├── .dockerignore                      # Exclusões do Docker build
├── .env                               # Variáveis de ambiente (gitignored)
├── .env.example                       # Template de .env
├── .gitignore                         # Arquivos ignorados pelo Git
├── check_vps_ready.py                 # ✅ Verificação de deployment
├── docker-compose.yml                 # Orquestração Docker
├── Dockerfile                         # Imagem Docker
├── LICENSE                            # Licença MIT
├── README.md                          # Documentação principal
├── README.old.md                      # README anterior (backup)
└── requirements.txt                   # Dependências Python
```

---

## 📦 Módulos Principais

### `app/main.py`
Ponto de entrada da aplicação FastAPI.

**Responsabilidades**:
- Criação da instância FastAPI
- Configuração de middlewares (CORS, rate limiting, security headers)
- Registro de routers
- Lifecycle management (startup/shutdown)
- Exception handlers globais

### `app/config.py`
Configurações centralizadas usando Pydantic Settings.

**Responsabilidades**:
- Carregar variáveis do .env
- Validar tipos e formatos
- Fornecer defaults seguros
- Expor settings globalmente

### `app/core/security.py`
Núcleo de segurança da aplicação.

**Funções principais**:
- `get_password_hash()` - Hash bcrypt de senhas
- `verify_password()` - Verificação de senha
- `create_access_token()` - Criação de JWT
- `decode_access_token()` - Validação de JWT

### `app/core/backup.py`
Sistema de backup automático.

**Features**:
- Backup comprimido (gzip)
- Rotação automática (diário/semanal/mensal)
- Agendamento automático
- Restore seguro

### `app/middleware/auth.py`
Middleware de autenticação.

**Funções**:
- `get_current_user()` - Extrair usuário do token
- `get_current_active_user()` - Verificar se usuário está ativo
- `get_current_admin_user()` - Verificar se usuário é admin

### `app/middleware/security_headers.py`
Middleware de security headers.

**Headers**:
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

---

## 🔄 Fluxo de Dados

### 1. Requisição HTTP
```
Cliente → Nginx → FastAPI → Middleware → Router → Service → Model → Database
```

### 2. Autenticação
```
Cliente envia JWT → Middleware extrai token → Valida assinatura →
Busca usuário no DB → Injeta current_user → Router processa request
```

### 3. Sincronização de Calendários
```
Cron/Manual trigger → CalendarService.sync_all_sources() →
Fetch iCal URLs → Parse eventos → Salvar bookings →
ConflictDetector.detect() → Notificar se houver conflitos
```

### 4. Backup Automático
```
Task agendada (3h AM) → BackupManager.create_backup() →
Comprimir DB → Salvar em data/backups/{type}/ →
Rotacionar backups antigos → Log resultado
```

---

## 📊 Camadas da Aplicação

### Camada 1: Presentation (API)
- **Responsável**: Receber requisições HTTP, validar input, retornar JSON
- **Arquivos**: `app/api/v1/*.py`, `app/routers/*.py`
- **Tecnologia**: FastAPI, Pydantic

### Camada 2: Business Logic (Services)
- **Responsável**: Lógica de negócio, regras, cálculos
- **Arquivos**: `app/services/*.py`
- **Exemplos**: CalendarService, ConflictDetector, StatsService

### Camada 3: Data Access (Models)
- **Responsável**: Interação com banco de dados
- **Arquivos**: `app/models/*.py`, `app/database/*.py`
- **Tecnologia**: SQLAlchemy ORM

### Camada 4: Infrastructure
- **Responsável**: Segurança, logging, backup, monitoring
- **Arquivos**: `app/core/*.py`, `app/middleware/*.py`, `app/utils/*.py`

---

## 🗄️ Modelos do Banco de Dados

### `User`
Usuários do sistema.

**Campos principais**:
- `id` (PK)
- `email` (unique)
- `username` (unique)
- `hashed_password`
- `is_active`
- `is_admin`
- `created_at`
- `last_login_at`

### `Property`
Imóveis gerenciados.

**Campos principais**:
- `id` (PK)
- `name`
- `address`
- `airbnb_ical_url`
- `booking_ical_url`
- `owner_id` (FK → User)

### `Booking`
Reservas sincronizadas.

**Campos principais**:
- `id` (PK)
- `property_id` (FK)
- `source` (airbnb, booking, manual)
- `guest_name`
- `check_in`
- `check_out`
- `status`
- `external_id`

### `Conflict`
Conflitos detectados.

**Campos principais**:
- `id` (PK)
- `property_id` (FK)
- `booking1_id` (FK)
- `booking2_id` (FK)
- `conflict_type`
- `severity`
- `resolved`
- `resolution_notes`

---

## 🔐 Arquivos Sensíveis (Gitignored)

### `.env`
Variáveis de ambiente sensíveis.

**Nunca commitar!** Contém:
- `SECRET_KEY`
- `DATABASE_URL`
- Tokens de API
- Credenciais

### `data/sentinel.db`
Banco de dados com dados de produção.

**Conteúdo sensível**:
- Passwords hashados
- Emails de usuários
- Dados de reservas
- PII (Personally Identifiable Information)

### `data/backups/`
Backups do banco de dados.

**Mesma sensibilidade** do banco principal.

### `deployment/nginx/ssl/`
Certificados SSL/TLS.

**Privacidade crítica**:
- Private keys (.key)
- Certificates (.pem, .crt)

---

## 📝 Convenções de Código

### Nomes de Arquivos
- **Módulos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções**: `snake_case()`
- **Constantes**: `UPPER_SNAKE_CASE`

### Estrutura de Arquivos
```python
# 1. Imports padrão
import os
from datetime import datetime

# 2. Imports third-party
from fastapi import APIRouter
from sqlalchemy import Column

# 3. Imports locais
from app.config import settings
from app.models.user import User

# 4. Constantes
DEFAULT_LIMIT = 100

# 5. Classes/Funções
class MyService:
    pass

def my_function():
    pass
```

### Docstrings
```python
def create_user(email: str, password: str) -> User:
    """
    Cria um novo usuário no sistema.

    Args:
        email: Email do usuário
        password: Senha em texto plano

    Returns:
        User: Objeto do usuário criado

    Raises:
        HTTPException: Se email já existe
    """
    pass
```

---

## 🧪 Testes (Futuro)

Estrutura planejada:
```
tests/
├── unit/                    # Testes unitários
│   ├── test_security.py
│   ├── test_calendar_service.py
│   └── ...
├── integration/             # Testes de integração
│   ├── test_auth_flow.py
│   └── ...
├── e2e/                     # Testes end-to-end
│   └── test_booking_lifecycle.py
└── conftest.py              # Fixtures pytest
```

---

## 🔧 Scripts Úteis

### Desenvolvimento
```bash
# Iniciar servidor dev
uvicorn app.main:app --reload

# Criar migrações (Alembic - futuro)
alembic revision --autogenerate -m "Add column"
alembic upgrade head

# Linter/Formatter
black app/
flake8 app/
mypy app/
```

### Deployment
```bash
# Build Docker
docker compose build

# Deploy VPS
sudo ./deployment/scripts/deploy_vps.sh

# Backup manual
python -c "from app.core.backup import create_manual_backup; create_manual_backup()"
```

### Verificação
```bash
# Readiness check
python check_vps_ready.py

# Test deployment
./deployment/scripts/test_deployment.sh https://seu-dominio.com

# Verificar imports
python -c "from app.main import app; print('OK')"
```

---

## 📦 Dependências Principais

Ver `requirements.txt` para lista completa.

**Core**:
- `fastapi` - Framework web
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Validação de dados

**Segurança**:
- `python-jose` - JWT
- `bcrypt` - Password hashing
- `slowapi` - Rate limiting

**Utilitários**:
- `loguru` - Logging
- `python-dotenv` - .env loading
- `icalendar` - iCal parsing
- `psutil` - System metrics

---

## 🚀 Próximos Passos

1. **Correção de Vulnerabilidades** (prioridade máxima)
2. **Testes Automatizados** (pytest)
3. **CI/CD** (GitHub Actions)
4. **Migrations** (Alembic)
5. **Frontend** (React/Vue)
6. **Observability** (Grafana, Prometheus)
7. **Multi-tenancy** (Múltiplos imóveis)

---

## 📞 Referências

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

**Atualizado**: 2026-02-04
**Versão**: 1.0.0
