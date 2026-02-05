# 🌐 Arquitetura da Interface Web - SENTINEL

## 📋 Visão Geral

**Estratégia:**
- 🌐 **Interface Web** = Centro de Controle (Desktop + Mobile)
- 📱 **Telegram Bot** = Alertas + Aprovações Rápidas (notificações push)
- 🔄 **Backend** = FastAPI (já implementado)

```
┌─────────────────────────────────────────────┐
│                                             │
│         INTERFACE WEB (React)               │
│      Centro de Controle Principal           │
│                                             │
│  • Calendário visual consolidado            │
│  • Gestão de reservas                       │
│  • Histórico de hóspedes                    │
│  • Configurações do apartamento             │
│  • Geração de documentos                    │
│  • Análise de dados                         │
│                                             │
└──────────────┬──────────────────────────────┘
               │
               │ REST API
               │
┌──────────────▼──────────────────────────────┐
│                                             │
│         BACKEND (FastAPI)                   │
│          (Já Implementado)                  │
│                                             │
│  • Sincronização iCal                       │
│  • Detecção de conflitos                    │
│  • Banco de dados SQLite                    │
│  • Lógica de negócio                        │
│                                             │
└──────────────┬──────────────────────────────┘
               │
               │ Notificações
               │
┌──────────────▼──────────────────────────────┐
│                                             │
│        TELEGRAM BOT (Opcional)              │
│         Notificações Push                   │
│                                             │
│  • Alertas de conflitos                     │
│  • Notificações de novas reservas           │
│  • Aprovações rápidas (Sim/Não)            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎨 Design da Interface Web

### Stack Tecnológica Recomendada

**Frontend:**
- **Framework:** React 18 + TypeScript
- **Routing:** React Router v6
- **UI Components:** shadcn/ui + Tailwind CSS
- **Calendário:** FullCalendar.io ou React Big Calendar
- **Estado:** Zustand (simples) ou React Query
- **Build:** Vite
- **Mobile:** Responsivo (mobile-first)

**Backend (já temos):**
- **API:** FastAPI
- **Auth:** JWT tokens (opcional para MVP)
- **CORS:** Configurado para localhost:3000

**Deployment:**
- **Dev:** Local (mesmo PC rodando backend)
- **Prod:** Mesma máquina Windows (IIS ou nginx)

---

## 📱 Páginas e Funcionalidades

### 1. Dashboard (Página Inicial)

```
┌─────────────────────────────────────────────────┐
│  🏠 SENTINEL - Apartamento Goiânia              │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Visão Geral                                 │
│  ┌─────────────┬─────────────┬─────────────┐  │
│  │ 📅 Reservas │ ⚠️ Conflitos│ 📈 Ocupação │  │
│  │     15      │      2      │     78%     │  │
│  └─────────────┴─────────────┴─────────────┘  │
│                                                 │
│  📍 Status Atual                                │
│  ┌──────────────────────────────────────────┐  │
│  │ 🟢 OCUPADO                                │  │
│  │ João Silva (Airbnb)                      │  │
│  │ Check-out: 15/03/2024 (em 2 dias)       │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  📅 Próximas 3 Reservas                        │
│  ┌──────────────────────────────────────────┐  │
│  │ 🏠 18/03 - Maria Santos (Airbnb) 5n     │  │
│  │ 🏨 25/03 - Pedro Alves (Booking) 3n     │  │
│  │ 🏠 30/03 - Ana Costa (Airbnb) 7n        │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ⚠️ Alertas Pendentes (2)                      │
│  ┌──────────────────────────────────────────┐  │
│  │ 🚨 Conflito: 18-20/03 (Airbnb x Booking)│  │
│  │    [Ver Detalhes] [Resolver]            │  │
│  ├──────────────────────────────────────────┤  │
│  │ 📋 Bloquear 25/03 no Booking.com        │  │
│  │    [Abrir Link] [Marcar Feito]          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  [📅 Ir para Calendário] [📊 Relatórios]      │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Componentes:**
- Cards de estatísticas (reservas, conflitos, ocupação)
- Status atual do apartamento (ocupado/vazio)
- Lista de próximas reservas (com avatar da plataforma)
- Alertas pendentes com botões de ação
- Links rápidos

