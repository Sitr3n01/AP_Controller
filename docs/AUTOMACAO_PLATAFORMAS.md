# 🤖 Automação de Plataformas - Airbnb e Booking.com

## 📋 Visão Geral

Este documento explica as possibilidades e limitações de automação com as plataformas Airbnb e Booking.com, e como o sistema SENTINEL gerencia isso.

---

## 🏠 Airbnb

### ✅ O que FUNCIONA (iCal)

**Via iCal Feed (Atual - MVP1):**
- ✅ **Leitura de reservas confirmadas** - Detecta novas reservas automaticamente
- ✅ **Cancelamentos** - Detecta quando hóspede cancela
- ✅ **Bloqueios manuais** - Detecta períodos bloqueados
- ✅ **Atualizações de datas** - Detecta mudanças em reservas existentes

**Limitações do iCal:**
- ⏱️ **Delay de 30min-2h**: O calendário iCal não atualiza em tempo real
- 📧 **Dados limitados**: Não inclui preço, número de hóspedes, emails, telefones
- 🔒 **Somente leitura**: Não permite criar/cancelar/bloquear via iCal

### 🔒 O que NÃO FUNCIONA (Limitações da API oficial)

**Airbnb API Oficial:**
- ❌ **Não disponível publicamente** - API restrita apenas para parceiros grandes
- ❌ **Sem acesso para hosts individuais** - Não há como se cadastrar
- ❌ **Sem SDK oficial** - Não existe biblioteca Python oficial

**Por isso NÃO É POSSÍVEL fazer automaticamente:**
- ❌ Criar bloqueios no calendário Airbnb via código
- ❌ Cancelar reservas programaticamente
- ❌ Alterar preços automaticamente
- ❌ Enviar mensagens para hóspedes via API
- ❌ Aceitar/recusar reservas programaticamente

### 💡 Soluções Alternativas (Semi-Automação)

1. **Sincronização Bidirecional via iCal:**
   - Sentinel detecta reserva do Airbnb via iCal
   - **Bloqueia automaticamente** no Booking.com (próximo MVP)
   - Previne overbooking entre plataformas

2. **Notificações + Ação Manual:**
   - Sentinel detecta conflito
   - Envia alerta no Telegram
   - **Você bloqueia manualmente** no Airbnb (30 segundos)
   - Sentinel confirma que bloqueio foi efetivado

3. **Interface Web do Sentinel (Futuro):**
   - Dashboard mostra calendário consolidado
   - Botão "Bloquear em todas as plataformas"
   - Abre abas do Airbnb/Booking automaticamente
   - Você só confirma em cada uma

---

## 🏨 Booking.com

### ✅ O que FUNCIONA (iCal)

**Via iCal Feed (Atual - MVP1):**
- ✅ **Leitura de reservas confirmadas**
- ✅ **Cancelamentos**
- ✅ **Bloqueios manuais**
- ✅ **Atualizações de datas**

**Limitações do iCal (igual ao Airbnb):**
- ⏱️ Delay de 30min-2h
- 📧 Dados limitados
- 🔒 Somente leitura

### 🟡 Booking.com API (Possível, mas complexo)

**API XML Oficial:**
- ✅ **Existe API pública** - Disponível via Booking.com Connectivity
- ✅ **Permite automação completa** - Criar bloqueios, preços, disponibilidade
- ⚠️ **Processo burocrático** - Precisa se registrar como "Channel Manager"
- ⚠️ **Documentação complexa** - XML API, não é REST
- ⚠️ **Requer aprovação** - Booking precisa aprovar sua integração

**Se implementarmos a API do Booking (MVP4 - Futuro):**
- ✅ Bloquear datas automaticamente via código
- ✅ Atualizar preços programaticamente
- ✅ Modificar disponibilidade
- ✅ Consultar reservas em tempo real

**Por que não implementamos agora:**
- Processo de aprovação demora 2-4 semanas
- Complexidade alta para MVP1
- iCal resolve 90% dos casos

---

## 🎯 Estratégia do SENTINEL

### MVP1 (Atual): Prevenção de Overbooking
```
Airbnb iCal → Sentinel ← Booking iCal
                ↓
    Detecta conflito em 30min
                ↓
    Alerta no Telegram
                ↓
    Você bloqueia manualmente
```

### MVP2 (Próximo): Bloqueio Inteligente
```
Nova reserva Airbnb
    ↓ (detectada via iCal)
Sentinel analisa calendário
    ↓
Envia comando Telegram:
"🔒 Bloquear Booking de 10-15/03?"
    ↓ (você clica "Sim")
Sentinel gera link direto:
booking.com/calendar?block=10-15
    ↓ (abre no celular)
Você confirma em 2 cliques
```

### MVP3 (Futuro - com Gmail):
```
Email confirmação Airbnb
    ↓ (0-5 minutos)
IA extrai datas
    ↓
Alerta ANTES do iCal atualizar
    ↓
Bloqueia em tempo real
```

### MVP4 (Avançado - Booking API):
```
Nova reserva Airbnb
    ↓
Sentinel detecta (iCal)
    ↓
**BLOQUEIA AUTOMATICAMENTE**
no Booking.com via API
    ↓
Notifica: "✅ Bloqueado no Booking!"
```

---

## 🔄 Fluxo de Sincronização Atual (MVP1)

