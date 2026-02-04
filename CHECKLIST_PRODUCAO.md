# ✅ Checklist de Produção - SENTINEL

## 📋 Use este checklist antes de começar a usar o sistema

---

## 1. ⚙️ PREPARAÇÃO DO AMBIENTE

### 1.1. Pré-Requisitos do Sistema
- [ ] Python 3.10 ou superior instalado
- [ ] Node.js 16 ou superior instalado
- [ ] Git instalado (opcional)
- [ ] Telegram instalado (opcional para bot)
- [ ] Navegador web moderno (Chrome, Firefox, Edge)

**Verificar:**
```bash
python --version
node --version
npm --version
```

---

## 2. 🧹 LIMPEZA E ORGANIZAÇÃO

### 2.1. Executar Script de Limpeza
- [ ] Executar `LIMPAR_PROJETO.bat`
- [ ] Verificar que `app/interfaces/` foi removida
- [ ] Verificar que arquivos .pyc foram removidos
- [ ] Verificar que backup do DB foi criado (se existir)

### 2.2. Verificar Estrutura
- [ ] Pasta `app/` existe e contém módulos
- [ ] Pasta `frontend/` existe
- [ ] Pasta `docs/` existe
- [ ] Pasta `data/` existe
- [ ] Arquivo `.env.example` existe
- [ ] Arquivo `requirements.txt` existe

---

## 3. 📝 CONFIGURAÇÃO

### 3.1. Criar Arquivo .env
- [ ] Copiar `.env.example` para `.env`
- [ ] Editar `.env` com editor de texto

### 3.2. Configurar Variáveis Obrigatórias

#### Aplicação
- [ ] `APP_NAME` = "Sentinel" (pode personalizar)
- [ ] `APP_ENV` = "production"
- [ ] `TIMEZONE` = "America/Sao_Paulo"

#### Dados do Apartamento
- [ ] `PROPERTY_NAME` = Nome do seu apartamento
- [ ] `PROPERTY_ADDRESS` = Endereço completo
- [ ] `CONDO_NAME` = Nome do condomínio
- [ ] `CONDO_ADMIN_NAME` = Nome da administradora

#### URLs dos Calendários iCal
- [ ] `AIRBNB_ICAL_URL` = URL do calendário Airbnb
- [ ] `BOOKING_ICAL_URL` = URL do calendário Booking.com

**Como obter as URLs:**

**Airbnb:**
1. Login no Airbnb
2. Acessar "Calendário"
3. Clicar em "Disponibilidade"
4. Copiar link "Exportar calendário"

**Booking.com:**
1. Login no Booking.com (painel de host)
2. Acessar "Calendário"
3. Procurar "Sincronização de calendário"
4. Copiar link iCal

### 3.3. Configurar Bot Telegram (OPCIONAL)

**Se NÃO quiser usar o bot:**
- [ ] Deixar `TELEGRAM_BOT_TOKEN` vazio
- [ ] Deixar `TELEGRAM_ADMIN_USER_IDS` vazio

**Se QUISER usar o bot:**
- [ ] Criar bot no @BotFather (ver `CONFIGURAR_BOT_TELEGRAM.txt`)
- [ ] `TELEGRAM_BOT_TOKEN` = Token do BotFather
- [ ] `TELEGRAM_ADMIN_USER_IDS` = Seu User ID

---

## 4. 📦 INSTALAÇÃO DE DEPENDÊNCIAS

### 4.1. Backend (Python)
- [ ] Abrir terminal/CMD na raiz do projeto
- [ ] Executar: `pip install -r requirements.txt`
- [ ] Aguardar instalação completa
- [ ] Verificar que não houve erros

**Se houver erro de compatibilidade:**
- Verificar versão do Python (deve ser 3.10+)
- Tentar com: `pip install --upgrade pip`
- Reinstalar: `pip install -r requirements.txt`

### 4.2. Frontend (React)
- [ ] Abrir terminal/CMD em `frontend/`
- [ ] Executar: `npm install`
- [ ] Aguardar instalação completa
- [ ] Executar: `npm install recharts`
- [ ] Ou usar: `frontend\instalar_recharts.bat`

---

## 5. 🗄️ INICIALIZAÇÃO DO BANCO DE DADOS

### 5.1. Criar Banco de Dados
- [ ] Executar: `python scripts/init_db.py`
- [ ] Verificar que `data/sentinel.db` foi criado
- [ ] Verificar mensagens de sucesso

**Mensagens esperadas:**
```
✅ Database initialized successfully!
✅ Created tables
✅ Created initial property
```

---

## 6. 🚀 PRIMEIRO TESTE

### 6.1. Iniciar Sistema
- [ ] Executar `INICIAR_SISTEMA.bat`
- [ ] Aguardar backends iniciarem

**Verificar mensagens:**
```
✅ Backend iniciado em http://localhost:8000
✅ Frontend iniciado em http://localhost:5173
✅ Bot do Telegram iniciado (se configurado)
```