---

### 2. Calendário Consolidado

**Visualização Principal:**

```
┌───────────────────────────────────────────────────┐
│  📅 CALENDÁRIO - Março 2024           [Hoje]      │
├───────────────────────────────────────────────────┤
│                                                   │
│  [◄ Fev]  Março 2024  [Abr ►]  [Mês][Semana][Dia]│
│                                                   │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐    │
│  │ Dom │ Seg │ Ter │ Qua │ Qui │ Sex │ Sáb │    │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤    │
│  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │    │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤    │
│  │  8  │  9  │ 10  │ 11  │ 12  │ 13  │ 14  │    │
│  │     │     │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│     │    │
│  │     │     │ João Silva (Airbnb)  │     │    │
│  │     │     │ 5 noites - R$ 950    │     │    │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤    │
│  │ 15  │ 16  │ 17  │ 18  │ 19  │ 20  │ 21  │    │
│  │     │     │     │ ████████████████│     │    │
│  │     │     │     │ Maria (Airbnb) │     │    │
│  │     │     │     │ ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️│     │    │
│  │     │     │     │ Pedro (Booking)│     │    │
│  │     │     │     │ CONFLITO!      │     │    │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤    │
│  │ 22  │ 23  │ 24  │ 25  │ 26  │ 27  │ 28  │    │
│  │     │     │     │ ░░░░░░░░░░░░░░│     │     │
│  │     │     │     │ Ana (Airbnb)  │     │     │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘    │
│                                                   │
│  Legenda:                                         │
│  ▓▓ Airbnb  ░░ Booking  ⚠️ Conflito  ⬜ Livre   │
│                                                   │
│  [+ Bloquear Período] [Sincronizar Agora]       │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Recursos:**
- Visualização mensal/semanal/diária
- Cores diferentes para Airbnb (azul) e Booking (verde)
- Conflitos em vermelho com padrão listrado
- Click em reserva = modal com detalhes
- Drag & drop para criar bloqueios (futuro)
- Sincronização manual com botão

**Modal de Detalhes da Reserva:**
```
┌─────────────────────────────────────┐
│  Reserva - João Silva               │
├─────────────────────────────────────┤
│                                     │
│  🏠 Plataforma: Airbnb              │
│  👤 Hóspede: João Silva             │
│  📅 Check-in: 10/03/2024 14:00     │
│  📅 Check-out: 15/03/2024 12:00    │
│  🌙 Noites: 5                       │
│  💰 Valor: R$ 950,00                │
│  📧 Email: joao@email.com           │
│  📱 Telefone: (62) 99999-9999      │
│                                     │
│  🚗 Veículo                         │
│  Placa: ABC-1234                    │
│  Modelo: Fiat Uno                   │
│                                     │
│  📄 Documentos                      │
│  ✅ Autorização condomínio enviada  │
│     15/02/2024 10:30               │
│     [📥 Download]                   │
│                                     │
│  [✏️ Editar] [📄 Gerar Doc]        │
│  [🗑️ Cancelar Reserva]             │
│                                     │
└─────────────────────────────────────┘
```

---

### 3. Gestão de Reservas

```
┌────────────────────────────────────────────────────┐
│  📋 RESERVAS                                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  Filtros: [Todas ▼] [Airbnb ▼] [Mês ▼] [🔍]     │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🏠 João Silva (Airbnb)                       │ │
│  │ 10-15/03/2024 • 5 noites • R$ 950           │ │
│  │ ✅ Ativo | 📄 Doc enviado | 🚗 Veículo OK   │ │
│  │ [Ver] [Editar] [Documento]                  │ │
│  ├──────────────────────────────────────────────┤ │
│  │ 🏨 Maria Santos (Booking)                    │ │
│  │ 18-22/03/2024 • 4 noites • R$ 680           │ │
│  │ ⚠️ Conflito | ❌ Doc pendente | - Veículo    │ │
│  │ [Ver] [Editar] [Gerar Doc]                  │ │
│  ├──────────────────────────────────────────────┤ │
│  │ 🏠 Pedro Alves (Airbnb)                      │ │
│  │ 25-28/03/2024 • 3 noites • R$ 570           │ │
│  │ ✅ Ativo | ⏳ Doc em processo | - Veículo    │ │
│  │ [Ver] [Editar] [Documento]                  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  Página 1 de 3   [◄] [1] [2] [3] [►]            │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Lista de todas as reservas
- Filtros (plataforma, status, período)
- Busca por nome do hóspede
- Indicadores visuais de status
- Ações rápidas por reserva

