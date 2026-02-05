# app/schemas/email.py
"""
Schemas Pydantic para envio e gerenciamento de emails.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class SendEmailRequest(BaseModel):
    """Request para envio de email personalizado"""
    to: List[EmailStr] = Field(..., description="Lista de destinatários")
    subject: str = Field(..., min_length=1, max_length=500, description="Assunto do email")
    body: str = Field(..., min_length=1, description="Corpo do email (texto ou HTML)")
    html: bool = Field(default=False, description="Se True, corpo é HTML")
    cc: Optional[List[EmailStr]] = Field(None, description="Lista de destinatários em cópia")
    bcc: Optional[List[EmailStr]] = Field(None, description="Lista de destinatários em cópia oculta")
    attachments: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Lista de anexos (cada item: {filename, content, content_type})"
    )


class SendTemplateEmailRequest(BaseModel):
    """Request para envio de email usando template"""
    to: List[EmailStr] = Field(..., description="Lista de destinatários")
    subject: str = Field(..., min_length=1, max_length=500, description="Assunto do email")
    template_name: str = Field(..., description="Nome do template (ex: booking_confirmation.html)")
    context: Dict[str, Any] = Field(..., description="Variáveis do template")
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    attachments: Optional[List[Dict[str, Any]]] = None


class SendBookingConfirmationRequest(BaseModel):
    """Request simplificado para enviar confirmação de reserva"""
    booking_id: int = Field(..., description="ID da reserva")
    send_in_background: bool = Field(
        default=True,
        description="Se True, envia em background"
    )


class SendCheckinReminderRequest(BaseModel):
    """Request simplificado para enviar lembrete de check-in"""
    booking_id: int = Field(..., description="ID da reserva")
    send_in_background: bool = Field(
        default=True,
        description="Se True, envia em background"
    )


class FetchEmailsRequest(BaseModel):
    """Request para buscar emails via IMAP"""
    folder: str = Field(default="INBOX", description="Pasta do email (INBOX, SENT, etc)")
    limit: int = Field(default=10, ge=1, le=100, description="Número máximo de emails")
    unread_only: bool = Field(default=False, description="Apenas emails não lidos")


class EmailResponse(BaseModel):
    """Response genérico para operações de email"""
    success: bool
    message: str
    message_id: Optional[str] = None


class EmailItem(BaseModel):
    """Item de email retornado pela busca IMAP"""
    uid: str = Field(..., description="UID único do email")
    from_addr: str = Field(..., description="Remetente")
    to_addr: List[str] = Field(..., description="Destinatários")
    subject: str = Field(..., description="Assunto")
    date: str = Field(..., description="Data do email")
    body: str = Field(..., description="Corpo do email")
    is_read: bool = Field(..., description="Se foi lido")

    class Config:
        from_attributes = True


class EmailListResponse(BaseModel):
    """Response para listagem de emails"""
    success: bool
    total: int
    emails: List[EmailItem]
