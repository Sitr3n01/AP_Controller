# 🏠 SENTINEL - Apartment Management System

**Sistema de Gestão Automatizada de Apartamento para Airbnb e Booking.com**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-54%2F100-red.svg)](docs/reports/VULNERABILIDADES_CRITICAS.md)

---

## 📋 Visão Geral

SENTINEL é uma API completa para gerenciamento automatizado de apartamentos alugados em plataformas como Airbnb e Booking.com. O sistema sincroniza calendários, detecta conflitos de reservas, gera documentos e oferece dashboards e notificações via Telegram.

### ✅ MVP1 Completo

- 🗓️ **Sincronização de Calendários**: Integração com iCal (Airbnb/Booking)
- ⚠️ **Detecção de Conflitos**: Identificação automática de sobreposição de reservas
- 📊 **Dashboard e Estatísticas**: Visualização de ocupação, receita e métricas
- 📱 **Bot Telegram**: 9 comandos funcionais, notificações automáticas
- 🔒 **Autenticação JWT**: Segurança com tokens e bcrypt
- 📈 **API REST Completa**: 54 endpoints documentados

### ✅ MVP2 Completo

- 📄 **Geração de Documentos**: Templates DOCX com Jinja2 (6 endpoints)
- 📧 **Sistema de Email Universal**: IMAP/SMTP para Gmail, Outlook, Yahoo (7 endpoints)
- 📨 **Templates de Email**: Confirmação de reserva e lembretes
- 🔗 **Integração Completa**: Notificações por email e Telegram

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
git clone https://github.com/SEU_USUARIO/AP_Controller.git
cd AP_Controller

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Inicializar banco de dados
python -c "from app.database.session import create_all_tables; create_all_tables()"
python scripts/create_default_admin.py

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

Acesse: **http://localhost:8000/docs**

Credenciais padrão: **admin** / **Admin123!** (mude imediatamente!)

---

## 📖 Documentação Completa

**📚 Índice Geral**: **[docs/README.md](docs/README.md)**

### 🚀 Para Iniciantes
1. **[Guia de Instalação](docs/guides/GUIA_INSTALACAO.md)** - 20+ páginas passo a passo
2. **[Guia de Uso Diário](docs/guides/GUIA_USO_DIARIO.md)** - Como usar todas as funcionalidades
3. **[Guia Telegram](docs/guides/GUIA_TELEGRAM.md)** - Configurar o bot do zero

### 👨‍💻 Para Desenvolvedores
1. **[Guia da API](docs/guides/GUIA_API.md)** - Documentação completa dos 54 endpoints
2. **[Arquitetura Geral](docs/architecture/ARQUITETURA_GERAL.md)** - Visão técnica do sistema
3. **[Estrutura do Projeto](docs/PROJECT_STRUCTURE.md)** - Organização do código

### 🔒 Segurança (URGENTE!)
1. **[Vulnerabilidades Críticas](docs/reports/VULNERABILIDADES_CRITICAS.md)** - ⚠️ **LEIA PRIMEIRO**
2. **[Auditoria Completa](docs/security/AUDITORIA_SEGURANCA_DETALHADA.md)** - Análise profunda
3. **[Bugs Encontrados](docs/reports/BUGS_ENCONTRADOS.md)** - Lista de bugs conhecidos

### 📊 Status do Projeto
1. **[MVP1 Status](docs/status/RESUMO_FINAL_MVP1.md)** - 100% completo
2. **[MVP2 Implementação](docs/status/MVP2_IMPLEMENTACAO.md)** - 100% completo
3. **[Organização Final](ORGANIZACAO_FINAL.md)** - Resumo completo

---

## ⚠️ Status de Segurança

**Score Atual**: **54/100** 🔴 **CRÍTICO**

- ✅ Autenticação JWT com tokens assinados
- ✅ Bcrypt para hashing de senhas
- ✅ Rate limiting parcial
- ✅ Security headers básicos
- 🔴 **3 vulnerabilidades CRÍTICAS** identificadas
- 🟡 **5 vulnerabilidades ALTAS** identificadas

**⚠️ IMPORTANTE**: **NÃO fazer deploy em produção** até corrigir as vulnerabilidades críticas!

Veja detalhes em: **[docs/reports/VULNERABILIDADES_CRITICAS.md](docs/reports/VULNERABILIDADES_CRITICAS.md)**

Ver: [Auditoria Completa](docs/security/AUDITORIA_SEGURANCA_DETALHADA.md)

---

## 🛠️ Stack Tecnológico

**Backend**: FastAPI, SQLAlchemy, Pydantic, JWT, Bcrypt  
**Database**: SQLite (dev) / PostgreSQL (prod)  
**Deployment**: Docker, Nginx, Let's Encrypt, Systemd  
**Monitoramento**: psutil, Loguru, Health checks  

---

## 📦 Deploy Rápido

### Docker (Recomendado)
```bash
docker compose up -d
```

### VPS Tradicional
```bash
sudo ./deployment/scripts/deploy_vps.sh
sudo ./deployment/scripts/setup_ssl.sh seu-dominio.com email@example.com
```

---

## 📞 Suporte

- **Documentação**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/AP_Controller/issues)

---

## ⚠️ Aviso Importante

Este sistema contém **vulnerabilidades de segurança conhecidas** que estão sendo corrigidas.

**NÃO USE EM PRODUÇÃO** até que as correções críticas sejam aplicadas.

---

<div align="center">

**Feito com ❤️ para facilitar a gestão de apartamentos**

[Documentação](docs/) • [Deployment](docs/deployment/) • [Segurança](docs/security/)

</div>