---

### 4. Histórico de Hóspedes

```
┌────────────────────────────────────────────────────┐
│  👥 HÓSPEDES                                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  [🔍 Buscar hóspede...]                           │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ 👤 João Silva                    ⭐⭐⭐⭐⭐    │ │
│  │ 📧 joao@email.com | 📱 (62) 99999-9999      │ │
│  │ 📄 CPF: 123.456.789-00                       │ │
│  │                                              │ │
│  │ 🏠 Histórico de Reservas (3x)               │ │
│  │ • 10-15/03/2024 (Airbnb) ✅                 │ │
│  │ • 05-10/01/2024 (Airbnb) ✅                 │ │
│  │ • 20-25/11/2023 (Booking) ✅                │ │
│  │                                              │ │
│  │ 🚗 Veículo Cadastrado                       │ │
│  │ Fiat Uno - ABC-1234 (Prata)                 │ │
│  │                                              │ │
│  │ 📝 Notas                                     │ │
│  │ "Hóspede educado, deixa apto limpo"         │ │
│  │                                              │ │
│  │ [✏️ Editar] [📄 Docs] [🗑️ Arquivar]        │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ 👤 Maria Santos                  ⭐⭐⭐⭐☆    │ │
│  │ 📧 maria@email.com | 📱 (62) 98888-8888    │ │
│  │ 🏠 Histórico (1x)                           │ │
│  │ [Ver Detalhes]                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Dados armazenados:**
- Informações pessoais (nome, email, telefone, CPF)
- Histórico completo de reservas
- Veículos cadastrados
- Avaliação/notas internas
- Documentos gerados

---

### 5. Conflitos e Ações

```
┌────────────────────────────────────────────────────┐
│  ⚠️ CONFLITOS E AÇÕES PENDENTES                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  🚨 Conflitos Ativos (2)                          │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🔴 CRÍTICO - Sobreposição 18-20/03           │ │
│  │                                              │ │
│  │ 🏠 AIRBNB: Maria Santos                      │ │
│  │    18-22/03/2024 (4 noites)                 │ │
│  │                                              │ │
│  │ 🏨 BOOKING: Pedro Alves                      │ │
│  │    18-20/03/2024 (2 noites)                 │ │
│  │                                              │ │
│  │ ⚠️ Sobreposição: 2 noites                   │ │
│  │                                              │ │
│  │ Sugestão: Manter Airbnb (chegou primeiro)   │ │
│  │                                              │ │
│  │ [📱 Contatar Booking] [✅ Marcar Resolvido] │ │
│  │ [📝 Adicionar Nota]                         │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  📋 Ações Pendentes (3)                           │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🔴 Bloquear 18-20/03 no Booking.com         │ │
│  │ Prioridade: Alta                            │ │
│  │ Motivo: Conflito com reserva Airbnb         │ │
│  │ [🔗 Abrir Booking] [✅ Concluído]          │ │
│  ├──────────────────────────────────────────────┤ │
│  │ ⚠️ Gerar documento: João Silva              │ │
│  │ Prioridade: Média                           │ │
│  │ [📄 Gerar Agora] [⏰ Lembrar Depois]       │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ✅ Ações Concluídas Recentes (5)                │
│  [Ver Histórico]                                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

### 6. Documentos

