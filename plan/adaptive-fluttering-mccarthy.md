# PLANO DE IMPLEMENTAÇÃO: SENTINEL - Sistema de Gestão Automatizada de Apartamento

## 📋 Contexto do Projeto

**Objetivo:** Criar sistema local de automação para gerenciar apartamento listado no Airbnb e Booking.com, prevenindo overbooking, automatizando documentação de condomínio, e mantendo histórico de hóspedes.

**Situação Atual:**
- Apartamento já está operando com reservas ativas
- Usuário tem nível técnico intermediário
- Sistema rodará 24/7 em PC Windows local
- Template de autorização do condomínio já existe (.docx)

**Abordagem:** Implementação incremental em 3 MVPs progressivos, priorizando funcionalidades críticas primeiro.

---

## 🎯 MVP 1: PREVENÇÃO DE OVERBOOKING (Crítico - Semanas 1-2)

### Objetivo
Implementar sincronização de calendários e detecção de conflitos para prevenir double bookings imediatamente.

### Funcionalidades
1. **Sincronização de Calendários iCal**
   - Download automático de feeds do Airbnb e Booking
   - Parsing de eventos (datas, hóspedes, status)
   - Normalização de formatos diferentes das plataformas
   - Atualização a cada 30 minutos

2. **Banco de Dados Local (SQLite)**
   - Tabela `properties`: dados do apartamento
   - Tabela `calendar_sources`: URLs dos iCal feeds
   - Tabela `bookings`: todas as reservas consolidadas
   - Tabela `booking_conflicts`: detecção de sobreposições
   - Tabela `sync_logs`: histórico de sincronizações

3. **Detecção de Conflitos**
   - Algoritmo de verificação de overlap de datas
   - Identificação de reservas duplicadas
   - Classificação de severidade (crítico, aviso)

4. **Interface Telegram - Comandos Básicos**
   - `/start` - Iniciar bot
   - `/status` - Resumo do sistema (próximas 5 reservas, conflitos ativos)
   - `/hoje` - Quem está no apartamento hoje
   - `/proximas` - Próximas reservas
   - `/sync` - Forçar sincronização manual
   - **Alertas automáticos** quando conflitos são detectados

### Arquivos Críticos do MVP1
```
AP_Controller/
├── .env.template                    # Template de configuração
├── requirements.txt                 # Dependências Python
├── app/
│   ├── config.py                    # Gerenciamento de configurações
│   ├── main.py                      # Aplicação FastAPI
│   ├── models/
│   │   ├── property.py              # Modelo SQLAlchemy: Property
│   │   ├── booking.py               # Modelo SQLAlchemy: Booking
│   │   ├── calendar_source.py      # Modelo SQLAlchemy: CalendarSource
│   │   └── sync_log.py              # Modelo SQLAlchemy: SyncLog
│   ├── core/
│   │   ├── calendar_sync.py         # Engine de sincronização iCal
│   │   └── conflict_detector.py     # Detector de conflitos
│   ├── services/
│   │   ├── booking_service.py       # Lógica de negócio: bookings
│   │   └── calendar_service.py      # Lógica de negócio: calendários
│   ├── interfaces/telegram/
│   │   ├── bot.py                   # Inicialização do bot
│   │   ├── handlers.py              # Handlers de comandos
│   │   └── messages.py              # Templates de mensagens PT-BR
│   └── database/
│       ├── connection.py            # Conexão SQLite
│       └── session.py               # Session factory
├── scripts/
│   ├── setup_windows.bat            # Script de setup automatizado
│   ├── init_db.py                   # Inicialização do banco
│   └── start_server.bat             # Iniciar servidor
└── data/
    └── sentinel.db                  # Banco de dados SQLite
```

### Verificação MVP1
- [ ] Calendários do Airbnb e Booking sincronizando corretamente
- [ ] Banco de dados populado com reservas reais
- [ ] Bot Telegram respondendo a comandos
- [ ] Alertas de conflito funcionando (testar criando bloqueio manual)
- [ ] Sistema roda continuamente sem erros por 24h

---

## 🎯 MVP 2: BANCO DE DADOS DE HÓSPEDES + DOCUMENTAÇÃO AUTOMÁTICA (Semanas 3-4)

### Objetivo
Automatizar geração de documentos do condomínio e criar histórico de hóspedes.

### Funcionalidades
1. **Gestão de Hóspedes**
   - Tabela `guests`: nome completo, email, telefone, documento, nacionalidade
   - Tabela `vehicles`: placa, modelo, cor (vinculada a hóspede)
   - Histórico de reservas por hóspede
   - Busca de hóspedes anteriores

