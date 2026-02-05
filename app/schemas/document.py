# app/schemas/document.py
"""
Schemas Pydantic para geração de documentos.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class GuestDocumentData(BaseModel):
    """Dados do hóspede para geração de documento"""
    name: str = Field(..., min_length=3, max_length=200, description="Nome completo do hóspede")
    cpf: Optional[str] = Field(None, description="CPF ou documento do hóspede")
    phone: Optional[str] = Field(None, description="Telefone do hóspede")
    email: Optional[str] = Field(None, description="Email do hóspede")


class PropertyDocumentData(BaseModel):
    """Dados do imóvel para geração de documento"""
    name: str = Field(..., description="Nome/identificação do imóvel")
    address: str = Field(..., description="Endereço completo")
    condo_name: Optional[str] = Field(None, description="Nome do condomínio")
    owner_name: Optional[str] = Field(None, description="Nome do proprietário")


class BookingDocumentData(BaseModel):
    """Dados da reserva para geração de documento"""
    id: Optional[int] = Field(None, description="ID da reserva")
    check_in: date = Field(..., description="Data de check-in")
    check_out: date = Field(..., description="Data de check-out")

    @field_validator('check_out')
    @classmethod
    def validate_checkout_after_checkin(cls, v: date, info) -> date:
        """Valida que check-out é depois de check-in"""
        if 'check_in' in info.data and v <= info.data['check_in']:
            raise ValueError('Check-out deve ser após check-in')
        return v


class GenerateDocumentRequest(BaseModel):
    """Request para gerar documento de autorização"""
    guest: GuestDocumentData
    property: PropertyDocumentData
    booking: BookingDocumentData
    save_to_file: bool = Field(
        default=True,
        description="Se True, salva em arquivo. Se False, retorna bytes para download."
    )


class GenerateDocumentFromBookingRequest(BaseModel):
    """Request simplificado: gera documento a partir de booking_id existente"""
    booking_id: int = Field(..., description="ID da reserva existente")
    save_to_file: bool = Field(default=True)


class DocumentResponse(BaseModel):
    """Response após gerar documento"""
    success: bool
    message: str
    filename: Optional[str] = None
    file_path: Optional[str] = None  # Se save_to_file=True
    download_url: Optional[str] = None  # URL para download


class DocumentListItem(BaseModel):
    """Item da lista de documentos gerados"""
    filename: str
    path: str
    size_kb: float
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response para listagem de documentos"""
    total: int
    documents: list[DocumentListItem]
