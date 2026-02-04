"""
Configuração centralizada da aplicação usando Pydantic Settings.
Carrega variáveis do arquivo .env e valida tipos.
"""
from pathlib import Path
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação Sentinel"""

    # === APLICAÇÃO ===
    APP_NAME: str = "Sentinel"
    APP_ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    TIMEZONE: str = "America/Sao_Paulo"

    # === BANCO DE DADOS ===
    DATABASE_URL: str = "sqlite:///./data/sentinel.db"

    # === TELEGRAM BOT (MVP1 - Opcional) ===
    TELEGRAM_BOT_TOKEN: str = Field(default="", description="Token do bot Telegram do BotFather")
    TELEGRAM_ADMIN_USER_IDS: str = Field(default="", description="IDs de usuários admin separados por vírgula")

    # === CALENDÁRIOS ===
    AIRBNB_ICAL_URL: str = Field(default="https://www.airbnb.com/calendar/ical/XXXXXXX.ics", description="URL do feed iCal do Airbnb")
    BOOKING_ICAL_URL: str = Field(default="https://admin.booking.com/hotel/hoteladmin/ical/XXXXXXX.ics", description="URL do feed iCal do Booking")
    CALENDAR_SYNC_INTERVAL_MINUTES: int = 30

    # === GMAIL API (MVP3) ===
    GMAIL_CREDENTIALS_FILE: str = "./credentials.json"
    GMAIL_TOKEN_FILE: str = "./token.json"
    GMAIL_CHECK_INTERVAL_MINUTES: int = 5
    ENABLE_EMAIL_MONITORING: bool = False

    # === OLLAMA/GEMMA 3 (MVP3) ===
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma3:4b"
    OLLAMA_TIMEOUT_SECONDS: int = 30
    OLLAMA_TEMPERATURE: float = 0.1

    # === DOCUMENTOS ===
    TEMPLATE_DIR: str = "./templates"
    OUTPUT_DIR: str = "./data/generated_docs"
    DEFAULT_TEMPLATE: str = "autorizacao_condominio.docx"

    # === DADOS DO IMÓVEL ===
    PROPERTY_NAME: str = "Apartamento 2 Quartos - Goiânia"
    PROPERTY_ADDRESS: str = "Rua Exemplo, 123, Setor Central, 74000-000 Goiânia - GO"
    CONDO_NAME: str = "Condomínio Exemplo"
    CONDO_ADMIN_NAME: str = "Administração do Condomínio"

    # === FEATURES ===
    ENABLE_AUTO_DOCUMENT_GENERATION: bool = False
    ENABLE_CONFLICT_NOTIFICATIONS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignora variáveis extras no .env
    )

    @field_validator("TELEGRAM_ADMIN_USER_IDS")
    @classmethod
    def parse_admin_ids(cls, v: str) -> List[int]:
        """Converte string de IDs separados por vírgula em lista de inteiros"""
        if not v or v.strip() == "":
            return []
        try:
            return [int(id.strip()) for id in v.split(",") if id.strip()]
        except ValueError:
            raise ValueError("TELEGRAM_ADMIN_USER_IDS deve conter números separados por vírgula")

    @property
    def admin_user_ids(self) -> List[int]:
        """Retorna lista de IDs de administradores"""
        return self.parse_admin_ids(self.TELEGRAM_ADMIN_USER_IDS)

    @property
    def database_path(self) -> Path:
        """Retorna o caminho absoluto do banco de dados"""
        # Remove o prefixo sqlite:///
        path_str = self.DATABASE_URL.replace("sqlite:///", "")
        return Path(path_str)

    @property
    def template_path(self) -> Path:
        """Retorna o caminho completo do template padrão"""
        return Path(self.TEMPLATE_DIR) / self.DEFAULT_TEMPLATE

    @property
    def output_path(self) -> Path:
        """Retorna o caminho do diretório de saída de documentos"""
        return Path(self.OUTPUT_DIR)

    def ensure_directories(self) -> None:
        """Cria diretórios necessários se não existirem"""
        directories = [
            Path("data"),
            Path("data/downloads"),
            Path("data/generated_docs"),
            Path("data/logs"),
            Path(self.TEMPLATE_DIR),
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Instância global de configuração
settings = Settings()

# Garante que os diretórios existam ao importar
settings.ensure_directories()