```
┌────────────────────────────────────────────────────┐
│  📄 DOCUMENTOS                                     │
├────────────────────────────────────────────────────┤
│                                                    │
│  📁 Autorizações do Condomínio                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ 📄 autorizacao_joao_silva_10-15mar.pdf       │ │
│  │ 15/02/2024 10:30 | João Silva | Airbnb      │ │
│  │ ✅ Enviado: admin@condominio.com.br          │ │
│  │ [📥 Download] [📧 Reenviar] [👁️ Visualizar] │ │
│  ├──────────────────────────────────────────────┤ │
│  │ 📄 autorizacao_maria_santos_18-22mar.pdf    │ │
│  │ 20/02/2024 14:15 | Maria Santos | Booking   │ │
│  │ ✅ Enviado: admin@condominio.com.br          │ │
│  │ [📥 Download] [📧 Reenviar] [👁️ Visualizar] │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  📊 Templates                                      │
│  ┌──────────────────────────────────────────────┐ │
│  │ 📝 autorizacao_condominio.docx               │ │
│  │ Última atualização: 01/02/2024              │ │
│  │ [✏️ Editar] [📤 Fazer Upload Novo]          │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  [📄 Gerar Novo Documento]                        │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

### 7. Configurações do Apartamento

```
┌────────────────────────────────────────────────────┐
│  ⚙️ CONFIGURAÇÕES                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  🏠 Dados do Imóvel                               │
│  ┌──────────────────────────────────────────────┐ │
│  │ Nome: [Apartamento 2 Quartos - Goiânia]     │ │
│  │ Endereço: [Rua Exemplo, 123...]             │ │
│  │ CEP: [74000-000]                             │ │
│  │ Capacidade: [4 hóspedes]                     │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  🏢 Condomínio                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Nome: [Condomínio Exemplo]                   │ │
│  │ Administração: [Administração do Condomínio] │ │
│  │ Email: [admin@condominio.com.br]            │ │
│  │ Telefone: [(62) 3333-3333]                  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  🔗 Integrações                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🏠 Airbnb                                    │ │
│  │ URL iCal: [airbnb.com/calendar/ical/...]    │ │
│  │ Status: ✅ Conectado                         │ │
│  │ Última sync: há 15 minutos                  │ │
│  │ [🔄 Sincronizar] [✏️ Editar]                │ │
│  ├──────────────────────────────────────────────┤ │
│  │ 🏨 Booking.com                               │ │
│  │ URL iCal: [admin.booking.com/ical/...]      │ │
│  │ Status: ✅ Conectado                         │ │
│  │ Última sync: há 15 minutos                  │ │
│  │ [🔄 Sincronizar] [✏️ Editar]                │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  📧 Notificações                                   │
│  ┌──────────────────────────────────────────────┐ │
│  │ 📱 Telegram                                  │ │
│  │ Status: ⚠️ Não configurado                   │ │
│  │ [⚙️ Configurar Bot]                          │ │
│  ├──────────────────────────────────────────────┤ │
│  │ 📧 Email (SMTP)                              │ │
│  │ Servidor: [smtp.gmail.com]                  │ │
│  │ Status: ✅ Configurado                       │ │
│  │ [✏️ Editar] [📧 Testar Envio]               │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  [💾 Salvar Alterações] [🔄 Restaurar Padrões]   │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

### 8. Relatórios e Estatísticas