### Cenário 1: Nova Reserva no Airbnb

```
1. Hóspede reserva no Airbnb (10:00)
2. Airbnb atualiza iCal (10:15 - 11:30)
3. Sentinel sincroniza (10:30, 11:00, 11:30...)
4. Detecta nova reserva
5. Verifica conflitos com Booking
6. Se OK: ✅ "Nova reserva: João, 10-15/03"
7. Se CONFLITO: ⚠️ "ATENÇÃO: Overlapping com Booking!"
```

**Janela de risco:** 30min - 2h entre reserva e detecção

### Cenário 2: Nova Reserva no Booking (ao mesmo tempo)

```
1. Hóspede reserva no Booking (10:05)
2. Booking atualiza iCal (10:20 - 11:35)
3. Sentinel sincroniza e detecta
4. ⚠️ CONFLITO DETECTADO!
5. Alerta Telegram: "🚨 OVERBOOKING: Airbnb + Booking no mesmo período!"
6. Você cancela uma das duas (política do anfitrião)
```

**Por isso o sync a cada 30min é crítico!**

---

## 🛠️ Funcionalidades de Bloqueio do Sentinel

### Bloqueio Manual via Telegram
```
Você: /bloquear 10/03/2024 15/03/2024
Bot: ✅ Período bloqueado no Sentinel
Bot: ⚠️ LEMBRETE: Bloquear manualmente em:
     🏠 Airbnb: airbnb.com/hosting/calendar
     🏨 Booking: admin.booking.com/calendar
```

### Bloqueio Automático no Sentinel (Previne agendamento duplo interno)
- Quando detecta reserva A, marca período como ocupado
- Se outra fonte tentar criar reserva B no mesmo período, alerta

### Detecção de Conflito
```python
# Sentinel verifica automaticamente:
if reserva_airbnb.sobrepoe(reserva_booking):
    criar_alerta_conflito()
    notificar_telegram()
    marcar_como_critico()
```

---

## 📱 Interface Web - UX para seu Parente (Futuro)

### Dashboard Principal
```
┌─────────────────────────────────────────┐
│  📅 Calendário - Março 2024             │
├─────────────────────────────────────────┤
│  10-15: João Silva (Airbnb)      ✅     │
│  18-22: Maria Santos (Booking)   ✅     │
│  25-27: ⚠️ CONFLITO DETECTADO!          │
│         [Ver Detalhes] [Resolver]       │
└─────────────────────────────────────────┘

🔘 Bloquear período
🔘 Ver próximas reservas
🔘 Histórico de hóspedes
```

### Resolver Conflito (1 clique)
```
⚠️ Conflito em 25-27/03:
   🏠 Airbnb: Pedro (R$ 450)
   🏨 Booking: Ana (R$ 380)

Sugestão:
✅ Manter Airbnb (valor maior)
❌ Cancelar Booking

[📱 Abrir Booking para Cancelar]
   ↓
   Abre: admin.booking.com/reservations/123
```

---

## 🎓 Resumo para o Usuário

### ✅ O que o Sentinel FAZ automaticamente:
1. Lê reservas do Airbnb e Booking
2. Detecta conflitos em até 30 minutos
3. Alerta você no Telegram
4. Mantém histórico completo
5. Gera documentos do condomínio

### ⚠️ O que VOCÊ precisa fazer manualmente:
1. Bloquear nas plataformas quando alertado
2. Cancelar reservas duplicadas (escolher qual)
3. Responder mensagens de hóspedes

### 💰 ROI (Retorno do Investimento):
- **Sem Sentinel:** Risco de overbooking = multa + péssima avaliação + estresse
- **Com Sentinel:** Alertas em 30min + 5min para resolver = Tranquilidade

**Tempo economizado:** 2-3 horas/semana de verificação manual

---

## 🚀 Roadmap de Automação

| Fase | Automação | Esforço | Status |
|------|-----------|---------|--------|
| MVP1 | Detecção de conflitos via iCal | ⭐ Baixo | ✅ Atual |
| MVP2 | Links diretos para bloqueio | ⭐⭐ Médio | 📅 Próximo |
| MVP3 | Alertas em tempo real (Gmail) | ⭐⭐ Médio | 🔮 Futuro |
| MVP4 | Booking API (bloqueio automático) | ⭐⭐⭐ Alto | 🔮 Futuro |
| MVP5 | Scraping Airbnb (não recomendado) | ⭐⭐⭐⭐ Muito Alto | ❌ Arriscado |

---

## ⚖️ Considerações Legais

**É permitido:**
- ✅ Usar iCal feeds públicos fornecidos pelas plataformas
- ✅ Notificar sobre conflitos
- ✅ Armazenar dados das suas próprias reservas

**Não é permitido:**
- ❌ Fazer scraping/automação via Selenium no Airbnb (viola ToS)
- ❌ Usar credenciais de terceiros
- ❌ Burlar sistemas de segurança

---

## 📞 Suporte

**Dúvidas sobre automação:**
- Verifique os logs em `data/logs/`
- Teste sincronização manual: `python scripts/manual_sync.py`
- Consulte: docs/TROUBLESHOOTING.md

**Alternativas caso iCal falhe:**
- Email monitoring (MVP3) - backup via Gmail
- Checagem manual diária - Sentinel gera relatório
