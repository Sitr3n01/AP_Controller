"""
Schemas Pydantic para notificações do sistema.
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    """Resposta de uma notificação"""
    id: int
    type: str
    title: str
    message: str
    booking_id: Optional[int] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Resposta paginada de notificações"""
    items: List[NotificationResponse]
    total: int
    unread_count: int
    page: int = 1
    limit: int = 20


class NotificationSummaryResponse(BaseModel):
    """Resumo de notificações para os cards bento"""
    total: int = 0
    unread: int = 0
    today: int = 0
    by_type: Dict[str, int] = Field(default_factory=dict)