2. **Geração Automática de Documentos**
   - Leitura do template `.docx` do condomínio
   - Preenchimento automático com dados da reserva
   - Campos: nome hóspede, CPF/documento, datas, veículo, etc.
   - Conversão DOCX → PDF
   - Armazenamento com metadata

3. **Comandos Telegram Expandidos**
   - `/hospedes` - Listar todos os hóspedes
   - `/hospede <nome>` - Buscar hóspede específico
   - `/reserva <id>` - Detalhes completos da reserva
   - `/gerar_doc <reserva_id>` - Gerar autorização do condomínio
   - `/veiculo <reserva_id> <placa> <modelo>` - Adicionar veículo
   - **Bot envia PDF automaticamente no Telegram**

### Novos Arquivos MVP2
```
AP_Controller/
├── templates/
│   └── autorizacao_condominio.docx  # Template Word do condomínio
├── app/
│   ├── models/
│   │   ├── guest.py                 # Modelo: Guest
│   │   ├── vehicle.py               # Modelo: Vehicle
│   │   └── document.py              # Modelo: Document
│   ├── core/
│   │   ├── document_generator.py    # Gerador de documentos
│   │   └── pdf_converter.py         # Conversor DOCX→PDF
│   ├── services/
│   │   ├── guest_service.py         # Lógica: hóspedes
│   │   └── document_service.py      # Lógica: documentos
└── data/
    └── generated_docs/              # PDFs gerados
```

### Verificação MVP2
- [ ] Template `.docx` preenchido corretamente com dados de teste
- [ ] PDF gerado com formatação correta (caracteres PT-BR)
- [ ] Bot envia PDF via Telegram
- [ ] Histórico de hóspedes consultável
- [ ] Informações de veículo sendo salvas

---

## 🎯 MVP 3: INTEGRAÇÃO INTELIGENTE COM IA (Semanas 5-6)

### Objetivo
Adicionar monitoramento de email e extração inteligente de dados com Gemma 3 local.

### Funcionalidades
1. **Monitoramento de Email (Gmail API)**
   - Conexão via OAuth2 com Gmail
   - Monitoramento de emails do Airbnb/Booking
   - Detecção mais rápida que iCal (tempo real vs 30min-2h)
   - Fila de processamento de emails

2. **Processamento com IA Local (Ollama + Gemma 3)**
   - Extração de dados estruturados de emails em linguagem natural
   - Campos: nome hóspede, datas, booking ID, preço, número de pessoas
   - Extração de info de veículos (placa, modelo, cor)
   - Validação de dados extraídos
   - Fallback para entrada manual se extração falhar

3. **Fluxo Inteligente**
   ```
   Email recebido → Gmail API captura →
   Gemma 3 extrai JSON → Valida dados →
   Cria/atualiza booking → Notifica Telegram
   ```

4. **Comandos IA Telegram**
   - Enviar mensagem livre: "Chega o João dia 10 com esposa e Fiat Uno placa ABC-1234"
   - Bot extrai automaticamente: nome, data, acompanhantes, veículo
   - Confirmação antes de salvar

### Novos Arquivos MVP3
```
AP_Controller/
├── app/
│   ├── core/
│   │   ├── email_monitor.py         # Monitor Gmail API
│   │   └── llm_processor.py         # Processador Ollama/Gemma
│   ├── interfaces/
│   │   ├── gmail/
│   │   │   ├── client.py            # Cliente Gmail API
│   │   │   └── parser.py            # Parser de emails
│   │   └── ollama/
│   │       ├── client.py            # Cliente Ollama
│   │       └── prompts.py           # Prompts de extração
│   └── models/
│       └── email_queue.py           # Fila de emails processados
├── credentials.json                 # Credenciais Gmail API
└── token.json                       # Token OAuth2
```

### Verificação MVP3
- [ ] Ollama rodando localmente com Gemma 3 4B
- [ ] Email de teste processado com sucesso
- [ ] Dados extraídos corretamente (nome, datas, veículo)
- [ ] Mensagem livre no Telegram processada pela IA
- [ ] Notificações de novas reservas via email funcionando

---

## 🏗️ Estrutura de Diretórios Completa

