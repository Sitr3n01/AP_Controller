# app/routers/documents.py
"""
Router para geração e gerenciamento de documentos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database.session import get_db
from app.models.user import User
from app.models.booking import Booking
from app.models.property import Property
from app.models.guest import Guest
from app.middleware.auth import get_current_active_user
from app.services.document_service import DocumentService
from app.schemas.document import (
    GenerateDocumentRequest,
    GenerateDocumentFromBookingRequest,
    DocumentResponse,
    DocumentListResponse,
    DocumentListItem
)

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])
doc_service = DocumentService()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(
    request: GenerateDocumentRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera documento de autorização de condomínio com dados personalizados.

    Permite especificar manualmente todos os dados (hóspede, imóvel, reserva).

    Returns:
        DocumentResponse com sucesso e caminho/nome do arquivo gerado
    """
    # Converter para dict
    booking_data = request.booking.model_dump()
    property_data = request.property.model_dump()
    guest_data = request.guest.model_dump()

    # Gerar documento
    result = doc_service.generate_condo_authorization(
        booking_data=booking_data,
        property_data=property_data,
        guest_data=guest_data,
        save_to_file=request.save_to_file
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )

    # Construir response
    response = DocumentResponse(
        success=True,
        message=result["message"],
        filename=result.get("filename")
    )

    if request.save_to_file:
        response.file_path = result.get("file_path")
        response.download_url = f"/api/v1/documents/download/{result.get('filename')}"
    else:
        # Para bytes, indicar que deve usar endpoint de download
        response.download_url = "/api/v1/documents/generate-and-download"

    return response


@router.post("/generate-from-booking", response_model=DocumentResponse)
def generate_document_from_booking(
    request: GenerateDocumentFromBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera documento de autorização a partir de uma reserva existente.

    Busca automaticamente os dados da reserva, imóvel e hóspede do banco de dados.

    Args:
        request: Contém booking_id

    Returns:
        DocumentResponse com sucesso e caminho do arquivo gerado
    """
    # Buscar reserva
    booking = db.query(Booking).filter(Booking.id == request.booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva com ID {request.booking_id} não encontrada"
        )

    # Buscar imóvel
    property_obj = db.query(Property).filter(Property.id == booking.property_id).first()

    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel da reserva não encontrado"
        )

    # Buscar hóspede (se existir guest_id)
    guest_data = {}
    if booking.guest_id:
        guest = db.query(Guest).filter(Guest.id == booking.guest_id).first()
        if guest:
            guest_data = {
                "name": guest.name,
                "cpf": guest.document_number,
                "phone": guest.phone,
                "email": guest.email
            }

    # Se não tem hóspede cadastrado, usar guest_name da reserva
    if not guest_data:
        guest_data = {
            "name": booking.guest_name or "Hóspede",
            "cpf": "",
            "phone": "",
            "email": ""
        }

    # Preparar dados
    booking_data = {
        "id": booking.id,
        "check_in": booking.check_in,
        "check_out": booking.check_out
    }

    property_data = {
        "name": property_obj.name,
        "address": property_obj.address,
        "condo_name": getattr(property_obj, 'condo_name', None),
        "owner_name": ""  # Pode adicionar campo owner no modelo Property
    }

    # Gerar documento
    result = doc_service.generate_condo_authorization(
        booking_data=booking_data,
        property_data=property_data,
        guest_data=guest_data,
        save_to_file=request.save_to_file
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )

    return DocumentResponse(
        success=True,
        message=result["message"],
        filename=result.get("filename"),
        file_path=result.get("file_path"),
        download_url=f"/api/v1/documents/download/{result.get('filename')}"
    )


@router.get("/list", response_model=DocumentListResponse)
def list_documents(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista documentos gerados recentemente.

    Args:
        limit: Número máximo de documentos a retornar (padrão 50)

    Returns:
        DocumentListResponse com lista de documentos
    """
    documents = doc_service.list_generated_documents(limit=limit)

    return DocumentListResponse(
        total=len(documents),
        documents=[DocumentListItem(**doc) for doc in documents]
    )


@router.get("/download/{filename}")
def download_document(
    filename: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Faz download de um documento gerado.

    Args:
        filename: Nome do arquivo a baixar

    Returns:
        FileResponse com o documento
    """
    file_path = doc_service.get_document_path(filename)

    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.delete("/{filename}", status_code=status.HTTP_200_OK)
def delete_document(
    filename: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Deleta um documento gerado.

    Args:
        filename: Nome do arquivo a deletar

    Returns:
        Mensagem de sucesso
    """
    success = doc_service.delete_document(filename)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )

    return {"message": "Documento deletado com sucesso"}


@router.post("/generate-and-download")
async def generate_and_download(
    request: GenerateDocumentRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera documento e retorna para download imediato (sem salvar em arquivo).

    Útil para gerar documentos sob demanda sem ocupar espaço em disco.

    Returns:
        StreamingResponse com o documento DOCX
    """
    # Converter para dict
    booking_data = request.booking.model_dump()
    property_data = request.property.model_dump()
    guest_data = request.guest.model_dump()

    # Gerar documento (sem salvar em arquivo)
    result = doc_service.generate_condo_authorization(
        booking_data=booking_data,
        property_data=property_data,
        guest_data=guest_data,
        save_to_file=False
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )

    # Retornar como streaming response
    file_bytes = result.get("file_bytes")
    filename = result.get("filename")

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
