# Documentacao SENTINEL - Indice Geral

Bem-vindo a documentacao completa do sistema SENTINEL!

---

## Visao Geral do Projeto

SENTINEL e um sistema de gestao automatizada de apartamentos para plataformas como Airbnb e Booking.com. O sistema sincroniza calendarios, detecta conflitos de reservas, gera documentos automaticamente e oferece notificacoes via Telegram e email.

**Status do MVP**: MVP1 completo (100%), MVP2 implementado (70%), MVP3 nao iniciado
**Score de Seguranca**: 85/100 (com vulnerabilidades criticas identificadas - **NAO usar em producao ainda**)

---

## Indice Rapido

### Para Iniciantes
- **[Guia de Instalacao Completo](guides/GUIA_INSTALACAO.md)** - Passo a passo detalhado para iniciantes
- **[Como Iniciar](guides/COMO_INICIAR.md)** - Quick start para desenvolvedores
- **[Guia de Uso Diario](guides/GUIA_USO_DIARIO.md)** - Como usar o sistema no dia a dia

### Para Desenvolvedores
- **[Estrutura do Projeto](PROJECT_STRUCTURE.md)** - Organizacao do codigo
- **[Documentacao da API](API_DOCUMENTATION.md)** - Endpoints e schemas
- **[Guia do Frontend](FRONTEND_GUIDE.md)** - Interface web
- **[Arquitetura da Interface Web](ARQUITETURA_INTERFACE_WEB.md)** - Design e componentes

### Para Deploy
- **[Deployment VPS](deployment/DEPLOYMENT_VPS.md)** - Deploy completo em VPS
- **[Deployment Docker](deployment/DOCKER_DEPLOYMENT.md)** - Deploy com Docker Compose
- **[Quick Start VPS](deployment/README_VPS_DEPLOYMENT.md)** - Deploy rapido
- **[Checklist de Producao](guides/CHECKLIST_PRODUCAO.md)** - Verificacoes pre-deploy

### Seguranca
- **[Auditoria Detalhada de Seguranca](security/AUDITORIA_SEGURANCA_DETALHADA.md)** - Analise profunda (LEIA PRIMEIRO!)
- **[Vulnerabilidades Criticas](reports/VULNERABILIDADES_CRITICAS.md)** - Resumo executivo
- **[Seguranca Fase 1 - Implementada](security/SEGURANCA_IMPLEMENTADA.md)** - JWT e autenticacao
- **[Seguranca Fase 2 - VPS](security/SEGURANCA_FASE2_VPS.md)** - HTTPS, Fail2ban, rate limiting

---

## Estrutura da Documentacao

```
docs/
├── README.md                           # Este arquivo - indice geral
├── status/                             # Status e relatorios do MVP
│   ├── MVP1_STATUS.md                  # Status completo do MVP1
│   ├── MVP2_IMPLEMENTACAO.md           # Status do MVP2
│   └── STATUS_MVP_ATUAL.md             # Status atual consolidado
├── security/                           # Documentacao de seguranca
│   ├── AUDITORIA_SEGURANCA_DETALHADA.md    # Auditoria completa (IMPORTANTE!)
│   ├── SEGURANCA_IMPLEMENTADA.md           # Fase 1 implementada
│   ├── SEGURANCA_FASE1_URGENTE.md          # Correcoes urgentes
│   └── SEGURANCA_FASE2_VPS.md              # Preparacao VPS
├── guides/                             # Guias praticos
│   ├── GUIA_INSTALACAO.md              # Instalacao passo a passo (INICIANTES)
│   ├── COMO_INICIAR.md                 # Quick start
│   ├── GUIA_USO_DIARIO.md              # Uso do sistema
│   ├── GUIA_API.md                     # Como usar a API
│   ├── GUIA_TELEGRAM.md                # Bot Telegram
│   ├── CHECKLIST_PRODUCAO.md           # Pre-deploy checklist
│   ├── TORNAR_UTILIZAVEL.md            # Melhorias de UX
│   ├── PROXIMOS_PASSOS.md              # Roadmap de features
│   └── PRIMEIRO_UPLOAD_GITHUB.md       # Git e GitHub
├── architecture/                       # Arquitetura do sistema
│   ├── ARQUITETURA_GERAL.md            # Visao geral
│   ├── BANCO_DE_DADOS.md               # Models e schemas
│   └── INTEGRACAO_CALENDARIOS.md       # Sincronizacao iCal
├── deployment/                         # Deploy e infraestrutura
│   ├── DEPLOYMENT_VPS.md               # Deploy VPS completo
│   ├── DOCKER_DEPLOYMENT.md            # Docker Compose
│   └── README_VPS_DEPLOYMENT.md        # Quick start VPS
├── reports/                            # Relatorios e analises
│   ├── BUGS_ENCONTRADOS.md             # Lista de bugs conhecidos
│   ├── VULNERABILIDADES_CRITICAS.md    # Resumo de seguranca
│   └── ANALISE_CODIGO.md               # Code review
└── archived/                           # Documentacao antiga (backup)
    └── (documentos obsoletos movidos para ca)
```