```
AP_Controller/
├── .env                             # Configurações (gitignored)
├── .env.template                    # Template de configurações
├── .gitignore                       # Arquivos ignorados
├── requirements.txt                 # Dependências Python
├── README.md                        # Documentação em português
├── pyproject.toml                   # Config moderna Python
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # Entry point FastAPI
│   ├── config.py                    # Configuração Pydantic
│   ├── constants.py                 # Constantes do sistema
│   ├── exceptions.py                # Exceções customizadas
│   │
│   ├── core/                        # Lógica central
│   │   ├── calendar_sync.py         # Sincronização iCal
│   │   ├── conflict_detector.py     # Detecção de conflitos
│   │   ├── email_monitor.py         # Monitor de emails
│   │   ├── llm_processor.py         # Processador IA
│   │   ├── document_generator.py    # Gerador de docs
│   │   └── pdf_converter.py         # Conversor PDF
│   │
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── base.py                  # Base model
│   │   ├── property.py
│   │   ├── calendar_source.py
│   │   ├── booking.py
│   │   ├── guest.py
│   │   ├── vehicle.py
│   │   ├── document.py
│   │   ├── sync_log.py
│   │   └── email_queue.py
│   │
│   ├── schemas/                     # Schemas Pydantic (DTOs)
│   │   ├── booking.py
│   │   ├── guest.py
│   │   └── telegram.py
│   │
│   ├── services/                    # Camada de negócio
│   │   ├── booking_service.py
│   │   ├── calendar_service.py
│   │   ├── guest_service.py
│   │   ├── document_service.py
│   │   └── notification_service.py
│   │
│   ├── interfaces/                  # Interfaces externas
│   │   ├── telegram/
│   │   │   ├── bot.py
│   │   │   ├── handlers.py
│   │   │   ├── keyboards.py         # Teclados inline
│   │   │   └── messages.py          # Mensagens PT-BR
│   │   ├── gmail/
│   │   │   ├── client.py
│   │   │   └── parser.py
│   │   └── ollama/
│   │       ├── client.py
│   │       └── prompts.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── session.py
│   │
│   ├── routers/                     # Rotas FastAPI
│   │   ├── health.py                # Health check
│   │   └── webhooks.py              # Webhooks Telegram
│   │
│   └── utils/
│       ├── logger.py                # Logging configurado
│       ├── date_utils.py            # Manipulação de datas
│       └── validators.py            # Validadores
│
├── templates/                       # Templates de documentos
│   └── autorizacao_condominio.docx
│
├── data/                            # Dados runtime (gitignored)
│   ├── sentinel.db                  # Banco SQLite
│   ├── downloads/                   # iCal files baixados
│   ├── generated_docs/              # PDFs gerados
│   └── logs/                        # Logs da aplicação
│
├── scripts/                         # Scripts utilitários
│   ├── setup_windows.bat            # Setup completo Windows
│   ├── init_db.py                   # Inicializar banco
│   ├── start_server.bat             # Iniciar aplicação
│   ├── install_service.bat          # Instalar como serviço Windows
│   └── manual_sync.py               # Sync manual para testes
│
├── tests/                           # Testes automatizados
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_calendar_sync.py
│   │   ├── test_conflict_detector.py
│   │   └── test_llm_processor.py
│   └── fixtures/
│       ├── sample_icals/
│       └── sample_emails/
│
└── docs/
    ├── SETUP.md                     # Guia de instalação PT-BR
    ├── COMANDOS_TELEGRAM.md         # Referência de comandos
    └── TROUBLESHOOTING.md           # Solução de problemas
```

---

## 🔧 Stack Tecnológica

### Core
- **Python 3.10+**
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local

### Integrações
- **python-telegram-bot** - Interface Telegram
- **httpx** - Cliente HTTP assíncrono
- **icalendar** - Parser de calendários iCal
- **google-api-python-client** - Gmail API
- **ollama** - SDK Python para Ollama/Gemma

### Documentos
- **python-docx-template** - Preenchimento de templates Word
- **python-docx** - Manipulação DOCX
- **weasyprint** - Conversão HTML→PDF

### Utilidades
- **pydantic-settings** - Gerenciamento de configuração
- **loguru** - Logging avançado
- **python-dateutil** - Manipulação de datas
- **tenacity** - Retry logic

---

## ⚙️ Configuração (.env.template)

