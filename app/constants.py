"""
Constantes da aplicação Sentinel.
Centraliza valores fixos usados em múltiplos módulos.
"""

# === PLATAFORMAS DE RESERVA ===
PLATFORM_AIRBNB = "airbnb"
PLATFORM_BOOKING = "booking"
PLATFORM_MANUAL = "manual"

# === STATUS DE RESERVA ===
STATUS_CONFIRMED = "confirmed"
STATUS_CANCELLED = "cancelled"
STATUS_COMPLETED = "completed"
STATUS_BLOCKED = "blocked"

# === TIPOS DE CONFLITO ===
CONFLICT_OVERLAP = "overlap"
CONFLICT_DUPLICATE = "duplicate"

# === SINCRONIZAÇÃO ===
DEFAULT_SYNC_INTERVAL_MINUTES = 30
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30

# === iCAL PARSING ===
# Campos comuns em eventos iCal do Airbnb
AIRBNB_ICAL_FIELDS = {
    "summary": "SUMMARY",
    "description": "DESCRIPTION",
    "dtstart": "DTSTART",
    "dtend": "DTEND",
    "uid": "UID",
    "status": "STATUS",
}

# Campos comuns em eventos iCal do Booking.com
BOOKING_ICAL_FIELDS = {
    "summary": "SUMMARY",
    "description": "DESCRIPTION",
    "dtstart": "DTSTART",
    "dtend": "DTEND",
    "uid": "UID",
    "status": "STATUS",
}

# === REGEX PATTERNS ===
# Airbnb geralmente usa formato: "Reserved - [Nome do Hóspede]"
AIRBNB_GUEST_PATTERN = r"(?:Reserved|Reservation)\s*[-:]\s*(.+?)(?:\s*\(|$)"

# Booking pode ter formatos variados
BOOKING_GUEST_PATTERN = r"^([^(]+?)(?:\s*\(|$)"

# === MENSAGENS ===
# Mensagens em português para o usuário final
MSG_SYNC_SUCCESS = "✅ Sincronização concluída com sucesso"
MSG_SYNC_ERROR = "❌ Erro na sincronização"
MSG_CONFLICT_DETECTED = "⚠️ Conflito detectado entre reservas"
MSG_NO_CONFLICTS = "✅ Nenhum conflito detectado"
MSG_BOOKING_ADDED = "🆕 Nova reserva adicionada"
MSG_BOOKING_UPDATED = "🔄 Reserva atualizada"
MSG_BOOKING_CANCELLED = "🚫 Reserva cancelada"

# === EMOJIS PARA UI ===
EMOJI_AIRBNB = "🏠"
EMOJI_BOOKING = "🏨"
EMOJI_CALENDAR = "📅"
EMOJI_GUEST = "👤"
EMOJI_WARNING = "⚠️"
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_INFO = "ℹ️"
EMOJI_SYNC = "🔄"
EMOJI_CONFLICT = "⚠️"
EMOJI_NEW = "🆕"

# === CONFIGURAÇÕES DE DISPLAY ===
# Para formatação de datas em português do Brasil (PT-BR)
DATE_FORMAT_SHORT = "%d/%m/%Y"
DATE_FORMAT_LONG = "%d de %B de %Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M"
TIME_FORMAT = "%H:%M"
CURRENCY_DEFAULT = "BRL"  # Real brasileiro

# === TIMEZONE ===
DEFAULT_TIMEZONE = "America/Sao_Paulo"

# === VALIDAÇÃO ===
MAX_GUEST_NAME_LENGTH = 200
MAX_NIGHTS_PER_BOOKING = 365
MIN_NIGHTS_PER_BOOKING = 1
