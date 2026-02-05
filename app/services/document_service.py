# app/services/document_service.py
"""
Serviço de geração automática de documentos.
Suporta templates DOCX para autorização de condomínio e outros documentos.
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from docxtpl import DocxTemplate
from docx import Document
import io

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentService:
    """
    Serviço para geração de documentos a partir de templates.

    Suporta:
    - Templates DOCX com placeholders
    - Geração automática de autorizações
    - Substituição de variáveis
    - Salvar em arquivo ou retornar bytes
    """

    def __init__(self):
        """Inicializa o serviço de documentos"""
        self.template_dir = Path(settings.TEMPLATE_DIR)
        self.output_dir = Path(settings.OUTPUT_DIR)

        # Garantir que diretórios existem
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_condo_authorization(
        self,
        booking_data: Dict[str, Any],
        property_data: Dict[str, Any],
        guest_data: Dict[str, Any],
        save_to_file: bool = True
    ) -> Dict[str, Any]:
        """
        Gera autorização de condomínio para um hóspede.

        Args:
            booking_data: Dados da reserva (check_in, check_out, etc)
            property_data: Dados do imóvel (nome, endereço, etc)
            guest_data: Dados do hóspede (nome, CPF, etc)
            save_to_file: Se True, salva em arquivo. Se False, retorna bytes.

        Returns:
            Dict com:
                - success: bool
                - file_path: str (se save_to_file=True)
                - file_bytes: bytes (se save_to_file=False)
                - message: str

        Example:
            >>> doc_service = DocumentService()
            >>> result = doc_service.generate_condo_authorization(
            ...     booking_data={'check_in': '2024-01-15', 'check_out': '2024-01-20'},
            ...     property_data={'name': 'Apt 101', 'address': 'Rua X'},
            ...     guest_data={'name': 'João Silva', 'cpf': '123.456.789-00'}
            ... )
        """
        try:
            template_path = self.template_dir / settings.DEFAULT_TEMPLATE

            # Verificar se template existe
            if not template_path.exists():
                logger.warning(f"Template not found: {template_path}, creating default")
                self._create_default_template(template_path)

            # Carregar template
            doc = DocxTemplate(template_path)

            # Preparar contexto com dados
            context = self._prepare_condo_authorization_context(
                booking_data, property_data, guest_data
            )

            # Renderizar template
            doc.render(context)

            # Salvar ou retornar bytes
            if save_to_file:
                filename = self._generate_filename(guest_data.get('name', 'hospede'))
                file_path = self.output_dir / filename
                doc.save(str(file_path))

                logger.info(f"Document generated: {file_path}")

                return {
                    "success": True,
                    "file_path": str(file_path),
                    "filename": filename,
                    "message": "Documento gerado com sucesso"
                }
            else:
                # Retornar bytes
                doc_bytes = io.BytesIO()
                doc.save(doc_bytes)
                doc_bytes.seek(0)

                return {
                    "success": True,
                    "file_bytes": doc_bytes.getvalue(),
                    "filename": self._generate_filename(guest_data.get('name', 'hospede')),
                    "message": "Documento gerado com sucesso"
                }

        except Exception as e:
            logger.error(f"Error generating document: {e}")
            return {
                "success": False,
                "message": f"Erro ao gerar documento: {str(e)}"
            }

    def _prepare_condo_authorization_context(
        self,
        booking_data: Dict[str, Any],
        property_data: Dict[str, Any],
        guest_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepara o contexto com todas as variáveis para o template.

        Variáveis disponíveis no template:
        - {{ guest_name }} - Nome do hóspede
        - {{ guest_cpf }} - CPF do hóspede
        - {{ guest_phone }} - Telefone do hóspede
        - {{ check_in }} - Data de check-in
        - {{ check_out }} - Data de check-out
        - {{ property_name }} - Nome do imóvel
        - {{ property_address }} - Endereço completo
        - {{ condo_name }} - Nome do condomínio
        - {{ date_today }} - Data de hoje
        - {{ owner_name }} - Nome do proprietário
        """
        # Formatar datas
        check_in = booking_data.get('check_in')
        check_out = booking_data.get('check_out')

        if isinstance(check_in, str):
            check_in_formatted = datetime.fromisoformat(check_in).strftime('%d/%m/%Y')
        else:
            check_in_formatted = check_in.strftime('%d/%m/%Y') if check_in else ''

        if isinstance(check_out, str):
            check_out_formatted = datetime.fromisoformat(check_out).strftime('%d/%m/%Y')
        else:
            check_out_formatted = check_out.strftime('%d/%m/%Y') if check_out else ''

        context = {
            # Hóspede
            'guest_name': guest_data.get('name', ''),
            'guest_cpf': guest_data.get('cpf', guest_data.get('document_number', '')),
            'guest_phone': guest_data.get('phone', ''),
            'guest_email': guest_data.get('email', ''),

            # Reserva
            'check_in': check_in_formatted,
            'check_out': check_out_formatted,
            'booking_id': booking_data.get('id', ''),

            # Imóvel
            'property_name': property_data.get('name', settings.PROPERTY_NAME),
            'property_address': property_data.get('address', settings.PROPERTY_ADDRESS),
            'condo_name': property_data.get('condo_name', settings.CONDO_NAME),

            # Outros
            'date_today': datetime.now().strftime('%d/%m/%Y'),
            'owner_name': property_data.get('owner_name', ''),
            'condo_admin': settings.CONDO_ADMIN_NAME,
        }

        return context

    def _generate_filename(self, guest_name: str) -> str:
        """
        Gera nome de arquivo único para o documento.

        Formato: autorizacao_NOME_DDMMYYYY_HHMMSS.docx
        """
        # Limpar nome do hóspede (remover caracteres especiais)
        clean_name = "".join(c for c in guest_name if c.isalnum() or c.isspace())
        clean_name = clean_name.replace(' ', '_')[:30]  # Limitar tamanho

        timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
        filename = f"autorizacao_{clean_name}_{timestamp}.docx"

        return filename

    def _create_default_template(self, template_path: Path):
        """
        Cria um template padrão de autorização de condomínio.

        Este template serve como exemplo e deve ser customizado conforme necessário.
        """
        doc = Document()

        # Título
        doc.add_heading('AUTORIZAÇÃO DE ACESSO AO CONDOMÍNIO', 0)

        # Corpo
        doc.add_paragraph(f"\n{settings.CONDO_ADMIN_NAME}")
        doc.add_paragraph(f"{settings.CONDO_NAME}")
        doc.add_paragraph("\nRef.: Autorização de Acesso para Hóspede")

        doc.add_paragraph("\nPrezados,")

        doc.add_paragraph(
            "\nVenho por meio desta autorizar o acesso do(a) Sr(a). {{{{ guest_name }}}}, "
            "portador(a) do CPF {{{{ guest_cpf }}}}, ao apartamento situado no endereço "
            "{{{{ property_address }}}}."
        )

        doc.add_paragraph(
            "\nO período autorizado para permanência é de {{{{ check_in }}}} até {{{{ check_out }}}}."
        )

        doc.add_paragraph("\nDados do Hóspede:")
        doc.add_paragraph("• Nome: {{{{ guest_name }}}}")
        doc.add_paragraph("• CPF: {{{{ guest_cpf }}}}")
        doc.add_paragraph("• Telefone: {{{{ guest_phone }}}}")

        doc.add_paragraph("\nAtenciosamente,")
        doc.add_paragraph("\n\n_________________________________")
        doc.add_paragraph("{{{{ owner_name }}}}")
        doc.add_paragraph("Proprietário(a)")

        doc.add_paragraph(f"\n{settings.PROPERTY_ADDRESS}")
        doc.add_paragraph(f"Data: {{{{ date_today }}}}")

        # Salvar template
        doc.save(str(template_path))
        logger.info(f"Default template created: {template_path}")

    def list_generated_documents(self, limit: int = 50) -> list[Dict[str, Any]]:
        """
        Lista os documentos gerados mais recentes.

        Args:
            limit: Número máximo de documentos a retornar

        Returns:
            Lista de dicts com informações dos documentos
        """
        documents = []

        for file_path in sorted(
            self.output_dir.glob("*.docx"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]:
            stat = file_path.stat()
            documents.append({
                "filename": file_path.name,
                "path": str(file_path),
                "size_kb": round(stat.st_size / 1024, 2),
                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

        return documents

    def get_document_path(self, filename: str) -> Optional[Path]:
        """
        Retorna o caminho completo de um documento gerado.

        Args:
            filename: Nome do arquivo

        Returns:
            Path do arquivo se existir, None caso contrário
        """
        file_path = self.output_dir / filename
        return file_path if file_path.exists() else None

    def delete_document(self, filename: str) -> bool:
        """
        Deleta um documento gerado.

        Args:
            filename: Nome do arquivo a deletar

        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            file_path = self.output_dir / filename
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Document deleted: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
