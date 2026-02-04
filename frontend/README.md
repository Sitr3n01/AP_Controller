# SENTINEL Frontend

Interface web para gerenciamento do apartamento.

## 🚀 Início Rápido

```bash
# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Acessar em: http://localhost:5173
```

## 📁 Estrutura

```
frontend/
├── src/
│   ├── components/     # Componentes reutilizáveis
│   │   └── Sidebar.jsx
│   ├── pages/          # Páginas da aplicação
│   │   ├── Dashboard.jsx
│   │   ├── Calendar.jsx
│   │   ├── Conflicts.jsx
│   │   ├── Statistics.jsx
│   │   └── Settings.jsx
│   ├── services/       # API calls
│   │   └── api.js
│   ├── styles/         # Estilos globais
│   │   └── global.css
│   ├── App.jsx         # Componente principal
│   └── main.jsx        # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 Funcionalidades

### ✅ Implementado

- Sidebar navegável (colapsa/expande)
- Dashboard com estatísticas
- Página de Configurações (Fácil/Avançada)
- Integração com API REST do backend
- Design responsivo

### 🚧 Em Desenvolvimento

- Calendário interativo
- Visualização de conflitos
- Gráficos de estatísticas

## 🔧 Configuração

O frontend se conecta automaticamente ao backend em `http://127.0.0.1:8000`.

Todas as configurações do sistema podem ser editadas na página **Configurações**:

- **Aba Fácil:** Dados do imóvel, condomínio e URLs iCal
- **Aba Avançada:** Sincronização, Telegram, features

## 📝 Scripts

- `npm run dev` - Servidor de desenvolvimento
- `npm run build` - Build para produção
- `npm run preview` - Preview do build

## 🎯 Próximos Passos

1. Implementar calendário completo
2. Adicionar visualização de conflitos
3. Criar gráficos de estatísticas
4. Adicionar gestão de reservas (CRUD)
