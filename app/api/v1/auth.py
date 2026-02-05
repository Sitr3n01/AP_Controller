# app/api/v1/auth.py
"""
Endpoints de autenticação: login, registro, mudança de senha.
"""
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database.session import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.config import settings
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserResponse,
    ChangePasswordRequest,
    Token
)
from app.middleware.auth import get_current_user, get_current_active_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")  # Máximo 3 registros por minuto
def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registra novo usuário no sistema.

    Validações:
    - Email único
    - Username único
    - Senha forte (mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número)

    Returns:
        UserResponse: Dados do usuário criado (sem senha)
    """
    # Verificar se email já existe
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Verificar se username já existe
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já cadastrado"
        )

    # Criar usuário
    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        is_admin=False,  # Primeiro usuário pode ser tornado admin manualmente no DB
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # Máximo 5 tentativas de login por minuto
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Autentica usuário e retorna token JWT.

    Args:
        login_data: Username/email e senha

    Returns:
        LoginResponse: Token JWT e dados do usuário

    Raises:
        HTTPException 401: Se credenciais inválidas
    """
    # Buscar por username ou email
    user = db.query(User).filter(
        (User.username == login_data.username) | (User.email == login_data.username)
    ).first()

    # Verificar se usuário existe e senha correta
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username/email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Entre em contato com o administrador."
        )

    # Atualizar last_login
    user.last_login_at = datetime.utcnow()
    db.commit()

    # Criar token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
        },
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna informações do usuário atualmente autenticado.

    Requer: Token JWT válido no header Authorization

    Returns:
        UserResponse: Dados do usuário atual
    """
    return current_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Altera senha do usuário autenticado.

    Args:
        password_data: Senha antiga e nova senha
        current_user: Usuário autenticado (automático via token)

    Returns:
        dict: Mensagem de sucesso

    Raises:
        HTTPException 400: Se senha antiga incorreta
    """
    # Verificar senha antiga
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )

    # Verificar se nova senha é diferente
    if password_data.old_password == password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nova senha deve ser diferente da atual"
        )

    # Atualizar senha
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Senha alterada com sucesso"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout do usuário (no frontend, apenas descarta o token).

    Note: Como JWT é stateless, não há invalidação server-side.
    O frontend deve descartar o token ao fazer logout.

    Returns:
        dict: Mensagem de sucesso
    """
    # Em produção, poderia adicionar token a uma blacklist com Redis
    return {"message": "Logout realizado com sucesso"}


@router.delete("/delete-account", status_code=status.HTTP_200_OK)
def delete_account(
    password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deleta conta do usuário autenticado (IRREVERSÍVEL).

    Args:
        password: Senha do usuário para confirmação

    Returns:
        dict: Mensagem de sucesso

    Raises:
        HTTPException 400: Se senha incorreta
    """
    # Verificar senha
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )

    # Deletar usuário
    db.delete(current_user)
    db.commit()

    return {"message": "Conta deletada com sucesso"}
