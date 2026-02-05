# app/services/email_service.py
"""
Serviço universal de email com suporte IMAP/SMTP.
Compatível com Gmail, Outlook, Yahoo e outros provedores.
"""
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import List, Dict, Any, Optional
import aiosmtplib
import aioimaplib
from jinja2 import Environment, FileSystemLoader, Template

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmailConfig:
    """Configuração de servidor de email"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        imap_host: str,
        imap_port: int,
        username: str,
        password: str,
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.username = username
        self.password = password
        self.use_tls = use_tls


class EmailService:
    """
    Serviço universal de email com IMAP/SMTP.

    Suporta:
    - Envio de emails (SMTP)
    - Leitura de emails (IMAP)
    - Templates HTML com Jinja2
    - Anexos
    - Gmail, Outlook, Yahoo, etc
    """

    # Configurações pré-definidas para provedores populares
    PROVIDERS = {
        "gmail": {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "use_tls": True
        },
        "outlook": {
            "smtp_host": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "imap_host": "outlook.office365.com",
            "imap_port": 993,
            "use_tls": True
        },
        "yahoo": {
            "smtp_host": "smtp.mail.yahoo.com",
            "smtp_port": 587,
            "imap_host": "imap.mail.yahoo.com",
            "imap_port": 993,
            "use_tls": True
        }
    }

    def __init__(self, config: EmailConfig):
        """
        Inicializa o serviço de email.

        Args:
            config: Configuração do servidor de email
        """
        self.config = config
        self.template_env = self._setup_template_engine()

    @classmethod
    def from_provider(
        cls,
        provider: str,
        username: str,
        password: str
    ) -> "EmailService":
        """
        Cria instância a partir de provedor pré-configurado.

        Args:
            provider: Nome do provedor (gmail, outlook, yahoo)
            username: Email do usuário
            password: Senha ou app password

        Returns:
            EmailService configurado

        Example:
            >>> service = EmailService.from_provider("gmail", "user@gmail.com", "password")
        """
        if provider.lower() not in cls.PROVIDERS:
            raise ValueError(
                f"Provider '{provider}' not supported. "
                f"Use one of: {', '.join(cls.PROVIDERS.keys())}"
            )

        provider_config = cls.PROVIDERS[provider.lower()]
        config = EmailConfig(
            smtp_host=provider_config["smtp_host"],
            smtp_port=provider_config["smtp_port"],
            imap_host=provider_config["imap_host"],
            imap_port=provider_config["imap_port"],
            username=username,
            password=password,
            use_tls=provider_config["use_tls"]
        )

        return cls(config)

    def _setup_template_engine(self) -> Environment:
        """Configura Jinja2 para templates de email"""
        template_dir = Path("app/templates/email")
        template_dir.mkdir(parents=True, exist_ok=True)

        return Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True
        )

    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Envia email via SMTP.

        Args:
            to: Lista de destinatários
            subject: Assunto do email
            body: Corpo do email (texto ou HTML)
            html: Se True, body é HTML. Se False, texto plano.
            cc: Lista de emails em cópia
            bcc: Lista de emails em cópia oculta
            attachments: Lista de anexos [{"filename": "file.pdf", "content": bytes}]

        Returns:
            Dict com:
                - success: bool
                - message: str
                - message_id: str (se sucesso)

        Example:
            >>> await service.send_email(
            ...     to=["guest@example.com"],
            ...     subject="Confirmação de Reserva",
            ...     body="<h1>Bem-vindo!</h1>",
            ...     html=True
            ... )
        """
        try:
            # Criar mensagem
            import uuid
            msg = MIMEMultipart()
            msg["From"] = self.config.username
            msg["To"] = ", ".join(to)
            msg["Subject"] = subject
            # FIX: Garantir Message-ID para rastreamento
            msg["Message-ID"] = f"<{uuid.uuid4()}@sentinel.local>"

            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)

            # Adicionar corpo
            mime_type = "html" if html else "plain"
            msg.attach(MIMEText(body, mime_type, "utf-8"))

            # Adicionar anexos
            if attachments:
                from app.core.validators import sanitize_filename
                for attachment in attachments:
                    # FIX: Sanitizar filename do attachment
                    safe_filename = sanitize_filename(attachment["filename"])

                    part = MIMEApplication(attachment["content"])
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=safe_filename
                    )
                    msg.attach(part)

            # Enviar email
            async with aiosmtplib.SMTP(
                hostname=self.config.smtp_host,
                port=self.config.smtp_port,
                use_tls=self.config.use_tls
            ) as smtp:
                await smtp.login(self.config.username, self.config.password)

                # Combinar todos os destinatários
                all_recipients = to.copy()
                if cc:
                    all_recipients.extend(cc)
                if bcc:
                    all_recipients.extend(bcc)

                await smtp.send_message(msg, recipients=all_recipients)

            logger.info(f"Email sent successfully to {', '.join(to)}")

            return {
                "success": True,
                "message": "Email enviado com sucesso",
                "message_id": msg.get("Message-ID", "")
            }

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {
                "success": False,
                "message": f"Erro ao enviar email: {str(e)}"
            }

    async def send_template_email(
        self,
        to: List[str],
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envia email usando template Jinja2.

        Args:
            to: Lista de destinatários
            subject: Assunto
            template_name: Nome do template (ex: "booking_confirmation.html")
            context: Dicionário com variáveis do template
            **kwargs: Argumentos adicionais para send_email (cc, bcc, attachments)

        Returns:
            Dict com resultado do envio

        Example:
            >>> await service.send_template_email(
            ...     to=["guest@example.com"],
            ...     subject="Confirmação de Reserva",
            ...     template_name="booking_confirmation.html",
            ...     context={"guest_name": "João", "check_in": "15/01/2024"}
            ... )
        """
        try:
            # SECURITY FIX: Validar template_name para prevenir path traversal
            import os

            # Remover path traversal attempts
            safe_template_name = os.path.basename(template_name)

            # Verificar se template_name foi alterado (tentativa de path traversal)
            if safe_template_name != template_name or '..' in template_name or '/' in template_name or '\\' in template_name:
                logger.warning(f"Template path traversal attempt detected: {template_name}")
                return {
                    "success": False,
                    "message": "Nome de template inválido"
                }

            # Whitelist de templates permitidos
            ALLOWED_TEMPLATES = {
                'booking_confirmation.html',
                'checkin_reminder.html',
                'checkout_reminder.html',
                'payment_receipt.html',
                'welcome_email.html'
            }

            if safe_template_name not in ALLOWED_TEMPLATES:
                logger.warning(f"Attempt to use non-whitelisted template: {safe_template_name}")
                return {
                    "success": False,
                    "message": f"Template '{safe_template_name}' não está na lista de templates permitidos"
                }

            # SECURITY FIX: Sanitizar valores do context para prevenir XSS
            from app.core.validators import sanitize_html
            sanitized_context = {}
            for key, value in context.items():
                if isinstance(value, str):
                    sanitized_context[key] = sanitize_html(value)
                else:
                    sanitized_context[key] = value

            # Carregar e renderizar template
            template = self.template_env.get_template(safe_template_name)
            html_body = template.render(**sanitized_context)

            # Enviar email com HTML
            return await self.send_email(
                to=to,
                subject=subject,
                body=html_body,
                html=True,
                **kwargs
            )

        except Exception as e:
            logger.error(f"Error sending template email: {e}")
            return {
                "success": False,
                "message": f"Erro ao enviar email template: {str(e)}"
            }

    async def send_inline_template_email(
        self,
        to: List[str],
        subject: str,
        template_string: str,
        context: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envia email usando template inline (string).

        SECURITY WARNING: Esta função foi DESABILITADA por motivos de segurança.
        Templates inline podem causar Server-Side Template Injection (SSTI).
        Use send_template_email() com templates pré-definidos em arquivos.

        Args:
            to: Lista de destinatários
            subject: Assunto
            template_string: Template HTML como string (NÃO USADO)
            context: Variáveis do template
            **kwargs: Argumentos adicionais

        Returns:
            Dict com erro de segurança
        """
        # SECURITY FIX: Desabilitar templates inline para prevenir SSTI
        logger.error(
            "Tentativa de uso de send_inline_template_email() detectada. "
            "Esta função foi desabilitada por motivos de segurança (SSTI risk)."
        )
        return {
            "success": False,
            "message": (
                "Templates inline foram desabilitados por motivos de segurança. "
                "Use send_template_email() com templates em arquivo."
            )
        }

    async def fetch_emails(
        self,
        folder: str = "INBOX",
        limit: int = 10,
        unread_only: bool = False
    ) -> Dict[str, Any]:
        """
        Busca emails via IMAP.

        Args:
            folder: Pasta a buscar (INBOX, Sent, etc)
            limit: Número máximo de emails a retornar
            unread_only: Se True, busca apenas não lidos

        Returns:
            Dict com:
                - success: bool
                - emails: List[Dict] com informações dos emails
                - message: str

        Example:
            >>> result = await service.fetch_emails(unread_only=True, limit=5)
            >>> for email in result["emails"]:
            ...     print(email["subject"])
        """
        # FIX: Usar try/finally para garantir cleanup da conexão IMAP
        imap = None
        try:
            # Conectar IMAP
            imap = aioimaplib.IMAP4_SSL(
                host=self.config.imap_host,
                port=self.config.imap_port
            )

            await imap.wait_hello_from_server()
            await imap.login(self.config.username, self.config.password)
            await imap.select(folder)

            # Buscar emails
            if unread_only:
                search_criteria = "UNSEEN"
            else:
                search_criteria = "ALL"

            _, data = await imap.search(search_criteria)

            # FIX: Validar resposta antes de processar
            if not data or not data[0]:
                logger.info(f"No emails found in folder {folder}")
                return {
                    "success": True,
                    "emails": [],
                    "count": 0,
                    "message": "Nenhum email encontrado"
                }

            # Processar IDs dos emails
            email_ids = data[0].split()
            if not email_ids:
                return {
                    "success": True,
                    "emails": [],
                    "count": 0,
                    "message": "Nenhum email encontrado"
                }

            email_ids = email_ids[-limit:]  # Pegar últimos N emails

            emails = []
            for email_id in email_ids:
                _, msg_data = await imap.fetch(email_id, "(RFC822)")
                # Aqui você parsearia o email completo
                # Por simplicidade, retornamos estrutura básica
                emails.append({
                    "id": email_id.decode(),
                    "raw": msg_data[0][1].decode(errors="ignore")
                    # TODO: Parsear subject, from, date, body, etc
                })

            logger.info(f"Fetched {len(emails)} emails from {folder}")

            return {
                "success": True,
                "emails": emails,
                "count": len(emails),
                "message": f"{len(emails)} emails encontrados"
            }

        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return {
                "success": False,
                "emails": [],
                "count": 0,
                "message": f"Erro ao buscar emails: {str(e)}"
            }

        finally:
            # FIX: Garantir logout mesmo em caso de erro
            if imap:
                try:
                    await imap.logout()
                except Exception as e:
                    logger.debug(f"Error during IMAP logout (expected if connection failed): {e}")

    def create_booking_confirmation_template(self) -> str:
        """
        Retorna template HTML para confirmação de reserva.

        Este é um template inline que pode ser usado sem arquivo.

        Returns:
            String com HTML do template
        """
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 20px; margin-top: 20px; }
        .info { background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 Confirmação de Reserva</h1>
        </div>
        <div class="content">
            <p>Olá <strong>{{ guest_name }}</strong>,</p>
            <p>Sua reserva foi confirmada! Estamos muito felizes em recebê-lo(a).</p>

            <div class="info">
                <h3>📅 Detalhes da Reserva</h3>
                <p><strong>Check-in:</strong> {{ check_in }}</p>
                <p><strong>Check-out:</strong> {{ check_out }}</p>
                <p><strong>Imóvel:</strong> {{ property_name }}</p>
                <p><strong>Endereço:</strong> {{ property_address }}</p>
            </div>

            <div class="info">
                <h3>📝 Informações Importantes</h3>
                <p>• Check-in a partir das 14h</p>
                <p>• Check-out até as 12h</p>
                <p>• WiFi disponível no apartamento</p>
            </div>

            <p>Em caso de dúvidas, entre em contato conosco.</p>
            <p>Aguardamos você!</p>
        </div>
        <div class="footer">
            <p>SENTINEL - Sistema de Gestão de Apartamentos</p>
            <p>{{ property_address }}</p>
        </div>
    </div>
</body>
</html>
        """


# Helper para criar instância global (se necessário)
def get_email_service(
    provider: str = "gmail",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Optional[EmailService]:
    """
    Helper para criar EmailService a partir de variáveis de ambiente.

    Args:
        provider: Provedor de email (gmail, outlook, yahoo)
        username: Email (usa settings se None)
        password: Senha (usa settings se None)

    Returns:
        EmailService ou None se credenciais não configuradas
    """
    # Aqui você pode adicionar suporte a .env
    # Por exemplo: EMAIL_PROVIDER, EMAIL_USERNAME, EMAIL_PASSWORD
    # Por enquanto, requer parametros explícitos

    if not username or not password:
        logger.warning("Email credentials not provided")
        return None

    try:
        return EmailService.from_provider(provider, username, password)
    except Exception as e:
        logger.error(f"Error creating email service: {e}")
        return None
