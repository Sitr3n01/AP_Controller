"""
Bot do Telegram para gerenciamento de apartamento.
Fornece comandos para visualizar reservas, conflitos e receber notificações.
"""
import asyncio
from datetime import datetime
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Booking, BookingConflict, Property
from app.core.calendar_sync import CalendarSync
from app.core.conflict_detector import ConflictDetector


class TelegramBot:
    """Bot do Telegram para gerenciamento de apartamento"""

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.admin_ids = settings.admin_user_ids
        self.application: Optional[Application] = None
        self._running = False

    async def start(self):
        """Inicia o bot"""
        if not self.token or self.token == "":
            print("⚠️  TELEGRAM_BOT_TOKEN não configurado. Bot não será iniciado.")
            return

        if not self.admin_ids:
            print("⚠️  TELEGRAM_ADMIN_USER_IDS não configurado. Bot não será iniciado.")
            return

        # Criar aplicação
        self.application = Application.builder().token(self.token).build()

        # Registrar handlers
        self._register_handlers()

        # Iniciar bot
        print("🤖 Iniciando bot do Telegram...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        self._running = True
        print("✅ Bot do Telegram iniciado com sucesso!")

    async def stop(self):
        """Para o bot"""
        if self.application and self._running:
            print("🛑 Parando bot do Telegram...")
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self._running = False
            print("✅ Bot do Telegram parado!")

    def _register_handlers(self):
        """Registra todos os handlers de comandos"""
        # Comandos básicos
        self.application.add_handler(CommandHandler("start", self._cmd_start))
        self.application.add_handler(CommandHandler("help", self._cmd_help))
        self.application.add_handler(CommandHandler("menu", self._cmd_menu))

        # Comandos de informação
        self.application.add_handler(CommandHandler("status", self._cmd_status))
        self.application.add_handler(CommandHandler("reservas", self._cmd_reservas))
        self.application.add_handler(CommandHandler("hoje", self._cmd_hoje))
        self.application.add_handler(CommandHandler("proximas", self._cmd_proximas))
        self.application.add_handler(CommandHandler("conflitos", self._cmd_conflitos))

        # Comandos de ação
        self.application.add_handler(CommandHandler("sync", self._cmd_sync))

        # Callback queries (botões inline)
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))

        # Handler de mensagens desconhecidas
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

    def _check_admin(self, user_id: int) -> bool:
        """Verifica se o usuário é admin"""
        return user_id in self.admin_ids

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Boas-vindas"""
        user = update.effective_user
        if not self._check_admin(user.id):
            await update.message.reply_text(
                "❌ Você não tem permissão para usar este bot.\n"
                f"Seu ID: {user.id}"
            )
            return

        welcome_text = (
            f"👋 Olá, {user.first_name}!\n\n"
            "🏢 Bem-vindo ao **SENTINEL** - Sistema de Gerenciamento de Apartamento\n\n"
            "Aqui você pode:\n"
            "• Ver status das reservas\n"
            "• Verificar conflitos\n"
            "• Sincronizar calendários\n"
            "• Receber notificações importantes\n\n"
            "Digite /help para ver todos os comandos disponíveis."
        )

        await update.message.reply_text(
            welcome_text,
            parse_mode="Markdown",
            reply_markup=self._get_main_menu_keyboard(),
        )

    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Lista de comandos"""
        if not self._check_admin(update.effective_user.id):
            return

        help_text = (
            "📋 **Comandos Disponíveis:**\n\n"
            "**Informações:**\n"
            "/status - Status geral do sistema\n"
            "/reservas - Lista todas as reservas\n"
            "/hoje - Check-ins e check-outs de hoje\n"
            "/proximas - Próximas 5 reservas\n"
            "/conflitos - Conflitos detectados\n\n"
            "**Ações:**\n"
            "/sync - Sincronizar calendários agora\n\n"
            "**Outros:**\n"
            "/menu - Menu principal\n"
            "/help - Esta mensagem\n\n"
            "💡 Use os botões do menu para navegar facilmente!"
        )

        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def _cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /menu - Menu principal"""
        if not self._check_admin(update.effective_user.id):
            return

        await update.message.reply_text(
            "🏠 **Menu Principal**\n\nEscolha uma opção:",
            parse_mode="Markdown",
            reply_markup=self._get_main_menu_keyboard(),
        )

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Status do sistema"""
        if not self._check_admin(update.effective_user.id):
            return

        db: Session = next(get_db())
        try:
            # Buscar dados
            property_obj = db.query(Property).first()
            total_bookings = db.query(Booking).count()
            active_bookings = (
                db.query(Booking).filter(Booking.status == "confirmed").count()
            )
            conflicts_count = (
                db.query(BookingConflict).filter(BookingConflict.resolved == False).count()
            )

            # Montar mensagem
            status_text = (
                "📊 **Status do Sistema**\n\n"
                f"🏢 Apartamento: {property_obj.name if property_obj else 'N/A'}\n"
                f"📅 Total de Reservas: {total_bookings}\n"
                f"✅ Reservas Ativas: {active_bookings}\n"
                f"⚠️ Conflitos: {conflicts_count}\n\n"
                f"🕐 Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

            await update.message.reply_text(status_text, parse_mode="Markdown")
        finally:
            db.close()

    async def _cmd_reservas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /reservas - Lista reservas confirmadas"""
        if not self._check_admin(update.effective_user.id):
            return

        db: Session = next(get_db())
        try:
            bookings = (
                db.query(Booking)
                .filter(Booking.status == "confirmed")
                .order_by(Booking.check_in_date)
                .limit(10)
                .all()
            )

            if not bookings:
                await update.message.reply_text("📭 Nenhuma reserva confirmada encontrada.")
                return

            text = f"📅 **Reservas Confirmadas** (10 mais próximas)\n\n"
            for booking in bookings:
                platform_emoji = self._get_platform_emoji(booking.platform)
                text += (
                    f"{platform_emoji} **{booking.guest_name}**\n"
                    f"  📆 {booking.check_in_date.strftime('%d/%m')} → "
                    f"{booking.check_out_date.strftime('%d/%m')} "
                    f"({booking.nights_count} noites)\n"
                    f"  👥 {booking.guest_count} hóspede(s)\n"
                )
                if booking.total_price:
                    text += f"  💰 R$ {booking.total_price:.2f}\n"
                text += "\n"

            await update.message.reply_text(text, parse_mode="Markdown")
        finally:
            db.close()

    async def _cmd_hoje(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /hoje - Check-ins e check-outs de hoje"""
        if not self._check_admin(update.effective_user.id):
            return

        db: Session = next(get_db())
        try:
            today = datetime.now().date()

            checkins = (
                db.query(Booking)
                .filter(
                    Booking.check_in_date == today,
                    Booking.status == "confirmed",
                )
                .all()
            )

            checkouts = (
                db.query(Booking)
                .filter(
                    Booking.check_out_date == today,
                    Booking.status == "confirmed",
                )
                .all()
            )

            text = f"📅 **Atividades de Hoje** - {today.strftime('%d/%m/%Y')}\n\n"

            if checkins:
                text += "🟢 **CHECK-INS:**\n"
                for booking in checkins:
                    platform_emoji = self._get_platform_emoji(booking.platform)
                    text += (
                        f"{platform_emoji} {booking.guest_name} "
                        f"({booking.guest_count} hóspede(s))\n"
                    )
                text += "\n"
            else:
                text += "🟢 **CHECK-INS:** Nenhum\n\n"

            if checkouts:
                text += "🟡 **CHECK-OUTS:**\n"
                for booking in checkouts:
                    platform_emoji = self._get_platform_emoji(booking.platform)
                    text += f"{platform_emoji} {booking.guest_name}\n"
                text += "\n"
            else:
                text += "🟡 **CHECK-OUTS:** Nenhum\n\n"

            if not checkins and not checkouts:
                text += "✨ Nenhuma atividade para hoje!"

            await update.message.reply_text(text, parse_mode="Markdown")
        finally:
            db.close()

    async def _cmd_proximas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /proximas - Próximas 5 reservas"""
        if not self._check_admin(update.effective_user.id):
            return

        db: Session = next(get_db())
        try:
            now = datetime.now().date()
            bookings = (
                db.query(Booking)
                .filter(
                    Booking.check_in_date >= now,
                    Booking.status == "confirmed",
                )
                .order_by(Booking.check_in_date)
                .limit(5)
                .all()
            )

            if not bookings:
                await update.message.reply_text("📭 Nenhuma reserva futura encontrada.")
                return

            text = "🔜 **Próximas 5 Reservas**\n\n"
            for booking in bookings:
                platform_emoji = self._get_platform_emoji(booking.platform)
                days_until = (booking.check_in_date - now).days
                text += (
                    f"{platform_emoji} **{booking.guest_name}**\n"
                    f"  📆 Check-in: {booking.check_in_date.strftime('%d/%m/%Y')} "
                    f"({days_until} dia(s))\n"
                    f"  🌙 {booking.nights_count} noite(s)\n"
                    f"  👥 {booking.guest_count} hóspede(s)\n\n"
                )

            await update.message.reply_text(text, parse_mode="Markdown")
        finally:
            db.close()

    async def _cmd_conflitos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /conflitos - Lista conflitos ativos"""
        if not self._check_admin(update.effective_user.id):
            return

        db: Session = next(get_db())
        try:
            conflicts = (
                db.query(BookingConflict)
                .filter(BookingConflict.resolved == False)
                .all()
            )

            if not conflicts:
                await update.message.reply_text("✅ Nenhum conflito detectado!")
                return

            text = f"⚠️ **Conflitos Detectados** ({len(conflicts)})\n\n"

            for conflict in conflicts:
                severity_emoji = self._get_severity_emoji(conflict.severity)
                type_text = "Duplicata" if conflict.conflict_type == "duplicate" else "Sobreposição"

                text += (
                    f"{severity_emoji} **{type_text}** - {conflict.severity.upper()}\n"
                    f"  📅 Reserva 1: {conflict.booking_1.guest_name}\n"
                    f"  📅 Reserva 2: {conflict.booking_2.guest_name}\n"
                    f"  🗓 Período: {conflict.booking_1.check_in_date.strftime('%d/%m')} → "
                    f"{conflict.booking_1.check_out_date.strftime('%d/%m')}\n\n"
                )

            text += "💡 Resolva os conflitos na interface web."

            await update.message.reply_text(text, parse_mode="Markdown")
        finally:
            db.close()

    async def _cmd_sync(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /sync - Sincroniza calendários"""
        if not self._check_admin(update.effective_user.id):
            return

        await update.message.reply_text("🔄 Iniciando sincronização dos calendários...")

        db: Session = next(get_db())
        try:
            # Sincronizar
            sync = CalendarSync(db)
            results = await sync.sync_all_properties()

            # Detectar conflitos
            detector = ConflictDetector(db)
            conflicts = detector.detect_all_conflicts()

            # Montar resposta
            total_new = sum(r["new_bookings"] for r in results)
            total_updated = sum(r["updated_bookings"] for r in results)
            total_conflicts = len(conflicts)

            text = (
                "✅ **Sincronização Concluída!**\n\n"
                f"📥 Novas reservas: {total_new}\n"
                f"🔄 Atualizadas: {total_updated}\n"
                f"⚠️ Conflitos: {total_conflicts}\n\n"
                f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

            if total_conflicts > 0:
                text += "\n\n💡 Use /conflitos para ver detalhes"

            await update.message.reply_text(text, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Erro na sincronização: {str(e)}")
        finally:
            db.close()

    async def _handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handler para botões inline"""
        query = update.callback_query
        await query.answer()

        # Mapear callbacks para comandos
        callback_map = {
            "status": self._cmd_status,
            "reservas": self._cmd_reservas,
            "hoje": self._cmd_hoje,
            "proximas": self._cmd_proximas,
            "conflitos": self._cmd_conflitos,
            "sync": self._cmd_sync,
            "menu": self._cmd_menu,
        }

        handler = callback_map.get(query.data)
        if handler:
            # Criar update fake para reusar handlers
            update.message = query.message
            await handler(update, context)

    async def _handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handler para mensagens de texto"""
        if not self._check_admin(update.effective_user.id):
            return

        await update.message.reply_text(
            "❓ Comando não reconhecido.\n"
            "Digite /help para ver os comandos disponíveis."
        )

    def _get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Retorna teclado do menu principal"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Status", callback_data="status"),
                InlineKeyboardButton("📅 Reservas", callback_data="reservas"),
            ],
            [
                InlineKeyboardButton("📆 Hoje", callback_data="hoje"),
                InlineKeyboardButton("🔜 Próximas", callback_data="proximas"),
            ],
            [
                InlineKeyboardButton("⚠️ Conflitos", callback_data="conflitos"),
                InlineKeyboardButton("🔄 Sincronizar", callback_data="sync"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    def _get_platform_emoji(self, platform: str) -> str:
        """Retorna emoji para a plataforma"""
        emojis = {
            "airbnb": "🔴",
            "booking": "🔵",
            "manual": "⚪",
        }
        return emojis.get(platform, "⚫")

    def _get_severity_emoji(self, severity: str) -> str:
        """Retorna emoji para severidade"""
        emojis = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }
        return emojis.get(severity, "⚪")
