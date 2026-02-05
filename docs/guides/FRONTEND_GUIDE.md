# 🌐 SENTINEL Frontend - Guia Completo

## 📋 Visão Geral

Interface web moderna construída com **React + Vite** para gerenciamento do apartamento listado no Airbnb e Booking.com.

---

## ✨ Funcionalidades Implementadas

### 1. **Sidebar Navegável** ✅
- Colapsa/expande com botão
- Ícones para cada seção
- Indicador de página ativa
- Status do sistema (online/offline)

### 2. **Dashboard** ✅
- Cards de estatísticas (Total de Reservas, Reservas Ativas, Conflitos, Ocupação)
- Próximas reservas listadas
- Alertas de conflitos
- Informações do sistema (última sync, próxima sync, check-ins/outs)

### 3. **Configurações** ✅
- **Aba Fácil:**
  - Dados do imóvel (nome, endereço, max hóspedes)
  - Dados do condomínio (nome, administração)
  - URLs iCal (Airbnb + Booking)
  - Instruções de como obter URLs

- **Aba Avançada:**
  - Intervalo de sincronização
  - Telegram Bot (preparado para MVP2)
  - Features toggles
  - Campos desabilitados para futuras funcionalidades

### 4. **Integração com Backend** ✅
- Axios configurado com proxy para `/api`
- Serviços organizados por domínio:
  - `bookingsAPI`
  - `calendarAPI`
  - `conflictsAPI`
  - `statisticsAPI`
  - `syncActionsAPI`
  - `systemAPI`
  - `settingsAPI`

---

## 🚧 Funcionalidades Pendentes

### Calendário Interativo
- View mensal com eventos
- Código de cores por plataforma (Airbnb/Booking)
- Clique para ver detalhes da reserva
- Navegação entre meses

### Visualização de Conflitos
- Lista de conflitos ativos
- Tipo (duplicata/sobreposição)
- Severidade (critical/high/medium/low)
- Botão para resolver com notas
- Detalhes de cada reserva conflitante

### Estatísticas Detalhadas
- Gráficos de ocupação mensal
- Receita por período
- Comparação entre plataformas
- Taxa de ocupação por mês

---

## 📁 Estrutura do Projeto

