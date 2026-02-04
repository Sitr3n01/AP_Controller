# 🏠 SENTINEL - Sistema de Gestão Automatizada de Apartamento

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

Sistema completo de automação para gerenciar apartamento em Goiânia-GO listado no **Airbnb** e **Booking.com**, prevenindo overbooking, detectando conflitos automaticamente e fornecendo dashboard com estatísticas detalhadas.

## ✨ Funcionalidades

### MVP 1 - Backend REST API ✅ (Completo)
- ✅ Sincronização automática de calendários iCal (Airbnb + Booking)
- ✅ Detecção de conflitos e double bookings
- ✅ REST API completa para gestão de reservas
- ✅ Dashboard com estatísticas e analytics
- ✅ Sistema de ações pendentes (sync actions)
- ✅ Paginação eficiente e otimização de queries
- ✅ Índices compostos para alta performance
- ✅ Interface Web completa com React + Vite
- ✅ Calendário visual com eventos coloridos
- ✅ Sistema de resolução de conflitos
- ✅ Página de estatísticas com gráficos interativos
- ✅ Bot Telegram para notificações e gerenciamento remoto

### MVP 2 - Gestão de Hóspedes (Em breve)
- 📋 Banco de dados de hóspedes e histórico
- 📄 Geração automática de documentos do condomínio
- 🚗 Registro de veículos
- 📱 Envio de PDFs via Telegram

### MVP 3 - Integração com IA (Futuro)
- 🤖 Processamento de emails com Gemma 3 local
- 💬 Interface de linguagem natural no Telegram
- 📧 Monitoramento em tempo real via Gmail API

## 🚀 Quick Start

### 1. Requisitos
- Python 3.10 ou superior
- Windows 10/11
- Conta Telegram
- URLs dos calendários iCal do Airbnb e Booking

### 2. Instalação

```batch
# Clone ou baixe o projeto
cd AP_Controller

# Execute o script de setup automatizado
scripts\setup_windows.bat

# Configure o arquivo .env com seus tokens e URLs
notepad .env

# Inicialize o banco de dados
python scripts\init_db.py

# Inicie o servidor
scripts\start_server.bat
```

### 3. Configuração do Telegram

1. Crie um bot no Telegram:
   - Abra [@BotFather](https://t.me/BotFather)
   - Envie `/newbot` e siga as instruções
   - Copie o token gerado

2. Obtenha seu User ID:
   - Abra [@userinfobot](https://t.me/userinfobot)
   - Envie `/start`
   - Copie o número do seu ID

3. Cole o token e ID no arquivo `.env`

### 4. Obter URLs dos Calendários

**Airbnb:**
1. Acesse [Airbnb Host](https://www.airbnb.com/hosting)
2. Vá em Calendário → Disponibilidade
3. Clique em "Exportar calendário"
4. Copie o link do calendário

**Booking.com:**
1. Acesse [Booking Extranet](https://admin.booking.com/)
2. Vá em Calendário → Sincronização
3. Copie o link de exportação iCal

## 🌐 API Endpoints

A API REST está disponível em `http://127.0.0.1:8000`

**Principais endpoints:**
- `GET /api/bookings` - Listar reservas (com paginação)
- `GET /api/calendar/events` - Eventos do calendário
- `POST /api/calendar/sync` - Forçar sincronização
- `GET /api/conflicts` - Listar conflitos
- `GET /api/statistics/dashboard` - Dashboard com métricas
- `GET /api/sync-actions` - Ações pendentes

**Documentação interativa:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 📱 Comandos do Telegram (Em breve)

```
/start      - Iniciar o bot
/status     - Ver resumo do sistema
/hoje       - Quem está no apartamento hoje
/proximas   - Próximas reservas
/sync       - Forçar sincronização manual
```

## 📁 Estrutura do Projeto

```
AP_Controller/
├── app/                    # Código da aplicação
│   ├── core/              # Lógica central
│   ├── models/            # Modelos do banco de dados
│   ├── services/          # Camada de negócio
│   └── interfaces/        # Telegram, Gmail, Ollama
├── data/                  # Dados e banco (gitignored)
├── scripts/               # Scripts utilitários
├── templates/             # Templates de documentos
└── docs/                  # Documentação
```

## 🔧 Solução de Problemas

**Bot não responde:**
- Verifique se o token está correto no `.env`
- Confirme que o servidor está rodando
- Teste a conexão: envie `/start` para o bot

**Calendários não sincronizam:**
- Verifique se as URLs estão corretas no `.env`
- Execute sync manual: `python scripts\manual_sync.py`
- Verifique os logs em `data/logs/`

**Erro ao iniciar:**
- Certifique-se de que o ambiente virtual está ativado
- Reinstale dependências: `pip install -r requirements.txt`
- Verifique se o Python 3.10+ está instalado

## 📚 Documentação Completa

- [SETUP.md](docs/SETUP.md) - Guia detalhado de instalação
- [COMANDOS_TELEGRAM.md](docs/COMANDOS_TELEGRAM.md) - Referência completa de comandos
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Solução de problemas comuns

## 🛠️ Stack Tecnológica

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local
- **python-telegram-bot** - Interface Telegram
- **Loguru** - Sistema de logging avançado

## 📝 Licença

Este é um projeto pessoal para uso privado.

## 🤝 Suporte

Para problemas ou dúvidas, consulte a [documentação](docs/) ou verifique os logs em `data/logs/`.

---

**Status:** ✅ MVP 1 Backend Completo | 🚧 Interface Web em desenvolvimento