```env
# === APLICAÇÃO ===
APP_NAME=Sentinel
APP_ENV=production
LOG_LEVEL=INFO
TIMEZONE=Europe/Lisbon

# === BANCO DE DADOS ===
DATABASE_URL=sqlite:///./data/sentinel.db

# === TELEGRAM BOT ===
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_ADMIN_USER_IDS=123456789
# Obter token: https://t.me/BotFather
# Obter seu user ID: https://t.me/userinfobot

# === CALENDÁRIOS ===
AIRBNB_ICAL_URL=https://www.airbnb.com/calendar/ical/XXXXXXX.ics
BOOKING_ICAL_URL=https://admin.booking.com/hotel/hoteladmin/ical/XXXXXXX.ics
CALENDAR_SYNC_INTERVAL_MINUTES=30

# === GMAIL API (MVP3) ===
GMAIL_CREDENTIALS_FILE=./credentials.json
GMAIL_TOKEN_FILE=./token.json
GMAIL_CHECK_INTERVAL_MINUTES=5
ENABLE_EMAIL_MONITORING=false  # Ativar apenas no MVP3

# === OLLAMA/GEMMA 3 (MVP3) ===
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
OLLAMA_TIMEOUT_SECONDS=30
OLLAMA_TEMPERATURE=0.1

# === DOCUMENTOS ===
TEMPLATE_DIR=./templates
OUTPUT_DIR=./data/generated_docs
DEFAULT_TEMPLATE=autorizacao_condominio.docx

# === DADOS DO IMÓVEL ===
PROPERTY_NAME=Apartamento T2 - Centro
PROPERTY_ADDRESS=Rua Exemplo, 123, 4000-000 Porto
CONDO_NAME=Condomínio Exemplo
CONDO_ADMIN_NAME=Administração Lda

# === FEATURES ===
ENABLE_AUTO_DOCUMENT_GENERATION=false  # Requer aprovação manual inicialmente
ENABLE_CONFLICT_NOTIFICATIONS=true
```

---

## 📊 Schema do Banco de Dados

### Tabelas Principais

**properties**
- id (PK)
- name, address, max_guests
- created_at, updated_at

**calendar_sources**
- id (PK)
- property_id (FK)
- platform (airbnb/booking)
- ical_url
- sync_enabled, last_sync_at
- sync_frequency_minutes

**bookings**
- id (PK)
- property_id (FK)
- calendar_source_id (FK)
- guest_id (FK)
- external_id (ID da plataforma)
- platform (airbnb/booking/manual)
- status (confirmed/cancelled/completed/blocked)
- check_in_date, check_out_date
- nights_count, guest_count
- guest_name, guest_email (denormalized)
- total_price, currency
- raw_ical_data, raw_email_data
- created_at, updated_at

**guests**
- id (PK)
- full_name, email, phone
- document_number, nationality
- notes
- created_at, updated_at

**vehicles**
- id (PK)
- guest_id (FK)
- license_plate, model, color
- created_at

**booking_conflicts**
- id (PK)
- booking_id_1, booking_id_2 (FKs)
- conflict_type (overlap/duplicate)
- overlap_start, overlap_end
- resolved, resolution_notes
- detected_at, resolved_at

**documents**
- id (PK)
- booking_id (FK)
- document_type (condo_authorization/invoice)
- template_name, file_path, file_format
- generated_at

**sync_logs**
- id (PK)
- calendar_source_id (FK)
- sync_type (ical/email/manual)
- status (success/error/partial)
- bookings_added, bookings_updated, bookings_cancelled
- conflicts_detected
- error_message, sync_duration_ms
- started_at, completed_at

**email_queue** (MVP3)
- id (PK)
- gmail_message_id, subject, sender
- received_at, processed
- processing_status
- extracted_data (JSON)
- booking_id (FK)
- error_message

---

## 🚀 Ordem de Implementação

### FASE 1: Setup Inicial (Dia 1)
1. Criar estrutura de diretórios
2. Configurar `requirements.txt`
3. Criar `.env.template`
4. Implementar `app/config.py` (Pydantic Settings)
5. Setup básico de logging (`app/utils/logger.py`)
6. Script `scripts/setup_windows.bat`

**Arquivos:**
- `requirements.txt`
- `.env.template`
- `app/config.py`
- `app/utils/logger.py`
- `scripts/setup_windows.bat`

---

### FASE 2: Database Foundation (Dia 2-3)
1. Criar modelos SQLAlchemy base:
   - `app/models/base.py`
   - `app/models/property.py`
   - `app/models/calendar_source.py`
   - `app/models/booking.py`
   - `app/models/sync_log.py`
2. Configurar conexão SQLite (`app/database/connection.py`)
3. Script de inicialização (`scripts/init_db.py`)
4. Inserir dados iniciais (1 property, 2 calendar sources)

**Arquivos:**
- `app/models/*.py` (5 arquivos)
- `app/database/connection.py`
- `app/database/session.py`
- `scripts/init_db.py`

---

### FASE 3: Calendar Sync Engine (Dia 4-5)
1. Implementar `app/core/calendar_sync.py`:
   - Método `download_ical(url)` com retry
   - Método `parse_ical(content, platform)`
   - Normalização Airbnb vs Booking
   - Método `merge_booking()` (create/update/cancel logic)
2. Implementar `app/services/booking_service.py`
3. Implementar `app/services/calendar_service.py`
4. Script manual de sync para testes (`scripts/manual_sync.py`)

