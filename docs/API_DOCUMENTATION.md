# 📘 API Documentation - SENTINEL

## 🚀 Início Rápido

**Base URL:** `http://127.0.0.1:8000`

**Documentação Interativa:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

**Iniciar Servidor:**
```bash
scripts\start_server.bat
```

---

## 📋 Endpoints Principais

### 🏠 Informações Gerais

#### `GET /`
Rota raiz - Informações básicas da API

**Response:**
```json
{
  "name": "Sentinel",
  "version": "1.0.0",
  "status": "online",
  "environment": "production"
}
```

#### `GET /health`
Health check para monitoramento

#### `GET /api/info`
Informações detalhadas da API e configurações

---

## 📅 Bookings (Reservas)

### `GET /api/bookings/`
Lista todas as reservas com filtros

**Query Parameters:**
- `property_id` (required): ID do imóvel
- `platform` (optional): airbnb, booking ou manual
- `status` (optional): confirmed, cancelled, completed
- `page` (optional): Número da página (padrão: 1)
- `page_size` (optional): Itens por página (padrão: 50)

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "guest_name": "João Silva",
      "check_in_date": "2024-03-10",
      "check_out_date": "2024-03-15",
      "nights_count": 5,
      "platform": "airbnb",
      "status": "confirmed",
      "total_price": 950.00,
      "currency": "BRL"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 50
}
```

### `GET /api/bookings/current`
Retorna a reserva ativa no momento (hóspede atual)

**Query Parameters:**
- `property_id` (required)

### `GET /api/bookings/upcoming`
Retorna próximas N reservas futuras

**Query Parameters:**
- `property_id` (required)
- `limit` (optional): Número de reservas (padrão: 5, max: 20)

### `GET /api/bookings/{booking_id}`
Detalhes de uma reserva específica

### `POST /api/bookings/`
Cria uma nova reserva manual

**Request Body:**
```json
{
  "property_id": 1,
  "guest_name": "João Silva",
  "check_in_date": "2024-03-10",
  "check_out_date": "2024-03-15",
  "guest_count": 2,
  "platform": "manual",
  "guest_email": "joao@email.com",
  "guest_phone": "(62) 99999-9999"
}
```

### `PUT /api/bookings/{booking_id}`
Atualiza dados de uma reserva

### `DELETE /api/bookings/{booking_id}`
Cancela uma reserva (marca como cancelled)

### `GET /api/bookings/statistics/summary`
Estatísticas gerais das reservas

**Response:**
```json
{
  "total": 45,
  "confirmed": 15,
  "completed": 28,
  "cancelled": 2
}
```

---

## ⚠️ Conflicts (Conflitos)

### `GET /api/conflicts/`
Lista todos os conflitos

**Query Parameters:**
- `property_id` (required)
- `active_only` (optional): true/false (padrão: true)

**Response:**
```json
[
  {
    "id": 1,
    "booking_id_1": 10,
    "booking_id_2": 11,
    "conflict_type": "overlap",
    "overlap_start": "2024-03-18",
    "overlap_end": "2024-03-20",
    "overlap_nights": 2,
    "severity": "high",
    "resolved": false,
    "detected_at": "2024-03-01T10:30:00",
    "booking_1_guest": "Maria Santos",
    "booking_1_platform": "airbnb",
    "booking_1_dates": "2024-03-18 - 2024-03-22",
    "booking_2_guest": "Pedro Alves",
    "booking_2_platform": "booking",
    "booking_2_dates": "2024-03-18 - 2024-03-20"
  }
]
```

### `GET /api/conflicts/summary`
Resumo de conflitos

**Response:**
```json
{
  "total": 2,
  "critical": 1,
  "high": 1,
  "medium": 0,
  "low": 0,
  "duplicates": 0,
  "overlaps": 2
}
```

### `POST /api/conflicts/{conflict_id}/resolve`
Marca um conflito como resolvido

**Request Body:**
```json
{
  "resolution_notes": "Cancelei reserva do Booking, mantive Airbnb"
}
```

### `POST /api/conflicts/detect`
Força detecção manual de conflitos

---

## 📋 Sync Actions (Ações de Sincronização)

### `GET /api/sync-actions/`
Lista ações de sincronização

**Query Parameters:**
- `property_id` (required)
- `status` (optional): pending, completed, dismissed (padrão: pending)

**Response:**
```json
[
  {
    "id": 1,
    "action_type": "block_dates",
    "status": "pending",
    "target_platform": "booking",
    "priority": "high",
    "priority_emoji": "🔴",
    "description": "🔒 Bloquear 18/03 a 20/03/2024 no Booking.com",
    "reason": "🚨 CONFLITO DETECTADO!...",
    "action_url": "https://admin.booking.com/hotel/hoteladmin/availability.html",
    "start_date": "2024-03-18",
    "end_date": "2024-03-20",
    "created_at": "2024-03-01T10:35:00",
    "auto_dismiss_after_hours": 72
  }
]
```

### `GET /api/sync-actions/summary`
Resumo de ações

### `POST /api/sync-actions/{action_id}/complete`
Marca ação como completada

**Request Body:**
```json
{
  "notes": "Bloqueio realizado com sucesso"
}
```

### `POST /api/sync-actions/{action_id}/dismiss`
Descarta uma ação

### `POST /api/sync-actions/auto-dismiss`
Auto-descarta ações expiradas

---

## 📅 Calendar (Calendário)

### `GET /api/calendar/events`
Retorna eventos do calendário

**Query Parameters:**
- `property_id` (required)
- `start_date` (required): Data inicial (YYYY-MM-DD)
- `end_date` (required): Data final (YYYY-MM-DD)

**Response (compatível com FullCalendar):**
```json
[
  {
    "id": 1,
    "title": "João Silva (AIRBNB)",
    "start": "2024-03-10",
    "end": "2024-03-15",
    "platform": "airbnb",
    "status": "confirmed",
    "color": "#FF5A5F",
    "conflict": false
  }
]
```

### `POST /api/calendar/sync`
Força sincronização manual dos calendários

**Query Parameters:**
- `property_id` (required)

**Response:**
```json
{
  "success": true,
  "total_stats": {
    "added": 2,
    "updated": 1,
    "cancelled": 0,
    "unchanged": 12
  },
  "message": "Sincronização concluída"
}
```

### `GET /api/calendar/sync-status`
Status da última sincronização

**Response:**
```json
{
  "sources": [
    {
      "id": 1,
      "platform": "airbnb",
      "last_sync_at": "2024-03-01T10:00:00",
      "last_sync_status": "success",
      "sync_enabled": true,
      "last_log": {
        "status": "success",
        "bookings_added": 1,
        "bookings_updated": 2,
        "conflicts_detected": 0,
        "duration_ms": 1250
      }
    }
  ],
  "total_sources": 2,
  "all_synced_recently": true
}
```

---

## 📊 Statistics (Estatísticas)

### `GET /api/statistics/dashboard`
Dados completos do dashboard

**Query Parameters:**
- `property_id` (required)

**Response:**
```json
{
  "current_booking": {
    "id": 5,
    "guest_name": "Ana Costa",
    "check_out_date": "2024-03-12",
    "platform": "airbnb",
    "nights_remaining": 3
  },
  "upcoming_bookings": [
    {
      "id": 10,
      "guest_name": "João Silva",
      "check_in_date": "2024-03-15",
      "check_out_date": "2024-03-20",
      "nights_count": 5,
      "platform": "airbnb"
    }
  ],
  "booking_statistics": {
    "total": 45,
    "confirmed": 15,
    "completed": 28,
    "cancelled": 2
  },
  "conflict_summary": {
    "total": 2,
    "critical": 1,
    "high": 1
  },
  "action_summary": {
    "pending": 3,
    "critical": 1
  },
  "alerts": {
    "critical_conflicts": 1,
    "critical_actions": 1,
    "total_pending": 3
  }
}
```

### `GET /api/statistics/occupancy`
Estatísticas de ocupação

**Query Parameters:**
- `property_id` (required)
- `months` (optional): Número de meses (padrão: 6, max: 12)

**Response:**
```json
{
  "months": [
    {
      "month": "2024-03",
      "occupied_nights": 23,
      "total_nights": 30,
      "bookings_count": 5,
      "airbnb_nights": 15,
      "booking_nights": 8,
      "occupancy_rate": 76.7
    }
  ],
  "summary": {
    "average_occupancy": 72.5,
    "total_bookings": 28,
    "total_nights": 385
  }
}
```

### `GET /api/statistics/revenue`
Estatísticas de receita

**Response:**
```json
{
  "total_revenue": 7650.00,
  "average_price_per_booking": 510.00,
  "by_platform": {
    "airbnb": 4590.00,
    "booking": 3060.00
  },
  "bookings_with_price": 15,
  "currency": "BRL",
  "period": "últimos 6 meses"
}
```

---

## 🔄 Sincronização Automática

O servidor executa sincronização automática a cada **30 minutos** (configurável em `.env`).

**Processo:**
1. Download dos iCal feeds (Airbnb + Booking)
2. Parse dos eventos
3. Merge com banco de dados local
4. Detecção de conflitos
5. Criação de ações pendentes
6. Log da sincronização

---

## 🎨 Cores das Plataformas

- **Airbnb:** `#FF5A5F` (Rosa)
- **Booking:** `#003580` (Azul)
- **Manual:** `#6B7280` (Cinza)