### 6.2. Testar Backend
- [ ] Abrir navegador em `http://localhost:8000`
- [ ] Deve mostrar: `{"name": "Sentinel", "status": "online"}`
- [ ] Abrir `http://localhost:8000/docs`
- [ ] Deve mostrar documentação da API

### 6.3. Testar Frontend
- [ ] Navegador abre automaticamente em `http://localhost:5173`
- [ ] Dashboard carrega sem erros
- [ ] Sidebar aparece à esquerda
- [ ] Consegue navegar entre páginas

### 6.4. Testar Bot (Se Configurado)
- [ ] Abrir Telegram
- [ ] Procurar @seu_bot_username
- [ ] Enviar `/start`
- [ ] Receber mensagem de boas-vindas
- [ ] Enviar `/menu`
- [ ] Botões inline aparecem

---

## 7. 📊 PRIMEIRA SINCRONIZAÇÃO

### 7.1. Via Interface Web
- [ ] Ir para página "Calendário"
- [ ] Clicar no botão "🔄 Sincronizar"
- [ ] Aguardar mensagem de sucesso
- [ ] Verificar que reservas aparecem no calendário

### 7.2. Via Bot Telegram (Se Configurado)
- [ ] Enviar `/sync` para o bot
- [ ] Aguardar mensagem de conclusão
- [ ] Verificar contadores (novas, atualizadas, conflitos)

### 7.3. Verificar Dados
- [ ] Dashboard mostra estatísticas atualizadas
- [ ] Calendário mostra eventos coloridos
- [ ] Conflitos mostra alertas (se houver)
- [ ] Estatísticas mostra gráficos

---

## 8. ✅ VERIFICAÇÕES DE SAÚDE

### 8.1. Verificar Logs
- [ ] Abrir `data/logs/` (se existe)
- [ ] Verificar últimos logs
- [ ] Não deve ter erros críticos

**Comandos úteis:**
```bash
# Ver últimas linhas do log
type data\logs\sentinel_*.log | more

# Buscar erros
findstr /i "error" data\logs\sentinel_*.log
```

### 8.2. Verificar Banco de Dados
- [ ] `data/sentinel.db` existe
- [ ] Tamanho > 0 bytes
- [ ] Backup em `data/backups/` (se criado)

### 8.3. Verificar API
- [ ] `http://localhost:8000/health` retorna `{"status": "healthy"}`
- [ ] `http://localhost:8000/api/bookings` retorna lista (pode estar vazia)
- [ ] `http://localhost:8000/api/conflicts/summary?property_id=1` retorna dados

---

## 9. 🎯 TESTES FUNCIONAIS

### 9.1. Dashboard
- [ ] Cards de estatísticas aparecem
- [ ] Números fazem sentido
- [ ] Seção de "Hoje" aparece (se houver check-ins/outs)
- [ ] Próximas reservas listadas
- [ ] Alertas de conflitos (se houver)

### 9.2. Calendário
- [ ] Mês atual aparece
- [ ] Eventos aparecem nos dias corretos
- [ ] Cores por plataforma (Airbnb vermelho, Booking azul)
- [ ] Clicar em evento abre modal
- [ ] Modal mostra detalhes corretos
- [ ] Navegação entre meses funciona
- [ ] Botão "Hoje" volta para mês atual

### 9.3. Conflitos
- [ ] Lista de conflitos aparece (se houver)
- [ ] Cards mostram ambas reservas
- [ ] Severidade colorida corretamente
- [ ] Botão "Resolver" funciona
- [ ] Modal de resolução abre
- [ ] Pode adicionar notas
- [ ] Conflito desaparece após resolver

### 9.4. Estatísticas
- [ ] 4 cards de resumo aparecem
- [ ] Gráfico de ocupação carrega
- [ ] Gráfico de receita carrega
- [ ] Gráfico de plataformas carrega
- [ ] Gráfico de noites carrega
- [ ] Seletor de período funciona
- [ ] Tooltips aparecem ao passar mouse

### 9.5. Configurações
- [ ] Aba "Fácil" mostra dados do apartamento
- [ ] Aba "Avançada" mostra configurações técnicas
- [ ] Botão "Salvar" funciona (placeholder)
- [ ] Botão "Restaurar" funciona (placeholder)

---

## 10. 🔧 CONFIGURAÇÕES FINAIS

### 10.1. Ajustar Sincronização
- [ ] Verificar `CALENDAR_SYNC_INTERVAL_MINUTES` no .env
- [ ] Padrão: 30 minutos
- [ ] Ajustar se necessário (min: 5, max: 1440)

### 10.2. Configurar Notificações
- [ ] `ENABLE_CONFLICT_NOTIFICATIONS` = true (padrão)
- [ ] Se quiser desativar: false

### 10.3. Timezone
- [ ] Verificar que `TIMEZONE` = "America/Sao_Paulo"
- [ ] Datas aparecem corretas no sistema

---

## 11. 📖 DOCUMENTAÇÃO CONSULTADA