**Arquivos:**
- `app/core/calendar_sync.py` ⭐
- `app/services/booking_service.py`
- `app/services/calendar_service.py`
- `scripts/manual_sync.py`

**Teste:** Executar `manual_sync.py` e verificar bookings no banco

---

### FASE 4: Conflict Detection (Dia 6)
1. Implementar `app/core/conflict_detector.py`:
   - Método `detect_conflicts(property_id)`
   - Algoritmo de overlap detection
   - Método `check_booking_conflict(booking)`
   - Gravação de conflitos na tabela
2. Adicionar modelo `app/models/booking_conflict.py`
3. Integrar com calendar sync (detectar após cada sync)

**Arquivos:**
- `app/core/conflict_detector.py` ⭐
- `app/models/booking_conflict.py`

**Teste:** Criar booking manual sobreposto e verificar detecção

---

### FASE 5: Telegram Bot Básico (Dia 7-8)
1. Criar estrutura Telegram:
   - `app/interfaces/telegram/bot.py` (inicialização)
   - `app/interfaces/telegram/handlers.py` (comandos)
   - `app/interfaces/telegram/messages.py` (templates PT-BR)
2. Implementar comandos MVP1:
   - `/start`, `/help`
   - `/status`, `/hoje`, `/proximas`
   - `/sync`
3. Implementar `app/services/notification_service.py`
4. Adicionar alertas de conflito automáticos
5. Integrar com FastAPI (`app/main.py`)

**Arquivos:**
- `app/interfaces/telegram/bot.py` ⭐
- `app/interfaces/telegram/handlers.py` ⭐
- `app/interfaces/telegram/messages.py`
- `app/services/notification_service.py`
- `app/main.py` (entry point)

**Teste:** Enviar comandos no Telegram e verificar respostas

---

### FASE 6: Automação e Persistência (Dia 9)
1. Adicionar sync automático periódico (cada 30 min)
2. Implementar scheduler (asyncio tasks no FastAPI lifespan)
3. Script de inicialização (`scripts/start_server.bat`)
4. Criar documentação básica (`docs/SETUP.md`)

**Arquivos:**
- `app/main.py` (adicionar lifespan events)
- `scripts/start_server.bat`
- `docs/SETUP.md`
- `README.md`

**Teste:** Sistema rodando por 24h sem erros, sync automático funcionando

---

### ✅ CHECKPOINT MVP1 (Dia 10)
- Sistema rodando 24/7
- Sincronizando Airbnb e Booking automaticamente
- Bot Telegram respondendo
- Alertas de conflito funcionando
- **DEPLOY EM PRODUÇÃO**

---

### FASE 7: Modelos de Guests (Dia 11)
1. Criar modelos:
   - `app/models/guest.py`
   - `app/models/vehicle.py`
   - `app/models/document.py`
2. Migração do banco (adicionar tabelas)
3. Implementar `app/services/guest_service.py`

**Arquivos:**
- `app/models/guest.py`
- `app/models/vehicle.py`
- `app/models/document.py`
- `app/services/guest_service.py`

---

### FASE 8: Document Generation (Dia 12-13)
1. Criar template Word com placeholders Jinja2
2. Implementar `app/core/document_generator.py`:
   - Método `fill_template(template_path, data)`
   - Método `convert_to_pdf(docx_path)`
3. Implementar `app/services/document_service.py`
4. Adicionar comandos Telegram:
   - `/reserva <id>` (detalhes completos)
   - `/gerar_doc <reserva_id>`
   - Bot envia PDF automaticamente

**Arquivos:**
- `templates/autorizacao_condominio.docx` ⭐
- `app/core/document_generator.py` ⭐
- `app/core/pdf_converter.py`
- `app/services/document_service.py`
- `app/interfaces/telegram/handlers.py` (atualizar)

**Teste:** Gerar documento de reserva real e verificar formatação

---

### FASE 9: Guest Management (Dia 14)
1. Adicionar comandos Telegram:
   - `/hospedes`
   - `/hospede <nome>`
   - `/veiculo <reserva_id> <placa> <modelo>`
2. Criar keyboards inline para navegação
3. Vincular guests a bookings existentes

**Arquivos:**
- `app/interfaces/telegram/handlers.py` (atualizar)
- `app/interfaces/telegram/keyboards.py` (novo)

**Teste:** Adicionar hóspede, vincular veículo, consultar histórico

---

### ✅ CHECKPOINT MVP2 (Dia 15)
- Banco de hóspedes funcional
- Documentos sendo gerados automaticamente
- PDFs enviados via Telegram
- **ATUALIZAÇÃO EM PRODUÇÃO**

---

