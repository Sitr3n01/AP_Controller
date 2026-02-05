# Guia da API - SENTINEL

Documentacao completa da API REST do SENTINEL para desenvolvedores.

---

## Base URL

**Desenvolvimento**: `http://localhost:8000`
**Producao**: `https://seu-dominio.com`

**Prefixo da API**: `/api/v1`

---

## Autenticacao

A API usa autenticacao JWT (JSON Web Tokens).

### Login

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "username": "admin",
  "password": "Admin123!"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usar Token

Todas as requisicoes autenticadas precisam do header:

```
Authorization: Bearer <seu-token-aqui>
```

**Exemplo com curl**:
```bash
curl -H "Authorization: Bearer eyJhbGc..." http://localhost:8000/api/v1/bookings/
```

---

## Endpoints

### Health Check

**GET /health**

Verifica se a API esta funcionando.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-04T12:00:00"
}
```

---

## Autenticacao e Usuarios

### 1. Login
`POST /api/v1/auth/login`

### 2. Logout
`POST /api/v1/auth/logout`

Requer autenticacao.

### 3. Usuario Atual
`GET /api/v1/auth/me`

Retorna dados do usuario logado.

**Response**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_admin": true,
  "is_active": true
}
```

### 4. Registrar Usuario
`POST /api/v1/auth/register`

**Request**:
```json
{
  "username": "novousuario",
  "email": "usuario@example.com",
  "password": "SenhaForte123!"
}
```

---

## Imoveis (Properties)

### 1. Listar Imoveis
`GET /api/v1/properties/`

**Query Parameters**:
- `skip`: Offset (padrao: 0)
- `limit`: Limite de resultados (padrao: 100)

**Response**:
```json
[
  {
    "id": 1,
    "name": "Apartamento 2 Quartos",
    "address": "Rua X, 123",
    "description": "Apartamento completo",
    "capacity": 4,
    "bedrooms": 2,
    "bathrooms": 1,
    "price_per_night": 150.00,
    "is_active": true
  }
]
```

### 2. Criar Imovel
`POST /api/v1/properties/`

**Request**:
```json
{
  "name": "Apartamento 2 Quartos",
  "address": "Rua X, 123, Centro, Goiania - GO",
  "description": "Apartamento completo com 2 quartos",
  "capacity": 4,
  "bedrooms": 2,
  "bathrooms": 1,
  "price_per_night": 150.00,
  "airbnb_ical_url": "https://airbnb.com/calendar/ical/...",
  "booking_ical_url": "https://booking.com/calendar/ical/..."
}
```

### 3. Obter Imovel
`GET /api/v1/properties/{property_id}`

### 4. Atualizar Imovel
`PUT /api/v1/properties/{property_id}`

### 5. Deletar Imovel
`DELETE /api/v1/properties/{property_id}`

---

## Reservas (Bookings)

### 1. Listar Reservas
`GET /api/v1/bookings/`

**Query Parameters**:
- `property_id`: Filtrar por imovel
- `status`: confirmed, pending, cancelled
- `source`: airbnb, booking, direct, other

**Response**:
```json
[
  {
    "id": 1,
    "property_id": 1,
    "guest_id": 1,
    "check_in": "2026-03-01",
    "check_out": "2026-03-05",
    "num_guests": 2,
    "total_price": 600.00,
    "status": "confirmed",
    "source": "airbnb",
    "property": { ... },
    "guest": { ... }
  }
]
```

### 2. Criar Reserva
`POST /api/v1/bookings/`

**Request**:
```json
{
  "property_id": 1,
  "check_in": "2026-03-01",
  "check_out": "2026-03-05",
  "num_guests": 2,
  "total_price": 600.00,
  "status": "confirmed",
  "source": "airbnb",
  "guest": {
    "name": "Joao Silva",
    "email": "joao@example.com",
    "phone": "(62) 99999-9999",
    "cpf": "123.456.789-00"
  }
}
```

### 3. Obter Reserva
`GET /api/v1/bookings/{booking_id}`