---

## Status do MVP

### MVP 1 - Sistema Basico (100% COMPLETO)
- API REST completa com FastAPI
- Autenticacao JWT
- CRUD de Reservas, Imoveis, Hospedes
- Sincronizacao de calendarios (iCal)
- Deteccao automatica de conflitos
- Dashboard e estatisticas
- Bot Telegram funcional
- Health checks e monitoramento

### MVP 2 - Automacoes (70% COMPLETO)
- Sistema de email universal (IMAP/SMTP) - **IMPLEMENTADO**
- Geracao automatica de documentos DOCX - **IMPLEMENTADO**
- Templates de email profissionais - **IMPLEMENTADO**
- Notificacoes push via Telegram - **IMPLEMENTADO**
- WhatsApp integration - **NAO INICIADO**

### MVP 3 - IA e Automacao Avancada (0% COMPLETO)
- Integracao com Ollama/Gemma - **NAO INICIADO**
- Parsing inteligente de emails - **NAO INICIADO**
- Analise preditiva de ocupacao - **NAO INICIADO**

---

## Documentos por Categoria

### Status e Planejamento
- [Status MVP Atual](status/STATUS_MVP_ATUAL.md) - Status completo e detalhado
- [MVP1 Checklist](status/MVP1_CHECKLIST.md) - Checklist do MVP1
- [MVP2 Implementacao](status/MVP2_IMPLEMENTACAO.md) - Status do MVP2
- [Resumo Final MVP1](status/RESUMO_FINAL_MVP1.md) - Resumo da implementacao
- [Proximos Passos](guides/PROXIMOS_PASSOS.md) - Roadmap de features

### Seguranca (LEIA COM ATENCAO!)
- [Auditoria Detalhada](security/AUDITORIA_SEGURANCA_DETALHADA.md) - **22 vulnerabilidades encontradas!**
- [Vulnerabilidades Criticas](reports/VULNERABILIDADES_CRITICAS.md) - Resumo executivo
- [Seguranca Implementada](security/SEGURANCA_IMPLEMENTADA.md) - JWT, bcrypt, rate limiting
- [Correcoes Urgentes](security/SEGURANCA_FASE1_URGENTE.md) - O que corrigir AGORA
- [Preparacao VPS](security/SEGURANCA_FASE2_VPS.md) - HTTPS, Fail2ban, hardening

### Guias Praticos
- [Instalacao Completa](guides/GUIA_INSTALACAO.md) - **COMECE AQUI SE FOR INICIANTE**
- [Como Iniciar](guides/COMO_INICIAR.md) - Quick start para devs
- [Uso Diario](guides/GUIA_USO_DIARIO.md) - Como usar o sistema
- [API](guides/GUIA_API.md) - Endpoints e exemplos
- [Telegram Bot](guides/GUIA_TELEGRAM.md) - Comandos e configuracao
- [Checklist de Producao](guides/CHECKLIST_PRODUCAO.md) - Pre-deploy
- [Tornar Utilizavel](guides/TORNAR_UTILIZAVEL.md) - Melhorias de UX

### Arquitetura e Desenvolvimento
- [Estrutura do Projeto](PROJECT_STRUCTURE.md) - Organizacao do codigo
- [Arquitetura Geral](architecture/ARQUITETURA_GERAL.md) - Visao do sistema
- [Banco de Dados](architecture/BANCO_DE_DADOS.md) - Models e relacionamentos
- [Integracao de Calendarios](architecture/INTEGRACAO_CALENDARIOS.md) - Sincronizacao iCal
- [API Documentation](API_DOCUMENTATION.md) - Endpoints completos
- [Frontend Guide](FRONTEND_GUIDE.md) - Interface React
- [Arquitetura Interface Web](ARQUITETURA_INTERFACE_WEB.md) - Components

### Features Especificas
- [Calendario e Conflitos](CALENDARIO_E_CONFLITOS.md) - Sistema de deteccao
- [Dashboard e Estatisticas](DASHBOARD_E_ESTATISTICAS.md) - Metricas e visualizacao
- [Telegram Bot](TELEGRAM_BOT.md) - Implementacao detalhada
- [Automacao de Plataformas](AUTOMACAO_PLATAFORMAS.md) - Integracao Airbnb/Booking