### FASE 10: Ollama Setup (Dia 16)
1. Instalar Ollama no Windows
2. Download modelo Gemma 3 4B: `ollama pull gemma3:4b`
3. Criar `app/interfaces/ollama/client.py`
4. Criar `app/interfaces/ollama/prompts.py` com prompts de extração
5. Implementar `app/core/llm_processor.py`
6. Testes com emails de exemplo

**Arquivos:**
- `app/interfaces/ollama/client.py`
- `app/interfaces/ollama/prompts.py` ⭐
- `app/core/llm_processor.py` ⭐

**Teste:** Enviar texto livre, verificar JSON extraído

---

### FASE 11: Gmail Integration (Dia 17-18)
1. Configurar Gmail API no Google Cloud Console
2. Download de `credentials.json`
3. Implementar `app/interfaces/gmail/client.py` (OAuth2)
4. Implementar `app/core/email_monitor.py`
5. Adicionar modelo `app/models/email_queue.py`
6. Fluxo: Email → LLM → Booking → Notificação

**Arquivos:**
- `credentials.json` (baixar manualmente)
- `app/interfaces/gmail/client.py` ⭐
- `app/interfaces/gmail/parser.py`
- `app/core/email_monitor.py` ⭐
- `app/models/email_queue.py`

**Teste:** Encaminhar email de booking, verificar criação automática

---

### FASE 12: Natural Language Interface (Dia 19)
1. Adicionar handler de mensagens livres no Telegram
2. Processar com LLM: "Chega o João dia 10 com esposa e Fiat Uno ABC-1234"
3. Extrair: nome, data, acompanhantes, veículo
4. Mostrar preview com keyboard de confirmação
5. Salvar após confirmação

**Arquivos:**
- `app/interfaces/telegram/handlers.py` (atualizar)

**Teste:** Enviar diversas mensagens em linguagem natural

---

### ✅ CHECKPOINT MVP3 (Dia 20)
- IA processando emails automaticamente
- Mensagens livres no Telegram funcionando
- Sistema completo operacional
- **DEPLOY FINAL**

---

## 🧪 Estratégia de Testes

### Testes Unitários (pytest)
- `tests/unit/test_calendar_sync.py` - Parser iCal
- `tests/unit/test_conflict_detector.py` - Algoritmo de overlap
- `tests/unit/test_llm_processor.py` - Extração de dados
- `tests/unit/test_document_generator.py` - Template rendering

### Testes de Integração
- Sincronização completa: iCal → DB → Telegram
- Email flow: Gmail → LLM → DB → Notificação
- Document flow: Booking → Template → PDF → Telegram

### Fixtures de Teste
- `tests/fixtures/sample_icals/` - Arquivos iCal reais anonimizados
- `tests/fixtures/sample_emails/` - Emails de confirmação anonimizados

---

## 🔒 Segurança e Boas Práticas

### Gerenciamento de Credenciais
- **NUNCA** commitar `.env`, `credentials.json`, `token.json`
- Usar `.env.template` como referência
- Variáveis sensíveis carregadas via Pydantic Settings

### Error Handling
- Mensagens em português para usuário final
- Logs técnicos em inglês para debugging
- Retry logic com exponential backoff para APIs externas
- Graceful degradation: sistema funciona parcialmente se serviço falhar

### Resilência
- Offline-first: banco SQLite local
- Fila de retry para syncs falhados
- Backup automático diário do banco
- Health check endpoint para monitoramento

---

## 📱 Comandos Telegram - Referência Completa

### Visualização
- `/start` - Mensagem de boas-vindas
- `/help` - Lista todos os comandos
- `/status` - Dashboard: próximas 5 reservas, conflitos ativos, último sync
- `/hoje` - Quem está no apartamento hoje
- `/proximas` - Próximas 5 reservas
- `/calendar <mes> <ano>` - Calendário visual do mês

### Reservas
- `/reservas` - Listar todas reservas ativas
- `/reserva <id>` - Detalhes completos: datas, hóspede, preço, platform, veículo
- `/bloquear <data_inicio> <data_fim>` - Bloquear datas manualmente

### Hóspedes
- `/hospedes` - Listar todos os hóspedes no histórico
- `/hospede <nome>` - Buscar hóspede por nome (mostra histórico)
- `/veiculo <reserva_id> <placa> <modelo> <cor>` - Adicionar veículo

### Documentos
- `/gerar_doc <reserva_id>` - Gerar autorização do condomínio (envia PDF)
- `/documentos <reserva_id>` - Listar todos documentos da reserva

### Manutenção
- `/sync` - Forçar sincronização manual dos calendários
- `/sync_log` - Ver últimas 10 sincronizações
- `/test_ollama` - Testar conexão com Ollama (MVP3)
- `/config` - Ver configurações atuais (sem expor tokens)

