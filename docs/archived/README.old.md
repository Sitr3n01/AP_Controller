# 🏢 SENTINEL - Sistema de Gestão Automatizada de Apartamento

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP1%20Complete-success.svg)]()

Sistema completo de gestão de apartamentos com sincronização automática de calendários Airbnb e Booking.com, detecção inteligente de conflitos, dashboard interativo e bot do Telegram.

---

## 🎯 O QUE É O SENTINEL?

SENTINEL é uma plataforma all-in-one para proprietários e gestores de imóveis de aluguel que automatiza completamente o gerenciamento de reservas, evita overbooking e centraliza todas as informações em um único lugar.

### Problema que Resolve
- ❌ **Overbooking acidental** entre plataformas (Airbnb vs Booking)
- ❌ **Desorganização** de calendários e reservas
- ❌ **Trabalho manual** de sincronização
- ❌ **Falta de visibilidade** de métricas e estatísticas

### Solução
- ✅ **Sincronização automática** bidirecional de calendários
- ✅ **Detecção inteligente** de conflitos em tempo real
- ✅ **Dashboard visual** com gráficos e estatísticas
- ✅ **Bot do Telegram** para gerenciamento remoto
- ✅ **Notificações proativas** de novas reservas e problemas

---

## ✨ Funcionalidades Principais

### 🔄 Sincronização Automática
- Importação de reservas do Airbnb via iCal
- Importação de reservas do Booking.com via iCal
- Sincronização bidirecional (leitura e escrita)
- Detecção de novas, modificadas e canceladas

### 📊 Dashboard Interativo
- **8 cards de métricas principais**
- **Gráficos interativos (Recharts):**
  - Evolução da taxa de ocupação
  - Receita mensal
  - Distribuição por plataforma
  - Noites reservadas por mês
- Lista das próximas 5 reservas

### 📅 Calendário Visual
- Visualização mensal/semanal/diária
- Eventos coloridos por plataforma (🔴 Airbnb, 🔵 Booking, ⚪ Manual)
- Detalhes ao clicar no evento
- Filtros por propriedade e status

### ⚠️ Detecção de Conflitos
- Algoritmo inteligente identifica sobreposições
- 3 níveis de severidade (🔴 Crítico, 🟡 Alto, 🟢 Baixo)
- Sugestões de resolução automáticas

### 🤖 Bot do Telegram
- 9 comandos disponíveis (`/status`, `/reservas`, `/hoje`, `/sync`, etc)
- Notificações automáticas de reservas e conflitos
- Gerenciamento remoto completo

---

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Instalação (5 minutos)

**Windows:**
```cmd
INICIAR_SISTEMA.bat
```

**Linux/Mac:**
```bash
chmod +x iniciar_sistema.sh
./iniciar_sistema.sh
```

### Acesso
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs

### Configuração Completa
Siga o guia: **`docs/TORNAR_UTILIZAVEL.md`** (45 minutos)

---

## 📁 Estrutura do Projeto

```
sentinel-apartment-manager/
├── app/                      # Backend (FastAPI)
│   ├── api/v1/              # Endpoints REST
│   ├── models/              # Models SQLAlchemy
│   ├── services/            # Lógica de negócio
│   ├── telegram/            # Bot do Telegram
│   └── main.py
├── frontend/                 # Frontend (React + Vite)
│   └── src/pages/           # Dashboard, Calendar, Statistics
├── docs/                     # Documentação completa
├── data/                     # Database e logs
├── scripts/                  # Scripts utilitários
└── requirements.txt
```

---

## 📚 Documentação Completa

### Para Uso Imediato
- [TORNAR_UTILIZAVEL.md](docs/TORNAR_UTILIZAVEL.md) - Guia de 45 minutos
- [PRIMEIRO_UPLOAD_GITHUB.md](PRIMEIRO_UPLOAD_GITHUB.md) - Upload seguro para GitHub
- [PROXIMOS_PASSOS.md](PROXIMOS_PASSOS.md) - Guia de decisão

### Para Escalabilidade
- [IMPLEMENTAR_SEGURANCA.md](docs/IMPLEMENTAR_SEGURANCA.md) - Hardening de segurança
- [MIGRAR_PARA_MULTITENANT.md](docs/MIGRAR_PARA_MULTITENANT.md) - Arquitetura multi-tenant
- [INTEGRACAO_STRIPE_BILLING.md](docs/INTEGRACAO_STRIPE_BILLING.md) - Sistema de pagamentos
- [DEVOPS_INFRAESTRUTURA.md](docs/DEVOPS_INFRAESTRUTURA.md) - Deploy em produção
- [ROADMAP_EXECUCAO_COMPLETO.md](docs/ROADMAP_EXECUCAO_COMPLETO.md) - Roadmap MVP→SaaS

### Para Negócio
- [PLANO_COMERCIAL_ESCALABILIDADE.md](docs/PLANO_COMERCIAL_ESCALABILIDADE.md) - Modelo de negócio
- [PROTOCOLOS_SEGURANCA_ESCALABILIDADE.md](docs/PROTOCOLOS_SEGURANCA_ESCALABILIDADE.md) - Segurança para escala

---

## 🛠️ Tecnologias

**Backend:** FastAPI, SQLAlchemy, SQLite, python-telegram-bot
**Frontend:** React 18, Vite, Recharts, Axios
**DevOps:** Docker, Nginx, GitHub Actions, Prometheus + Grafana

---

## 🎯 Roadmap

- ✅ **MVP1** - Backend + Frontend + Bot (COMPLETO)
- 🔄 **Fase 2** - Segurança e autenticação JWT
- 📅 **Fase 3** - Arquitetura multi-tenant
- 💳 **Fase 4** - Billing com Stripe
- 🌐 **Fase 5** - Deploy em cloud e auto-scaling

---

## 📊 Métricas do Projeto

- **Linhas de código:** ~15.000
- **Endpoints API:** 25+
- **Componentes React:** 30+
- **Documentação:** 50.000+ palavras
- **Status:** MVP1 100% completo

---

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 💬 Suporte

### Dúvidas Técnicas
1. Consulte a [documentação completa](docs/)
2. Abra uma [issue](https://github.com/seu-usuario/sentinel-apartment-manager/issues)

---

<div align="center">

**Feito com ❤️ para proprietários de imóveis**

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐

</div>