### 4. Atualizar Reserva
`PUT /api/v1/bookings/{booking_id}`

### 5. Deletar Reserva
`DELETE /api/v1/bookings/{booking_id}`

---

## Sincronizacao de Calendarios

### 1. Sincronizar Todos
`POST /api/v1/calendar/sync-all`

Sincroniza todos os imoveis.

**Response**:
```json
{
  "message": "Sincronizacao iniciada",
  "properties_synced": 3,
  "bookings_imported": 12
}
```

### 2. Sincronizar Imovel Especifico
`POST /api/v1/calendar/sync/{property_id}`

### 3. Historico de Sincronizacao
`GET /api/v1/sync-actions/`

**Response**:
```json
[
  {
    "id": 1,
    "property_id": 1,
    "action_type": "sync",
    "status": "completed",
    "details": "12 reservas importadas",
    "created_at": "2026-02-04T12:00:00"
  }
]
```

---

## Conflitos

### 1. Listar Conflitos
`GET /api/v1/conflicts/`

**Query Parameters**:
- `property_id`: Filtrar por imovel
- `resolved`: true/false

**Response**:
```json
[
  {
    "id": 1,
    "property_id": 1,
    "booking1_id": 10,
    "booking2_id": 11,
    "conflict_start": "2026-03-03",
    "conflict_end": "2026-03-05",
    "severity": "high",
    "resolved": false,
    "booking1": { ... },
    "booking2": { ... }
  }
]
```

### 2. Marcar Conflito como Resolvido
`PUT /api/v1/conflicts/{conflict_id}/resolve`

---

## Estatisticas

### 1. Dashboard
`GET /api/v1/statistics/dashboard`

**Response**:
```json
{
  "total_properties": 3,
  "total_bookings": 45,
  "active_bookings": 2,
  "upcoming_bookings": 8,
  "total_guests": 38,
  "occupancy_rate": 75.5,
  "monthly_revenue": 12500.00,
  "conflicts_count": 0
}
```

### 2. Ocupacao
`GET /api/v1/statistics/occupancy`

**Query Parameters**:
- `start_date`: Data inicial (YYYY-MM-DD)
- `end_date`: Data final (YYYY-MM-DD)
- `property_id`: Filtrar por imovel (opcional)

**Response**:
```json
{
  "occupancy_rate": 75.5,
  "occupied_days": 23,
  "total_days": 30,
  "by_property": [
    {
      "property_id": 1,
      "property_name": "Apartamento 2 Quartos",
      "occupancy_rate": 80.0
    }
  ]
}
```

### 3. Receita
`GET /api/v1/statistics/revenue`

**Query Parameters**:
- `start_date`: Data inicial
- `end_date`: Data final
- `property_id`: Filtrar por imovel (opcional)

**Response**:
```json
{
  "total_revenue": 12500.00,
  "by_property": [
    {
      "property_id": 1,
      "property_name": "Apartamento 2 Quartos",
      "revenue": 7500.00
    }
  ],
  "by_source": [
    {
      "source": "airbnb",
      "revenue": 8000.00
    },
    {
      "source": "booking",
      "revenue": 4500.00
    }
  ]
}
```

---

## Documentos

### 1. Gerar Documento
`POST /api/v1/documents/generate`

**Request**:
```json
{
  "guest": {
    "name": "Joao Silva",
    "cpf": "123.456.789-00",
    "phone": "(62) 99999-9999",
    "email": "joao@example.com"
  },
  "property": {
    "name": "Apartamento 101",
    "address": "Rua X, 123",
    "condo_name": "Condominio ABC"
  },
  "booking": {
    "check_in": "2026-03-01",
    "check_out": "2026-03-05"
  },
  "save_to_file": true
}
```

**Response**:
```json
{
  "filename": "autorizacao_joao_silva_20260301.docx",
  "path": "/data/generated_docs/autorizacao_joao_silva_20260301.docx",
  "generated_at": "2026-02-04T12:00:00"
}
```