### Mensagens Livres (MVP3)
- Escrever texto livre: "João Silva chega dia 15/03 com esposa"
- Bot extrai dados e pede confirmação

---

## 🔄 Fluxos de Dados Principais

### Fluxo 1: Sincronização de Calendários
```
Timer (30min) → CalendarSyncEngine
  ↓ download_ical(airbnb_url)
  ↓ download_ical(booking_url)
  ↓ parse_ical() → List[BookingData]
  ↓ BookingService.merge_booking()
  ↓ ConflictDetector.detect_conflicts()
  ↓ NotificationService.send_sync_report()
  → Telegram: "✅ Sync concluído: 5 reservas, 0 conflitos"
```

### Fluxo 2: Detecção de Conflito
```
ConflictDetector.detect_conflicts()
  ↓ get_active_bookings()
  ↓ for each pair: check_date_overlap()
  ↓ if overlap: create BookingConflict
  ↓ NotificationService.send_conflict_alert()
  → Telegram: "⚠️ CONFLITO: Airbnb e Booking sobrepostos em 10-12 Mar!"
```

### Fluxo 3: Geração de Documento
```
User: /gerar_doc 42
  ↓ BookingService.get_booking(42)
  ↓ GuestService.get_guest(booking.guest_id)
  ↓ DocumentGenerator.generate_from_booking()
    ↓ fill_template(autorizacao_condominio.docx, data)
    ↓ convert_to_pdf()
  ↓ DocumentService.save_document()
  ↓ TelegramBot.send_document()
  → Telegram: [PDF] "Autorizacao_Joao_Silva_10-12Mar.pdf"
```

### Fluxo 4: Processamento de Email (MVP3)
```
Gmail: Nova mensagem de reserva
  ↓ EmailMonitor detecta (push ou polling)
  ↓ EmailQueue.add(message_id, subject, body)
  ↓ LLMProcessor.extract_booking_from_email()
    ↓ Ollama API: prompt + email → JSON
    ↓ validate_extraction()
  ↓ BookingService.create_booking()
  ↓ NotificationService.send_new_booking_notification()
  → Telegram: "🆕 Nova reserva Airbnb: João Silva, 10-12 Mar"
```

---

## ⚠️ Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Delay do iCal** (30min-2h) | Overbooking não detectado a tempo | MVP3: Email monitoring tempo real |
| **Ollama crash** | Extração de dados falha | Graceful degradation: entrada manual via Telegram |
| **Gmail API rate limit** | Não consegue ler emails | Exponential backoff, fallback para iCal |
| **PC desliga** | Sistema para | Serviço Windows com auto-restart, sync ao reiniciar |
| **Banco corrompido** | Perda de dados | Backup diário automático em `data/backups/` |
| **Caracteres PT-BR em PDF** | Acentos bugados | WeasyPrint com UTF-8, testar em FASE 8 |
| **Template docx mudado** | Geração falha | Validar campos do template no setup |

---

## 📦 Dependências (requirements.txt)

```txt
# Core Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.0
pydantic-settings==2.6.0

# Database
sqlalchemy==2.0.36
aiosqlite==0.20.0

# Telegram
python-telegram-bot==22.0

# HTTP Client
httpx==0.28.1
tenacity==9.0.0  # Retry logic

# Calendar
icalendar==6.1.0
python-dateutil==2.9.0
pytz==2024.2

# Email (MVP3)
google-api-python-client==2.159.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.1

# Document Generation
python-docx-template==0.18.0
python-docx==1.1.2
weasyprint==63.1

# LLM (MVP3)
ollama==0.4.4

# Utilities
python-dotenv==1.0.1
loguru==0.7.2

# Testing
pytest==8.3.4
pytest-asyncio==0.24.0
faker==33.1.0
```

---

## 🚀 Comandos de Setup

### Setup Inicial (Executar uma vez)
```batch
# 1. Clonar/navegar para o projeto
cd C:\Users\zegil\Documents\GitHub\AP_Controller

# 2. Executar script de setup automatizado
scripts\setup_windows.bat

# 3. Editar configurações
notepad .env

# 4. Inicializar banco de dados
python scripts\init_db.py

# 5. (MVP3) Instalar Ollama
# Download: https://ollama.ai/download
ollama pull gemma3:4b
```

### Iniciar Sistema
```batch
# Modo desenvolvimento (com reload)
scripts\start_server.bat

# Modo produção (sem reload)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Testes
```batch
# Executar todos os testes
pytest

# Testes com cobertura
pytest --cov=app tests/

