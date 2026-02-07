"""
Schemas Pydantic para configurações do sistema.
"""
from typing import Optional
from pydantic import BaseModel, Field


class SettingsUpdate(BaseModel):
    """Campos editáveis pelo frontend"""
    condoEmail: Optional[str] = Field(None, description="Email do condomínio")
    syncIntervalMinutes: Optional[int] = Field(None, ge=5, le=1440, description="Intervalo de sync em minutos")
    enableAutoDocumentGeneration: Optional[bool] = Field(None, description="Geração automática de documentos")
    enableConflictNotifications: Optional[bool] = Field(None, description="Notificações de conflitos")


class SettingsResponse(BaseModel):
    """Resposta completa de settings (merge .env + DB)"""
    # Dados do imóvel (read-only, do .env)
    propertyName: str = ""
    propertyAddress: str = ""
    maxGuests: int = 6
    condoName: str = ""
    condoAdminName: str = ""

    # Dados do proprietário (read-only, do .env)
    ownerName: str = ""
    ownerEmail: str = ""
    ownerPhone: str = ""
    ownerApto: str = ""
    ownerBloco: str = ""
    ownerGaragem: str = ""

    # Editáveis (merge .env + DB)
    condoEmail: str = ""
    syncIntervalMinutes: int = 30
    enableAutoDocumentGeneration: bool = False
    enableConflictNotifications: bool = True

    # Informações extras (read-only)
    contactPhone: str = ""
    contactEmail: str = ""
    timezone: str = "America/Sao_Paulo"

    class Config:
        from_attributes = True