### 2. Gerar de Reserva Existente
`POST /api/v1/documents/generate-from-booking`

**Request**:
```json
{
  "booking_id": 10,
  "save_to_file": true
}
```

### 3. Download de Documento
`GET /api/v1/documents/download/{filename}`

Retorna o arquivo .docx para download.

### 4. Listar Documentos
`GET /api/v1/documents/list`

---

## Emails

### 1. Enviar Email
`POST /api/v1/emails/send`

**Request**:
```json
{
  "to": ["cliente@example.com"],
  "subject": "Confirmacao de Reserva",
  "body": "<h1>Sua reserva foi confirmada!</h1>",
  "html": true,
  "cc": [],
  "bcc": [],
  "attachments": []
}
```

### 2. Enviar Email de Template
`POST /api/v1/emails/send-template`

**Request**:
```json
{
  "to": ["cliente@example.com"],
  "template_name": "booking_confirmation",
  "template_data": {
    "guest_name": "Joao Silva",
    "check_in": "01/03/2026",
    "check_out": "05/03/2026"
  }
}
```

### 3. Confirma��ao de Reserva
`POST /api/v1/emails/send-booking-confirmation`

**Request**:
```json
{
  "booking_id": 10,
  "send_in_background": true
}
```

### 4. Lembrete de Check-in
`POST /api/v1/emails/send-checkin-reminder`

**Request**:
```json
{
  "booking_id": 10,
  "send_in_background": true
}
```

---

## Schemas de Dados

### Property Schema
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "description": "string",
  "capacity": 4,
  "bedrooms": 2,
  "bathrooms": 1,
  "price_per_night": 150.00,
  "is_active": true,
  "airbnb_ical_url": "string",
  "booking_ical_url": "string",
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}
```

### Booking Schema
```json
{
  "id": 1,
  "property_id": 1,
  "guest_id": 1,
  "check_in": "2026-03-01",
  "check_out": "2026-03-05",
  "num_guests": 2,
  "total_price": 600.00,
  "status": "confirmed",
  "source": "airbnb",
  "external_id": "HM12345",
  "notes": "string",
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}
```

### Guest Schema
```json
{
  "id": 1,
  "name": "Joao Silva",
  "email": "joao@example.com",
  "phone": "(62) 99999-9999",
  "cpf": "123.456.789-00",
  "created_at": "2026-01-01T00:00:00"
}
```

---

## Codigos de Status HTTP

- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Too Many Requests (Rate Limit)
- `500` - Internal Server Error

---

## Rate Limiting

**Autenticacao**:
- 5 requisicoes por minuto por IP

**Outros Endpoints**:
- 100 requisicoes por minuto por IP (configuravel)

Ao exceder o limite:
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

---

## Exemplos de Uso

### Python

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "admin",
        "password": "Admin123!"
    }
)
token = response.json()["access_token"]

# Headers com token
headers = {"Authorization": f"Bearer {token}"}

# Listar reservas
bookings = requests.get(
    "http://localhost:8000/api/v1/bookings/",
    headers=headers
).json()

print(bookings)
```

### JavaScript

```javascript
// Login
const response = await fetch("http://localhost:8000/api/v1/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "admin",
    password: "Admin123!"
  })
});
const { access_token } = await response.json();

// Listar reservas
const bookings = await fetch("http://localhost:8000/api/v1/bookings/", {
  headers: { "Authorization": `Bearer ${access_token}` }
}).then(res => res.json());

console.log(bookings);
```

### cURL

```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}' \
  | jq -r '.access_token')

# Listar reservas
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/bookings/"
```

---

## Documentacao Interativa

Acesse a documentacao Swagger UI em:
**http://localhost:8000/docs**

Permite:
- Visualizar todos os endpoints
- Testar requisicoes
- Ver schemas de dados
- Autenticar e fazer requisicoes autenticadas

---

## Suporte

- Documentacao Completa: [docs/README.md](../README.md)
- Issues: GitHub
- Email: api@sentinel.com

---

**Atualizado**: 2026-02-04
