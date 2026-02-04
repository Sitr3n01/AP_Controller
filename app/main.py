"""
Aplicação principal FastAPI - SENTINEL
Sistema de Gestão Automatizada de Apartamento
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.logger import setup_logger, get_logger
from app.routers import bookings, conflicts, statistics, sync_actions, calendar

# Configurar logging
setup_logger(log_level=settings.LOG_LEVEL, app_name=settings.APP_NAME)
logger = get_logger(__name__)


# Tarefas de background
async def sync_calendar_periodically():
    """Sincroniza calendários periodicamente"""
    from app.database.session import get_db_context
    from app.services.calendar_service import CalendarService
    from app.models.property import Property

    logger.info("Starting periodic calendar sync task...")

    while True:
        try:
            await asyncio.sleep(settings.CALENDAR_SYNC_INTERVAL_MINUTES * 60)

            with get_db_context() as db:
                property_obj = db.query(Property).first()

                if property_obj:
                    logger.info(f"Running scheduled sync for property {property_obj.id}")
                    calendar_service = CalendarService(db)
                    result = await calendar_service.sync_all_sources(property_obj.id)

                    if result["success"]:
                        logger.info(f"Scheduled sync completed successfully")
                    else:
                        logger.error(f"Scheduled sync failed")

        except Exception as e:
            logger.error(f"Error in periodic sync task: {e}")
            await asyncio.sleep(60)  # Espera 1 minuto em caso de erro


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    logger.info(f"Starting {settings.APP_NAME}...")

    # Garantir que diretórios existem
    settings.ensure_directories()

    # Iniciar bot do Telegram (se configurado)
    telegram_bot = None
    if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_BOT_TOKEN != "":
        try:
            from app.telegram import TelegramBot
            telegram_bot = TelegramBot()
            await telegram_bot.start()
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")

    # Iniciar task de sincronização periódica
    sync_task = asyncio.create_task(sync_calendar_periodically())

    logger.info(f"{settings.APP_NAME} started successfully!")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Sync interval: {settings.CALENDAR_SYNC_INTERVAL_MINUTES} minutes")

    yield

    # Cleanup ao encerrar
    logger.info("Shutting down...")

    # Parar bot do Telegram
    if telegram_bot:
        try:
            await telegram_bot.stop()
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")

    # Parar task de sincronização
    sync_task.cancel()
    try:
        await sync_task
    except asyncio.CancelledError:
        pass

    logger.info("Shutdown complete")


# Criar aplicação FastAPI
app = FastAPI(
    title="SENTINEL API",
    description="API para gerenciamento automatizado de apartamento no Airbnb e Booking.com",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev
        "http://localhost:5173",  # Vite dev
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(bookings.router)
app.include_router(conflicts.router)
app.include_router(statistics.router)
app.include_router(sync_actions.router)
app.include_router(calendar.router)


# Rotas básicas
@app.get("/")
def root():
    """Rota raiz"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        "environment": settings.APP_ENV
    }


@app.get("/health")
def health_check():
    """Health check para monitoramento"""
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time()
    }


@app.get("/api/info")
def api_info():
    """Informações da API"""
    return {
        "app_name": settings.APP_NAME,
        "property_name": settings.PROPERTY_NAME,
        "timezone": settings.TIMEZONE,
        "sync_interval_minutes": settings.CALENDAR_SYNC_INTERVAL_MINUTES,
        "features": {
            "calendar_sync": True,
            "conflict_detection": True,
            "document_generation": settings.ENABLE_AUTO_DOCUMENT_GENERATION,
            "conflict_notifications": settings.ENABLE_CONFLICT_NOTIFICATIONS
        }
    }


# Handler de erros global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(f"Unhandled exception: {exc}")
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.APP_ENV == "development" else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True if settings.APP_ENV == "development" else False,
        log_level=settings.LOG_LEVEL.lower()
    )