- [ ] Ler `LEIA-ME_PRIMEIRO.txt` (guia visual)
- [ ] Ler `COMO_INICIAR.md` (guia detalhado)
- [ ] Ler `INICIAR_AGORA.txt` (guia rápido)
- [ ] Ler `CONFIGURAR_BOT_TELEGRAM.txt` (se usar bot)
- [ ] Consultar `docs/DASHBOARD_E_ESTATISTICAS.md` (detalhes)
- [ ] Consultar `docs/TELEGRAM_BOT.md` (se usar bot)

---

## 12. 🎉 SISTEMA PRONTO PARA USO!

### Tarefas Pós-Configuração

- [ ] Adicionar `INICIAR_SISTEMA.bat` aos favoritos
- [ ] Criar atalho na área de trabalho (opcional)
- [ ] Configurar inicialização automática (opcional)
- [ ] Documentar credenciais em local seguro
- [ ] Criar rotina de backup do banco de dados

### Uso Diário

1. **Iniciar:** Executar `INICIAR_SISTEMA.bat`
2. **Acessar:** Abrir `http://localhost:5173`
3. **Verificar:** Dashboard, Conflitos, Atividades de Hoje
4. **Telegram:** Receber notificações (se configurado)
5. **Encerrar:** Fechar as janelas do terminal quando terminar

### Manutenção Semanal

- [ ] Verificar logs em `data/logs/`
- [ ] Fazer backup do `data/sentinel.db`
- [ ] Verificar espaço em disco
- [ ] Atualizar dependências (se necessário)

---

## 13. 🆘 TROUBLESHOOTING

### Problema: Backend não inicia
**Sintomas:** Erro ao executar `INICIAR_SISTEMA.bat`
**Soluções:**
1. Verificar que Python está instalado: `python --version`
2. Verificar dependências: `pip install -r requirements.txt`
3. Verificar .env existe e está configurado
4. Ver logs de erro no terminal

### Problema: Frontend não carrega
**Sintomas:** Página em branco ou erro 404
**Soluções:**
1. Verificar que Node.js está instalado: `node --version`
2. Instalar dependências: `cd frontend && npm install`
3. Instalar recharts: `npm install recharts`
4. Verificar porta 5173 não está em uso

### Problema: Bot não responde
**Sintomas:** Telegram não recebe mensagens
**Soluções:**
1. Verificar `TELEGRAM_BOT_TOKEN` no .env
2. Verificar `TELEGRAM_ADMIN_USER_IDS` no .env
3. Verificar que iniciou conversa com /start
4. Ver logs do backend para erros

### Problema: Nenhuma reserva aparece
**Sintomas:** Calendário vazio após sincronização
**Soluções:**
1. Verificar URLs do iCal estão corretas no .env
2. Testar URLs em navegador (devem baixar arquivo .ics)
3. Verificar logs para erros de conexão
4. Tentar sincronizar manualmente: `/sync` ou botão

### Problema: Gráficos não aparecem
**Sintomas:** Página de Estatísticas sem gráficos
**Soluções:**
1. Instalar recharts: `cd frontend && npm install recharts`
2. Ou usar: `frontend\instalar_recharts.bat`
3. Reiniciar frontend
4. Limpar cache do navegador (Ctrl+Shift+Delete)

---

## 14. 📞 SUPORTE

### Documentação
- `docs/` - Documentação completa
- `docs/ANALISE_E_DEBUG_COMPLETO.md` - Debug detalhado
- `docs/RESUMO_FINAL_MVP1.md` - Resumo do projeto

### Logs
- `data/logs/` - Logs do sistema
- Console do navegador (F12) - Erros do frontend

### Comandos de Debug
```bash
# Testar conexão DB
python -c "from app.database import engine; engine.connect()"

# Testar importação
python -c "from app.models import Booking; print('OK')"

# Ver status do sistema
curl http://localhost:8000/health
```

---

## ✅ CHECKLIST FINAL

**Antes de marcar como PRONTO, verificar:**

- [ ] ✅ Todos os pré-requisitos instalados
- [ ] ✅ Projeto limpo (sem `app/interfaces/`)
- [ ] ✅ `.env` configurado com dados reais
- [ ] ✅ URLs do iCal válidas e testadas
- [ ] ✅ Dependências instaladas (backend + frontend)
- [ ] ✅ Banco de dados inicializado
- [ ] ✅ Backend inicia sem erros
- [ ] ✅ Frontend carrega corretamente
- [ ] ✅ Bot Telegram funciona (se configurado)
- [ ] ✅ Primeira sincronização bem-sucedida
- [ ] ✅ Dados aparecem no dashboard
- [ ] ✅ Todos os testes funcionais passaram
- [ ] ✅ Documentação lida e compreendida

---

**🎉 SISTEMA PRONTO PARA PRODUÇÃO!**

**Próximo passo:** Usar o sistema diariamente e reportar quaisquer problemas.

**Data de Conclusão:** ___/___/______
**Configurado por:** _________________