### Deployment e Infraestrutura
- [Deployment VPS](deployment/DEPLOYMENT_VPS.md) - Setup completo
- [Docker Deployment](deployment/DOCKER_DEPLOYMENT.md) - Containerizacao
- [Quick Start VPS](deployment/README_VPS_DEPLOYMENT.md) - Deploy rapido
- [DevOps e Infraestrutura](DEVOPS_INFRAESTRUTURA.md) - CI/CD, monitoramento

### Relatorios e Analises
- [Bugs Conhecidos](reports/BUGS_ENCONTRADOS.md) - Lista de bugs
- [Vulnerabilidades](reports/VULNERABILIDADES_CRITICAS.md) - Seguranca
- [Analise de Codigo](reports/ANALISE_CODIGO.md) - Code review
- [Auditoria de Codigo](AUDITORIA_CODIGO.md) - Quality check

### Escalabilidade e Comercial (Futuro)
- [Plano Comercial](PLANO_COMERCIAL_ESCALABILIDADE.md) - Estrategia SaaS
- [Migracao Multi-tenant](MIGRAR_PARA_MULTITENANT.md) - Arquitetura multi-tenant
- [Integracao Stripe](INTEGRACAO_STRIPE_BILLING.md) - Sistema de pagamento
- [Roadmap Completo](ROADMAP_EXECUCAO_COMPLETO.md) - Roadmap de crescimento
- [Protocolos de Seguranca](PROTOCOLOS_SEGURANCA_ESCALABILIDADE.md) - Seguranca avancada

---

## Avisos Importantes

### SEGURANCA CRITICA
O sistema possui **3 vulnerabilidades criticas** e **5 de alta severidade** identificadas na auditoria:

1. **JWT Payload vaza informacoes** - Email, username e is_admin expostos
2. **Timing attack em login** - Permite user enumeration
3. **Sem bloqueio de conta** - Brute force possivel
4. **Sem token revocation** - Logout nao invalida tokens
5. **Sem protecao CSRF** - Ataques cross-site possiveis

**NAO FAZER DEPLOY EM PRODUCAO** ate corrigir as vulnerabilidades criticas!

Ver: [Auditoria Detalhada](security/AUDITORIA_SEGURANCA_DETALHADA.md)

### Tarefas Prioritarias

**Prioridade 1 - URGENTE** (4-6 horas):
1. Corrigir JWT payload
2. Implementar token blacklist
3. Corrigir timing attack
4. Implementar account lockout

**Prioridade 2 - ALTA** (8-10 horas):
1. Rate limiting global
2. CSRF protection
3. Audit logging
4. Melhorar error handling

Veja: [Correcoes Urgentes](security/SEGURANCA_FASE1_URGENTE.md)

---

## Comecando

### Para Usuarios Iniciantes
1. Leia o [Guia de Instalacao](guides/GUIA_INSTALACAO.md) completo
2. Configure o `.env` conforme o guia
3. Inicie o backend e frontend
4. Acesse http://localhost:5173
5. Consulte o [Guia de Uso Diario](guides/GUIA_USO_DIARIO.md)

### Para Desenvolvedores
1. Clone o repositorio
2. Leia [Como Iniciar](guides/COMO_INICIAR.md)
3. Revise a [Estrutura do Projeto](PROJECT_STRUCTURE.md)
4. Consulte a [API Documentation](API_DOCUMENTATION.md)
5. Contribua seguindo as convencoes do projeto

### Para Deploy em Producao
1. **PRIMEIRO**: Corrija as [Vulnerabilidades Criticas](reports/VULNERABILIDADES_CRITICAS.md)
2. Complete o [Checklist de Producao](guides/CHECKLIST_PRODUCAO.md)
3. Siga o [Deployment VPS](deployment/DEPLOYMENT_VPS.md) ou [Docker](deployment/DOCKER_DEPLOYMENT.md)
4. Configure HTTPS com Let's Encrypt
5. Habilite monitoring e backups

---

## Stack Tecnologico

**Backend**: FastAPI, SQLAlchemy, Pydantic, JWT, Bcrypt
**Database**: SQLite (dev) / PostgreSQL (prod)
**Frontend**: React, Vite, TailwindCSS (em desenvolvimento)
**Integracao**: Telegram Bot API, iCal, IMAP/SMTP
**Documentos**: python-docx, docxtpl, Jinja2
**Deployment**: Docker, Nginx, Let's Encrypt, Systemd, Fail2ban
**Monitoramento**: psutil, Loguru, Health checks

---

## Suporte e Contribuicao

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/AP_Controller/issues)
- **Documentacao**: Esta pasta `docs/`
- **Email**: contato@sentinel.com (exemplo)

---

## Licenca

MIT License - Ver arquivo LICENSE na raiz do projeto

---

**Feito com dedicacao para facilitar a gestao de apartamentos**

**Ultima Atualizacao**: 2026-02-04
**Versao da Documentacao**: 1.0.0
