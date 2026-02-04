"""
Router para notificações do sistema.
GET /api/v1/notifications - Lista paginada com filtros
GET /api/v1/notifications/summary - Resumo para cards bento
PUT /api/v1/notifications/{id}/read - Marcar como lida
PUT /api/v1/notifications/read-all - Marcar todas como lidas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.middleware.auth import get_current_active_user
from app.services.notification_db_service import NotificationDBService
from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    NotificationSummaryResponse,
)

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


@router.get("/summary", response_model=NotificationSummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Resumo de notificações para os cards bento. Requer autenticação."""
    service = NotificationDBService(db)
    return NotificationSummaryResponse(**service.get_summary())


@router.get("/", response_model=NotificationListResponse)
def get_notifications(
    limit: int = Query(20, ge=1, le=100, description="Itens por página"),
    page: int = Query(1, ge=1, description="Número da página"),
    type: str = Query(None, description="Filtrar por tipo (ex: new_booking,conflict)"),
    unread_only: bool = Query(False, description="Apenas não lidas"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Lista notificações com filtros e paginação"""
    service = NotificationDBService(db)
    offset = (page - 1) * limit

    result = service.get_list(
        limit=limit,
        offset=offset,
        type_filter=type,
        unread_only=unread_only,
    )

    return NotificationListResponse(
        items=[NotificationResponse.model_validate(n) for n in result["items"]],
        total=result["total"],
        unread_count=result["unread_count"],
        page=page,
        limit=limit,
    )


@router.put("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Marca todas as notificações como lidas"""
    service = NotificationDBService(db)
    count = service.mark_all_as_read()
    return {
        "success": True,
        "message": f"{count} notificação(ões) marcada(s) como lida(s)",
        "count": count,
    }


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Marca uma notificação como lida"""
    service = NotificationDBService(db)
    notification = service.mark_as_read(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")

    return NotificationResponse.model_validate(notification)