---

## 🔒 CORS

CORS configurado para permitir acesso de:
- `http://localhost:3000` (React dev)
- `http://localhost:5173` (Vite dev)

---

## ⚡ Exemplos de Uso

### Buscar Dashboard
```bash
curl http://127.0.0.1:8000/api/statistics/dashboard?property_id=1
```

### Forçar Sincronização
```bash
curl -X POST http://127.0.0.1:8000/api/calendar/sync?property_id=1
```

### Listar Conflitos Ativos
```bash
curl http://127.0.0.1:8000/api/conflicts/?property_id=1
```

### Marcar Ação Como Completada
```bash
curl -X POST http://127.0.0.1:8000/api/sync-actions/1/complete \
  -H "Content-Type: application/json" \
  -d '{"notes": "Bloqueio realizado"}'
```

---

## 🐛 Tratamento de Erros

**Códigos de Status:**
- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

**Formato de Erro:**
```json
{
  "error": "Not Found",
  "message": "Reserva não encontrada"
}
```

---

## 📝 Notas de Desenvolvimento

- Todas as datas são em formato ISO 8601 (`YYYY-MM-DD`)
- Timestamps incluem timezone UTC
- Valores monetários em Decimal (2 casas decimais)
- Paginação padrão: 50 itens por página
- Logs detalhados em `data/logs/`

---

## 🚀 Próximos Endpoints (MVP2)

- `GET /api/guests/` - Listar hóspedes
- `GET /api/guests/{id}` - Detalhes do hóspede
- `POST /api/documents/generate` - Gerar documento
- `GET /api/documents/` - Listar documentos
- `GET /api/settings/` - Configurações do sistema