# Testar sync manual
python scripts\manual_sync.py
```

---

## 📝 Arquivos Mais Críticos para Implementação

1. **`app/config.py`** - Configuração centralizada (todas as funcionalidades dependem)
2. **`app/models/booking.py`** - Modelo central do sistema
3. **`app/core/calendar_sync.py`** - Engine de sincronização (MVP1 crítico)
4. **`app/core/conflict_detector.py`** - Prevenção de overbooking (objetivo principal)
5. **`app/interfaces/telegram/handlers.py`** - Interface do usuário (família não-técnica)
6. **`app/core/document_generator.py`** - Automação de documentos (economia de tempo)
7. **`app/core/llm_processor.py`** - Inteligência do sistema (diferencial)
8. **`templates/autorizacao_condominio.docx`** - Template do condomínio (caso de uso real)

---

## ✅ Critérios de Sucesso

### MVP1 (Semana 2)
- [ ] Calendários sincronizando a cada 30 minutos automaticamente
- [ ] Banco de dados com pelo menos 10 reservas reais
- [ ] Bot Telegram respondendo `/status`, `/hoje`, `/proximas`
- [ ] Alertas de conflito chegando no Telegram (testar com bloqueio manual)
- [ ] Sistema rodando 24h sem crashes
- [ ] Logs legíveis e sem erros críticos

### MVP2 (Semana 4)
- [ ] Template Word preenchido corretamente
- [ ] PDF gerado com acentuação correta
- [ ] PDF enviado automaticamente no Telegram via `/gerar_doc`
- [ ] Hóspedes sendo salvos no banco
- [ ] Veículos vinculados a reservas
- [ ] Histórico de hóspede consultável

### MVP3 (Semana 6)
- [ ] Ollama rodando com Gemma 3 4B
- [ ] Email de confirmação processado automaticamente
- [ ] Dados extraídos com >90% de acurácia
- [ ] Mensagem livre no Telegram: "João chega dia 10" → booking criado
- [ ] Notificação de nova reserva via email antes do iCal atualizar
- [ ] Sistema completo operacional 24/7

---

## 🎓 Documentação a Ser Criada

1. **`README.md`** - Visão geral do projeto, quick start
2. **`docs/SETUP.md`** - Guia passo-a-passo de instalação em português
3. **`docs/COMANDOS_TELEGRAM.md`** - Referência completa de comandos
4. **`docs/TROUBLESHOOTING.md`** - Problemas comuns e soluções
5. **`.env.template`** - Template de configuração com comentários

---

## 🔄 Melhorias Futuras (Pós-MVP3)

1. **Dashboard Web** - Interface visual do calendário (FastAPI + Jinja2)
2. **Multi-propriedades** - Gerenciar vários apartamentos
3. **Analytics** - Taxa de ocupação, receita mensal, hóspedes frequentes
4. **Limpeza** - Integração com agenda de limpeza
5. **Serviço Windows** - Auto-start ao ligar o PC
6. **Cloudflare Tunnel** - Webhook mode para Telegram (mais eficiente)
7. **Backup na nuvem** - Backup criptografado no Google Drive
8. **WhatsApp** - Interface alternativa ao Telegram
9. **App mobile** - React Native frontend
10. **Smart pricing** - Sugestões de preço usando IA

---

## 📞 Suporte e Troubleshooting

### Problemas Comuns

**Bot não responde:**
- Verificar token no `.env`
- Testar conexão: `curl https://api.telegram.org/bot<TOKEN>/getMe`
- Verificar se servidor FastAPI está rodando

**iCal não sincroniza:**
- Verificar URLs no `.env` (acessíveis no navegador?)
- Checar logs: `data/logs/sentinel_YYYY-MM-DD.log`
- Executar sync manual: `python scripts/manual_sync.py`

**Ollama não responde:**
- Verificar se Ollama está rodando: `ollama list`
- Testar modelo: `ollama run gemma3:4b "teste"`
- Verificar porta 11434 livre

**PDF com caracteres bugados:**
- Instalar fontes do sistema corretamente
- Verificar WeasyPrint dependencies: `pip install weasyprint[all]`
- Testar template manualmente

**Sistema parou de funcionar:**
- Verificar logs em `data/logs/`
- Reiniciar servidor: `scripts\start_server.bat`
- Verificar espaço em disco (banco de dados)

---

## 🎯 Próximos Passos Imediatos

1. **Confirmar este plano** ✅
2. **Executar FASE 1**: Setup inicial + estrutura de diretórios
3. **Executar FASE 2**: Database foundation
4. **Executar FASE 3**: Calendar sync engine
5. **Testar MVP1** com calendários reais do Airbnb/Booking

---

**Fim do Plano de Implementação - Pronto para Execução** 🚀