```
frontend/
├── public/             # Assets estáticos
├── src/
│   ├── components/     # Componentes reutilizáveis
│   │   ├── Sidebar.jsx
│   │   └── Sidebar.css
│   ├── pages/          # Páginas da aplicação
│   │   ├── Dashboard.jsx     ✅ Implementado
│   │   ├── Dashboard.css
│   │   ├── Settings.jsx      ✅ Implementado
│   │   ├── Settings.css
│   │   ├── Calendar.jsx      🚧 Placeholder
│   │   ├── Conflicts.jsx     🚧 Placeholder
│   │   ├── Statistics.jsx    🚧 Placeholder
│   │   └── Placeholder.css
│   ├── services/       # Comunicação com backend
│   │   └── api.js
│   ├── styles/         # Estilos globais
│   │   └── global.css
│   ├── App.jsx         # Componente raiz
│   ├── App.css
│   └── main.jsx        # Entry point
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

---

## 🎨 Design System

### Cores
```css
--primary: #2563eb       /* Azul principal */
--primary-dark: #1e40af  /* Azul escuro (hover) */
--success: #10b981       /* Verde (sucesso) */
--warning: #f59e0b       /* Amarelo (aviso) */
--danger: #ef4444        /* Vermelho (erro/conflito) */
--bg-primary: #ffffff    /* Fundo branco */
--bg-secondary: #f8fafc  /* Fundo cinza claro */
--text-primary: #0f172a  /* Texto principal */
--text-secondary: #64748b /* Texto secundário */
```

### Componentes Reutilizáveis
- `.card` - Cartões com sombra
- `.btn` - Botões (primary, secondary, danger)
- `.input` - Campos de formulário
- `.badge` - Tags coloridas
- `.label` - Labels de formulário

---

## 🔌 API Integration

### Configuração do Proxy
O Vite está configurado para redirecionar todas as requisições `/api/*` para o backend em `http://127.0.0.1:8000`.

```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### Exemplo de Uso da API

```javascript
import { statisticsAPI } from './services/api';

// Buscar dashboard
const response = await statisticsAPI.getDashboard(1);
console.log(response.data);

// Sincronizar calendários
await calendarAPI.sync();

// Resolver conflito
await conflictsAPI.resolve(conflictId, 'Reserva do Airbnb cancelada');
```

---

## 🚀 Como Iniciar

### Opção 1: Apenas Frontend
```bash
cd frontend
npm install
npm run dev
```
Acesse: `http://localhost:5173`

### Opção 2: Frontend + Backend Juntos
```bash
# Na raiz do projeto
scripts\start_all.bat
```

Isso iniciará:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:5173`

---

## 📝 Dados Editáveis via Interface

Todas essas configurações podem ser alteradas na página **Configurações**:

### Aba Fácil
- ✅ Nome do imóvel
- ✅ Endereço completo
- ✅ Máximo de hóspedes
- ✅ Nome do condomínio
- ✅ Nome da administração
- ✅ URL iCal Airbnb
- ✅ URL iCal Booking

### Aba Avançada
- ✅ Intervalo de sincronização (minutos)
- 🚧 Token do bot Telegram (MVP2)
- 🚧 IDs de usuários admin (MVP2)
- ✅ Notificações de conflitos (toggle)
- 🚧 Geração automática de documentos (toggle - MVP2)

---

## 🔄 Fluxo de Dados

```
┌─────────────┐
│  Frontend   │
│ (React App) │
└──────┬──────┘
       │ HTTP
       │ /api/*
       ↓
┌─────────────┐
│   Vite      │
│   Proxy     │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Backend    │
│  FastAPI    │
│  :8000      │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  SQLite DB  │
│ sentinel.db │
└─────────────┘
```

---

## 🎯 Próximos Passos para Desenvolvimento

### Prioridade 1: Calendário
1. Instalar biblioteca de calendário (ex: `react-big-calendar` ou `fullcalendar`)
2. Buscar eventos via `calendarAPI.getEvents()`
3. Renderizar eventos coloridos por plataforma
4. Adicionar modal de detalhes ao clicar no evento

### Prioridade 2: Conflitos
1. Buscar conflitos via `conflictsAPI.getAll()`
2. Renderizar lista com cards
3. Mostrar detalhes de cada reserva conflitante
4. Adicionar formulário de resolução
5. Chamar `conflictsAPI.resolve()` com notas

### Prioridade 3: Estatísticas
1. Instalar biblioteca de gráficos (ex: `recharts` ou `chart.js`)
2. Buscar dados via `statisticsAPI`
3. Criar gráfico de ocupação mensal
4. Criar gráfico de receita
5. Criar comparação entre plataformas

---

## 🐛 Troubleshooting

**Frontend não conecta com backend:**
- Verifique se o backend está rodando em `http://127.0.0.1:8000`
- Teste acessando `http://127.0.0.1:8000/docs`
- Verifique o proxy no `vite.config.js`

**Erro ao instalar dependências:**
```bash
# Limpar cache do npm
npm cache clean --force

# Deletar node_modules e reinstalar
rm -rf node_modules package-lock.json
npm install
```

**Porta 5173 em uso:**
```bash
# Matar processo na porta 5173
npx kill-port 5173

# Ou alterar porta no vite.config.js
server: { port: 3000 }
```

---

## 📚 Tecnologias Utilizadas

- **React 18** - Framework UI
- **Vite** - Build tool ultra-rápido
- **Axios** - HTTP client
- **Lucide React** - Biblioteca de ícones
- **date-fns** - Manipulação de datas

---

## ✅ Checklist de Qualidade

- [x] Código organizado por feature
- [x] CSS modular (um arquivo por componente)
- [x] Variáveis CSS para cores e espaçamentos
- [x] Componentes reutilizáveis
- [x] Error handling nas chamadas API
- [x] Loading states
- [x] Empty states
- [x] Responsividade básica
- [ ] Testes unitários (TODO)
- [ ] Testes E2E (TODO)

---

**Status:** Frontend MVP1 Base - Pronto para desenvolvimento das features restantes! 🚀
