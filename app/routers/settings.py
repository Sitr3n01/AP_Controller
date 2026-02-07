"""
Router para configurações do sistema.
GET /api/v1/settings - Retorna todas as configurações (merge .env + DB)
PUT /api/v1/settings - Salva configurações editáveis no banco de dados
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.settings_service import SettingsService
from app.schemas.settings import SettingsUpdate, SettingsResponse

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])


@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)):
    """Retorna todas as configurações (merge .env + DB)"""
    service = SettingsService(db)
    data = service.get_all_settings()
    return SettingsResponse(**data)


@router.put("/")
def update_settings(
    data: SettingsUpdate,
    db: Session = Depends(get_db),
):
    """Salva configurações editáveis no banco de dados"""
    service = SettingsService(db)

    # Filtrar apenas campos não-None
    update_data = data.model_dump(exclude_none=True)
    saved = service.update_settings(update_data)

    return {
        "success": True,
        "message": "Configurações salvas com sucesso",
        "saved": saved,
    }
