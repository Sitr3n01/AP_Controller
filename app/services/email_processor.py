# app/services/email_processor.py
"""
Processador de emails para automação de reservas.
Lê emails, parseia conteúdo e cria ações no sistema.
"""
import asyncio
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.booking import Booking, BookingStatus
from app.models.sync_action import SyncAction, ActionType, ActionStatus, TargetPlatform
from app.models.property import Property
from app.services.email_service import EmailService, get_email_service
from app.services.platform_parser_service import PlatformParserService
from app.services.booking_service import BookingService
from app.services.notification_service import NotificationService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmailProcessor:
    """Processador de emails para automação"""

    def __init__(self, db: Session):
        self.db = db
        self.parser_service = PlatformParserService()
        self.booking_service = BookingService(db)
        self.notification_service = NotificationService(db)
        # EmailService deve ser instanciado com credenciais. 
        # Aqui assumimos que o get_email_service pega do .env
        self.email_service = get_email_service() 

    async def process_unread_emails(self, limit: int = 10):
        """
        Busca emails não lidos e processa novas reservas.
        """
        if not self.email_service:
            logger.warning("EmailService not configured. Skipping email processing.")
            return

        logger.info("Checking for new reservation emails...")
        
        # Buscar emails não lidos
        result = await self.email_service.fetch_emails(unread_only=True, limit=limit)
        
        if not result["success"]:
            logger.error(f"Failed to fetch emails: {result['message']}")
            return

        emails = result["emails"]
        logger.info(f"Found {len(emails)} unread emails.")

        for email_data in emails:
            # Parsear email
            # TODO: O fetch_emails atual retorna 'raw', precisamos extrair subject e body
            # Por enquanto, assumindo que fetch_emails será melhorado ou que o parser lida com raw
            # O PlatformParser espera (subject, body). 
            # Vou precisar melhorar o fetch_emails ou usar um parser de email raw aqui.
            
            # SIMULAÇÃO: Extração básica do raw (ideal seria usar email.message_from_string)
            import email
            from email.policy import default
            
            raw_content = email_data.get("raw", "")
            msg = email.message_from_string(raw_content, policy=default)
            
            subject = msg["subject"] or ""
            
            # Extrair corpo (texto/plain ou html)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_content()
                        except:
                            pass
            else:
                body = msg.get_content()

            # Tentar parsear
            booking_data = self.parser_service.parse_email(subject, body)
            
            if booking_data:
                await self._handle_booking_data(booking_data)

    async def _handle_booking_data(self, data: dict):
        """Processa dados de uma reserva extraída"""
        logger.info(f"Processing booking data: {data}")
        
        external_id = data.get("external_id")
        platform = data.get("platform")
        
        # Identificar imóvel (Isso é tricky se tivermos vários)
        # Por simplificação, vamos assumir o primeiro imóvel do banco ou tentar inferir do email se possível
        # Idealmente, o email diria "Apartamento X". O parser poderia extrair isso.
        # Por enquanto, vamos pegar o primeiro imóvel.
        property_obj = self.db.query(Property).first()
        if not property_obj:
            logger.error("No properties found in DB to associate booking.")
            return

        # Verificar se reserva já existe
        existing_booking = self.booking_service.get_booking_by_external_id(
            external_id, platform, property_obj.id
        )

        if existing_booking:
            logger.info(f"Booking {external_id} already exists. Skipping.")
            return

        # Criar nova reserva (com null-safety)
        check_in_raw = data.get("check_in_date")
        check_out_raw = data.get("check_out_date")

        if not check_in_raw or not check_out_raw:
            logger.error("Missing check_in_date or check_out_date in parsed booking data")
            return

        check_in_date = check_in_raw.date() if hasattr(check_in_raw, 'date') else check_in_raw
        check_out_date = check_out_raw.date() if hasattr(check_out_raw, 'date') else check_out_raw

        new_booking_data = {
            "property_id": property_obj.id,
            "external_id": external_id,
            "platform": platform,
            "guest_name": data.get("guest_name", "Hóspede"),
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guest_count": data.get("guest_count", 1),
            "total_price": data.get("total_price"),
            "currency": data.get("currency", "BRL"),
            "status": BookingStatus.CONFIRMED,
            "nights_count": (check_out_date - check_in_date).days
        }

        try:
            booking = self.booking_service.create_booking(new_booking_data)
            
            # Criar Ação de Aprovação para Documento
            self._create_approval_action(booking)
            
            # Notificar Proprietário
            await self._notify_owner(booking)
            
        except Exception as e:
            logger.error(f"Error creating booking from email: {e}")

    def _create_approval_action(self, booking: Booking):
        """Cria uma SyncAction para aprovar a reserva e gerar documento"""
        action = SyncAction(
            property_id=booking.property_id,
            trigger_booking_id=booking.id,
            action_type=ActionType.APPROVE_BOOKING,
            target_platform=TargetPlatform.BOTH, # Interno
            status=ActionStatus.PENDING,
            priority="high",
            reason=f"Nova reserva de {booking.guest_name} via {booking.platform}. Aprovar para gerar autorização.",
            start_date=booking.check_in_date,
            end_date=booking.check_out_date
        )
        self.db.add(action)
        self.db.commit()
        logger.info(f"Created approval action for booking {booking.id}")

    async def _notify_owner(self, booking: Booking):
        """Envia notificação para o proprietário"""
        message = (
            f"🔔 *Nova Reserva Detectada via Email*\n\n"
            f"👤 {booking.guest_name}\n"
            f"🏠 {booking.platform.upper()}\n"
            f"📅 {booking.check_in_date.strftime('%d/%m')} a {booking.check_out_date.strftime('%d/%m')}\n\n"
            f"Acesse o painel para aprovar e gerar o documento."
        )
        
        # Enviar via Telegram (se configurado no NotificationService)
        # O notification_service geralmente tem métodos para isso
        # self.notification_service.notify_all(...) 
        # Vou usar o logger por enquanto pois notify_new_booking já existe
        
        self.notification_service.notify_new_booking(booking)

