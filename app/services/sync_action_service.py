"""
Serviço de gerenciamento de ações de sincronização.
Cria, gerencia e acompanha ações que o usuário precisa executar manualmente nas plataformas.
"""
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.sync_action import SyncAction, ActionType, ActionStatus, TargetPlatform
from app.models.booking import Booking
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SyncActionService:
    """Serviço para gerenciar ações de sincronização entre plataformas"""

    def __init__(self, db: Session):
        self.db = db

    def create_block_action(
        self,
        property_id: int,
        start_date: date,
        end_date: date,
        target_platform: TargetPlatform,
        reason: str,
        trigger_booking: Optional[Booking] = None,
        priority: str = "high"
    ) -> SyncAction:
        """
        Cria uma ação de bloqueio de datas.

        Args:
            property_id: ID do imóvel
            start_date: Data inicial do bloqueio
            end_date: Data final do bloqueio
            target_platform: Plataforma alvo (airbnb/booking/both)
            reason: Motivo do bloqueio
            trigger_booking: Reserva que originou a ação (opcional)
            priority: Prioridade (low/medium/high/critical)

        Returns:
            SyncAction criada
        """
        logger.info(f"Creating block action for {target_platform.value}: {start_date} to {end_date}")

        # Gerar URL de ação (se possível)
        action_url = self._generate_block_url(target_platform, start_date, end_date)

        action = SyncAction(
            property_id=property_id,
            trigger_booking_id=trigger_booking.id if trigger_booking else None,
            action_type=ActionType.BLOCK_DATES,
            status=ActionStatus.PENDING,
            target_platform=target_platform,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            action_url=action_url,
            priority=priority,
            auto_dismiss_after_hours=72  # Ações de bloqueio expiram em 3 dias
        )

        self.db.add(action)
        self.db.commit()
        self.db.refresh(action)

        logger.info(f"✅ Block action created: ID={action.id}")
        return action

    def create_cancel_action(
        self,
        property_id: int,
        booking: Booking,
        reason: str,
        priority: str = "critical"
    ) -> SyncAction:
        """
        Cria uma ação de cancelamento de reserva.

        Args:
            property_id: ID do imóvel
            booking: Reserva a ser cancelada
            reason: Motivo do cancelamento
            priority: Prioridade (padrão: critical)

        Returns:
            SyncAction criada
        """
        logger.info(f"Creating cancel action for booking {booking.id}")

        # Determinar plataforma
        target_platform = TargetPlatform.AIRBNB if booking.platform == "airbnb" else TargetPlatform.BOOKING

        # URL de ação
        action_url = self._generate_cancel_url(booking)

        action = SyncAction(
            property_id=property_id,
            trigger_booking_id=booking.id,
            action_type=ActionType.CANCEL_BOOKING,
            status=ActionStatus.PENDING,
            target_platform=target_platform,
            reason=reason,
            action_url=action_url,
            priority=priority,
            auto_dismiss_after_hours=24  # Cancelamentos expiram em 24h
        )

        self.db.add(action)
        self.db.commit()
        self.db.refresh(action)

        logger.info(f"✅ Cancel action created: ID={action.id}")
        return action

    def get_pending_actions(self, property_id: int) -> List[SyncAction]:
        """
        Retorna todas as ações pendentes de um imóvel.

        Args:
            property_id: ID do imóvel

        Returns:
            Lista de SyncAction pendentes
        """
        return self.db.query(SyncAction).filter(
            and_(
                SyncAction.property_id == property_id,
                SyncAction.status == ActionStatus.PENDING
            )
        ).order_by(
            # Ordenar por prioridade (crítico primeiro)
            SyncAction.priority.desc(),
            SyncAction.created_at.asc()
        ).all()

    def get_action_by_id(self, action_id: int) -> Optional[SyncAction]:
        """Busca uma ação por ID"""
        return self.db.query(SyncAction).filter(SyncAction.id == action_id).first()

    def mark_action_completed(
        self,
        action_id: int,
        notes: str = None
    ) -> Optional[SyncAction]:
        """
        Marca uma ação como completada.

        Args:
            action_id: ID da ação
            notes: Notas do usuário (opcional)

        Returns:
            SyncAction atualizada ou None
        """
        action = self.get_action_by_id(action_id)

        if not action:
            logger.warning(f"Action {action_id} not found")
            return None

        action.mark_completed(notes)
        self.db.commit()
        self.db.refresh(action)

        logger.info(f"✅ Action {action_id} marked as completed")
        return action

    def mark_action_dismissed(
        self,
        action_id: int,
        notes: str = None
    ) -> Optional[SyncAction]:
        """
        Marca uma ação como descartada.

        Args:
            action_id: ID da ação
            notes: Motivo do descarte (opcional)

        Returns:
            SyncAction atualizada ou None
        """
        action = self.get_action_by_id(action_id)

        if not action:
            logger.warning(f"Action {action_id} not found")
            return None

        action.mark_dismissed(notes)
        self.db.commit()
        self.db.refresh(action)

        logger.info(f"Action {action_id} dismissed")
        return action

    def auto_dismiss_expired_actions(self, property_id: int) -> int:
        """
        Auto-descarta ações que expiraram.

        Args:
            property_id: ID do imóvel

        Returns:
            Número de ações descartadas
        """
        pending_actions = self.get_pending_actions(property_id)
        dismissed_count = 0

        for action in pending_actions:
            if action.should_auto_dismiss:
                action.status = ActionStatus.EXPIRED
                action.dismissed_at = datetime.utcnow()
                action.user_notes = "Auto-dismissed: expired"
                dismissed_count += 1

        if dismissed_count > 0:
            self.db.commit()
            logger.info(f"Auto-dismissed {dismissed_count} expired actions")

        return dismissed_count

    def get_action_summary(self, property_id: int) -> Dict[str, int]:
        """
        Retorna resumo de ações.

        Args:
            property_id: ID do imóvel

        Returns:
            Dicionário com contadores
        """
        total_pending = self.db.query(SyncAction).filter(
            and_(
                SyncAction.property_id == property_id,
                SyncAction.status == ActionStatus.PENDING
            )
        ).count()

        critical_pending = self.db.query(SyncAction).filter(
            and_(
                SyncAction.property_id == property_id,
                SyncAction.status == ActionStatus.PENDING,
                SyncAction.priority == "critical"
            )
        ).count()

        total_completed = self.db.query(SyncAction).filter(
            and_(
                SyncAction.property_id == property_id,
                SyncAction.status == ActionStatus.COMPLETED
            )
        ).count()

        return {
            "pending": total_pending,
            "critical": critical_pending,
            "completed": total_completed
        }

    def _generate_block_url(
        self,
        platform: TargetPlatform,
        start_date: date,
        end_date: date
    ) -> Optional[str]:
        """
        Gera URL direta para bloqueio (quando possível).

        Args:
            platform: Plataforma alvo
            start_date: Data inicial
            end_date: Data final

        Returns:
            URL ou None
        """
        if platform == TargetPlatform.AIRBNB:
            # Airbnb não tem URL direta para bloqueio específico
            return "https://www.airbnb.com/hosting/calendar"

        elif platform == TargetPlatform.BOOKING:
            # Booking também não tem URL direta parametrizada publicamente
            return "https://admin.booking.com/hotel/hoteladmin/availability.html"

        return None

    def _generate_cancel_url(self, booking: Booking) -> Optional[str]:
        """
        Gera URL direta para cancelamento (quando possível).

        Args:
            booking: Reserva a ser cancelada

        Returns:
            URL ou None
        """
        if booking.platform == "airbnb":
            # Airbnb não expõe URLs diretas de reserva via iCal
            return "https://www.airbnb.com/hosting/reservations"

        elif booking.platform == "booking":
            # Booking também não
            return "https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/booking.html"

        return None