```
┌────────────────────────────────────────────────────┐
│  📊 RELATÓRIOS E ANÁLISES                         │
├────────────────────────────────────────────────────┤
│                                                    │
│  📅 Período: [Março 2024 ▼] [📥 Exportar PDF]    │
│                                                    │
│  📈 Estatísticas                                   │
│  ┌──────────────┬──────────────┬──────────────┐  │
│  │ 📅 Reservas  │ 🌙 Noites    │ 💰 Receita   │  │
│  │     15       │     385      │  R$ 7.650    │  │
│  │  +25% ↑     │  +30% ↑      │  +20% ↑     │  │
│  └──────────────┴──────────────┴──────────────┘  │
│                                                    │
│  📊 Taxa de Ocupação (Março)                      │
│  ████████████████░░░░░░░░ 78% (23/30 dias)       │
│                                                    │
│  🏠 Por Plataforma                                │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🏠 Airbnb:   60% (9 reservas)                │ │
│  │ 🏨 Booking:  40% (6 reservas)                │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  📊 Gráfico de Ocupação (Últimos 6 meses)        │
│  ┌──────────────────────────────────────────────┐ │
│  │      ██                                      │ │
│  │      ██        ██                            │ │
│  │  ██  ██    ██  ██  ██    ██                 │ │
│  │  ██  ██    ██  ██  ██    ██                 │ │
│  │  Out Nov    Dez Jan Fev    Mar              │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  👥 Top 5 Hóspedes Recorrentes                    │
│  1. João Silva (3x) ⭐⭐⭐⭐⭐                     │
│  2. Maria Santos (2x) ⭐⭐⭐⭐☆                    │
│  3. Pedro Alves (2x) ⭐⭐⭐☆☆                     │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints Necessários (FastAPI)

### Endpoints já prontos (Backend atual):
- ✅ `GET /api/bookings` - Listar reservas
- ✅ `GET /api/bookings/{id}` - Detalhes da reserva
- ✅ `GET /api/conflicts` - Listar conflitos
- ✅ `GET /api/sync-actions` - Ações pendentes
- ✅ `POST /api/sync` - Forçar sincronização

### Endpoints a criar:
```python
# Reservas
GET    /api/bookings/current         # Reserva atual
GET    /api/bookings/upcoming        # Próximas reservas
POST   /api/bookings/{id}/cancel     # Cancelar reserva
PUT    /api/bookings/{id}            # Atualizar reserva

# Hóspedes
GET    /api/guests                   # Listar hóspedes
GET    /api/guests/{id}              # Detalhes do hóspede
POST   /api/guests                   # Criar hóspede
PUT    /api/guests/{id}              # Atualizar hóspede

# Documentos
GET    /api/documents                # Listar documentos
POST   /api/documents/generate       # Gerar documento
GET    /api/documents/{id}/download  # Download PDF

# Conflitos
PUT    /api/conflicts/{id}/resolve   # Marcar conflito resolvido

# Ações
PUT    /api/sync-actions/{id}/complete  # Completar ação
PUT    /api/sync-actions/{id}/dismiss   # Descartar ação

# Estatísticas
GET    /api/statistics/dashboard     # Dashboard
GET    /api/statistics/monthly       # Relatório mensal
GET    /api/statistics/occupancy     # Taxa de ocupação

# Configurações
GET    /api/settings                 # Buscar configurações
PUT    /api/settings                 # Atualizar configurações

# Calendário
GET    /api/calendar/events          # Eventos do calendário
POST   /api/calendar/block           # Bloquear período
```

---

## 🚀 Plano de Implementação da Web Interface

### FASE 5: Setup Frontend (Dia 16-17)
1. Criar projeto React com Vite
2. Configurar Tailwind CSS + shadcn/ui
3. Setup de rotas (React Router)
4. Configurar cliente API (axios/fetch)

### FASE 6: Dashboard + Calendário (Dia 18-20)
1. Página Dashboard
2. Calendário visual com FullCalendar
3. Integração com backend
4. Responsividade mobile

### FASE 7: CRUD Completo (Dia 21-23)
1. Gestão de reservas
2. Gestão de hóspedes
3. Conflitos e ações
4. Documentos

### FASE 8: Configurações + Relatórios (Dia 24-25)
1. Página de configurações
2. Relatórios e estatísticas
3. Exportação de dados

### FASE 9: Telegram Bot Simples (Dia 26-27)
1. Bot básico (apenas notificações)
2. Alertas de conflitos
3. Aprovações rápidas

---

## 📱 Estratégia Mobile-First

**Interface 100% responsiva:**
- Desktop: Sidebar + conteúdo amplo
- Tablet: Menu recolhível
- Mobile: Bottom navigation + cards verticais

**PWA (Progressive Web App):**
- Instalável no celular
- Funciona offline (dados em cache)
- Notificações push

Quer que eu comece implementando a estrutura do backend (APIs) ou prefere que eu crie o projeto React primeiro?