# 🏠 SENTINEL - Apartment Management System

**Sistema de Gestão Automatizada de Apartamento para Airbnb e Booking.com**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-92%2F100-brightgreen.svg)](docs/security-audits/SECURITY_REPORT.md)
[![Production](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)](docs/security-audits/SECURITY_REPORT.md)
[![Bugs Fixed](https://img.shields.io/badge/Critical_Bugs-12%2F12_Fixed-brightgreen.svg)](docs/security-audits/SECURITY_REPORT.md)
[![Vulnerabilities](https://img.shields.io/badge/Critical_Vulns-8%2F8_Fixed-brightgreen.svg)](docs/security-audits/SECURITY_REPORT.md)

---

## 📋 Visão Geral

SENTINEL v2.2.0 é uma API **production-ready** para gerenciamento automatizado de apartamentos alugados em plataformas como Airbnb e Booking.com. O sistema sincroniza calendários, detecta conflitos de reservas, gera documentos e oferece dashboards e notificações via Telegram.

### 🎉 **Status: Production Ready** (v2.2.0)

**✅ 25 Problemas Corrigidos**: 12 bugs críticos + 8 vulnerabilidades críticas + 5 problemas de alta prioridade

**🔒 Score de Segurança: 92/100** - Sistema pronto para deploy em produção

### ✅ MVP1 Completo

- 🗓️ **Sincronização de Calendários**: Integração com iCal (Airbnb/Booking)
- ⚠️ **Detecção de Conflitos**: Identificação automática de sobreposição de reservas com race condition protection
- 📊 **Dashboard e Estatísticas**: Visualização de ocupação, receita e métricas (com cálculos corrigidos)
- 📱 **Bot Telegram**: 9 comandos funcionais, notificações automáticas
- 🔒 **Autenticação JWT**: Token blacklist, rate limiting, proteção CSRF
- 📈 **API REST Completa**: 54 endpoints documentados e testados

### ✅ MVP2 Completo

- 📄 **Geração de Documentos**: Templates DOCX com Jinja2 (6 endpoints) + proteção IDOR
- 📧 **Sistema de Email Universal**: IMAP/SMTP para Gmail, Outlook, Yahoo (7 endpoints)
- 📨 **Templates de Email**: Confirmação de reserva e lembretes (com sanitização)
- 🔗 **Integração Completa**: Notificações por email e Telegram
- 🛡️ **Segurança Avançada**: SSTI prevention, header injection protection, path traversal protection

### 🚧 MVP3 Em Planejamento

- 🤖 **IA com Ollama/Gemma**: Respostas automatizadas inteligentes
- 📨 **Gmail API**: Monitoramento avançado de emails
- 🎯 **Automação Completa**: Fluxos de trabalho end-to-end

---

## 🚀 Quick Start

### Pré-requisitos

- **Python 3.11+**
- **pip** ou **poetry**
- **Git**

### Instalação Local

```bash
# 1. Clonar repositório
git clone https://github.com/Sitr3n01/AP_Controller.git
cd AP_Controller

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente (IMPORTANTE!)
cp .env.example .env
# Editar .env com suas configurações:
#   - SECRET_KEY: Mínimo 32 caracteres (obrigatório em produção)
#   - TELEGRAM_BOT_TOKEN: Token do @BotFather
#   - EMAIL_*: Configurações IMAP/SMTP

# 5. Inicializar banco de dados
python -c "from app.database.session import create_all_tables; create_all_tables()"
python scripts/create_default_admin.py

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

Acesse: **http://localhost:8000/docs**

Credenciais padrão: **admin** / **Admin123!** (⚠️ **MUDE IMEDIATAMENTE EM PRODUÇÃO!**)

📖 **Guia Completo**: [docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)

---

## 📖 Documentação Completa

**📚 Documentação Organizada**: Todos os documentos foram organizados em categorias

### 🚀 Para Iniciantes
1. **[Quick Start](docs/guides/QUICK_START.md)** - ⭐ **Comece aqui!** Guia rápido de 5 minutos
2. **[Guia de Instalação](docs/guides/GUIA_INSTALACAO.md)** - 20+ páginas passo a passo
3. **[Guia de Uso Diário](docs/guides/GUIA_USO_DIARIO.md)** - Como usar todas as funcionalidades
4. **[Guia Telegram](docs/guides/GUIA_TELEGRAM.md)** - Configurar o bot do zero

### 👨‍💻 Para Desenvolvedores
1. **[Guia da API](docs/guides/GUIA_API.md)** - Documentação completa dos 54 endpoints
2. **[Arquitetura Geral](docs/technical/ARQUITETURA_GERAL.md)** - Visão técnica do sistema
3. **[Estrutura do Projeto](docs/technical/PROJECT_STRUCTURE.md)** - Organização do código

### 🔒 Segurança e Auditorias
1. **[Security Report](docs/security-audits/SECURITY_REPORT.md)** - ⭐ **Relatório consolidado** de todas as auditorias
2. **[Bugs Corrigidos](docs/security-audits/CORRECOES_BUGS_CRITICOS.md)** - 12 bugs críticos corrigidos
3. **[Vulnerabilidades Corrigidas](docs/security-audits/CORRECOES_VULNERABILIDADES_CRITICAS.md)** - 8 vulnerabilidades críticas corrigidas
4. **[Auditoria Fase 3](docs/security-audits/CORRECOES_SEGURANCA_FASE3_FINAL.md)** - Token blacklist e melhorias MEDIUM
5. **[Auditoria Detalhada](docs/security-audits/AUDITORIA_SEGURANCA_DETALHADA.md)** - Análise profunda completa

### 📊 Status do Projeto
1. **[MVP1 Status](docs/status/RESUMO_FINAL_MVP1.md)** - 100% completo
2. **[MVP2 Implementação](docs/status/MVP2_IMPLEMENTACAO.md)** - 100% completo
3. **[Organização Final](ORGANIZACAO_FINAL.md)** - Resumo completo

---

## ✅ Status de Segurança

**Score Atual**: **92/100** 🟢 **PRODUCTION READY**

### Correções Implementadas (v2.2.0)

**✅ 8 Vulnerabilidades Críticas Corrigidas:**
- ✅ Path Traversal (CVSS 9.1) - Múltiplas camadas de proteção
- ✅ SSTI - Server-Side Template Injection (CVSS 9.8) - Templates inline desabilitados
- ✅ Mass Assignment (CVSS 8.8) - Pydantic `extra="forbid"`
- ✅ IDOR - Insecure Direct Object Reference (CVSS 8.1) - Validação de permissões
- ✅ Header Injection - Content-Disposition (CVSS 7.5) - RFC 5987 encoding
- ✅ SMTP Header Injection - Validação de newlines
- ✅ Attachment Filename Injection - Sanitização robusta
- ✅ IMAP NULL Pointer - Validação de dados

**✅ 12 Bugs Críticos Corrigidos:**
- ✅ AttributeError em check_in_date/check_out_date
- ✅ Comparação incorreta de enum (BookingStatus)
- ✅ Cálculo de ocupação (usando calendar.monthrange)
- ✅ N+1 queries (SQLAlchemy joinedload) - 200x melhoria
- ✅ Race condition em conflitos (UNIQUE constraint)
- ✅ Memory leak em token blacklist (cleanup periódico)
- ✅ IMAP resource leak (finally blocks)
- ✅ NoneType validation
- ✅ Message-ID tracking
- ✅ access_instructions null handling
- ✅ send_in_background parameter confusion
- ✅ Bulk email DoS (paginação)

**🔒 Segurança Implementada:**
- ✅ Autenticação JWT com token blacklist (Redis/in-memory)
- ✅ Bcrypt para hashing de senhas + account lockout
- ✅ Rate limiting global e por endpoint (slowapi)
- ✅ Security headers (CSP, HSTS, X-Frame-Options)
- ✅ CSRF protection middleware
- ✅ Input validation e sanitização (XSS, path traversal)
- ✅ SECRET_KEY validation (mínimo 32 caracteres)
- ✅ Security linters: Bandit + Safety

**📊 Relatório Detalhado**: [docs/security-audits/SECURITY_REPORT.md](docs/security-audits/SECURITY_REPORT.md)

---

## 🛠️ Stack Tecnológico

**Backend**: FastAPI 0.115+, SQLAlchemy 2.0, Pydantic v2, JWT, Bcrypt
**Database**: SQLite (dev) / PostgreSQL (prod)
**Security**: slowapi (rate limiting), CSRF middleware, security headers
**Email**: IMAP/SMTP (Gmail, Outlook, Yahoo), Jinja2 templates
**Documents**: python-docx, Jinja2 templating
**Telegram**: python-telegram-bot 20.0+
**Deployment**: Docker, Nginx, Let's Encrypt, Systemd
**Monitoramento**: psutil, Loguru, Health checks
**Linting**: Bandit (security), Safety (dependencies), Black, Flake8  

---

## 📦 Deploy em Produção

### Pré-requisitos de Segurança

**⚠️ ANTES DE FAZER DEPLOY:**

1. **Configurar SECRET_KEY forte** (mínimo 32 caracteres):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Configurar variáveis de ambiente**:
   - `APP_ENV=production`
   - `SECRET_KEY=<sua-chave-de-32-chars>`
   - `ALLOWED_HOSTS=seu-dominio.com`
   - `TELEGRAM_BOT_TOKEN=<seu-token>`
   - `EMAIL_USERNAME=<seu-email>`
   - `EMAIL_PASSWORD=<sua-senha-app>`

3. **Mudar senha do admin padrão**

### Docker (Recomendado)
```bash
# 1. Configurar .env de produção
cp .env.example .env.production
# Editar .env.production com valores reais

# 2. Build e deploy
docker compose up -d

# 3. Verificar logs
docker compose logs -f
```

### VPS Tradicional
```bash
# 1. Deploy com scripts automatizados
sudo ./deployment/scripts/deploy_vps.sh

# 2. Configurar SSL (Let's Encrypt)
sudo ./deployment/scripts/setup_ssl.sh seu-dominio.com email@example.com

# 3. Verificar status
sudo systemctl status sentinel
```

**📖 Guia Completo de Deploy**: [docs/guides/GUIA_INSTALACAO.md](docs/guides/GUIA_INSTALACAO.md)

---

## 📊 Funcionalidades Principais

### 🗓️ Gestão de Reservas
- Sincronização automática com Airbnb e Booking.com (iCal)
- Detecção de conflitos de reservas com proteção contra race conditions
- Dashboard de ocupação e estatísticas em tempo real
- Cálculo preciso de ocupação por mês

### 📄 Documentação Automatizada
- Geração de autorizações de condomínio em DOCX
- Templates personalizáveis com Jinja2
- Download seguro com proteção IDOR e path traversal

### 📧 Sistema de Email
- IMAP/SMTP para Gmail, Outlook, Yahoo
- Templates de confirmação de reserva e lembretes
- Envio em massa com paginação (proteção DoS)
- Sanitização de headers (proteção header injection)

### 📱 Bot Telegram
- 9 comandos funcionais (/start, /reservas, /conflitos, etc.)
- Notificações automáticas de novas reservas
- Dashboard interativo via mensagens

### 🔒 Segurança Enterprise
- Score 92/100 - Production Ready
- 25 problemas críticos corrigidos
- Rate limiting e CSRF protection
- Token blacklist com cleanup automático

---

## 📞 Suporte

- **Documentação**: [docs/](docs/)
- **Quick Start**: [docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)
- **Security Report**: [docs/security-audits/SECURITY_REPORT.md](docs/security-audits/SECURITY_REPORT.md)
- **Issues**: [GitHub Issues](https://github.com/Sitr3n01/AP_Controller/issues)

---

## 🎉 Changelog v2.2.0 (Production Ready)

**🔒 Segurança**:
- Corrigidas 8 vulnerabilidades críticas (Path Traversal, SSTI, Mass Assignment, IDOR, etc.)
- Score aumentado de 54/100 para 92/100
- Implementado token blacklist com cleanup automático
- Adicionada validação de SECRET_KEY em produção

**🐛 Bugs**:
- Corrigidos 12 bugs críticos (AttributeError, enum comparison, N+1 queries, race conditions, etc.)
- Melhorada performance em 200x (joinedload)
- Corrigido cálculo de ocupação (calendar.monthrange)
- Adicionada proteção contra memory leaks

**📚 Documentação**:
- Reorganizada em docs/guides/, docs/security-audits/, docs/technical/
- Criado QUICK_START.md para iniciantes
- Criado SECURITY_REPORT.md consolidado
- Atualizado README com status production-ready

---

<div align="center">

**Feito com ❤️ para facilitar a gestão de apartamentos**

[Documentação](docs/) • [Deployment](docs/deployment/) • [Segurança](docs/security/)

</div>
