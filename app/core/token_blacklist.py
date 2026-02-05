# app/core/token_blacklist.py
"""
Token Blacklist Service

Gerencia invalidação de tokens JWT (logout, password change, etc).
Suporta Redis (produção) com fallback para in-memory (desenvolvimento).
"""
import time
from typing import Optional, Set
from datetime import datetime, timedelta
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)


class TokenBlacklist:
    """
    Gerenciador de tokens inválidos (blacklist).

    Prioridade:
    1. Redis (se disponível) - persistente, distribuído
    2. In-memory (fallback) - volátil, apenas single-server

    Uso:
        blacklist = TokenBlacklist()
        blacklist.revoke_token("token_jwt", expires_at=datetime.utcnow() + timedelta(minutes=30))
        if blacklist.is_revoked("token_jwt"):
            raise HTTPException(401, "Token revogado")
    """

    def __init__(self):
        self._redis_client: Optional[object] = None
        self._memory_blacklist: Set[str] = set()
        self._setup_redis()

    def _setup_redis(self):
        """Tenta conectar ao Redis, usa in-memory como fallback"""
        # Verificar se Redis está configurado
        redis_url = getattr(settings, 'REDIS_URL', None)

        if not redis_url:
            logger.warning(
                "REDIS_URL not configured. Using in-memory token blacklist. "
                "This is NOT recommended for production with multiple servers!"
            )
            return

        try:
            import redis

            # Tentar conectar ao Redis
            self._redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )

            # Testar conexão
            self._redis_client.ping()
            logger.info(f"Redis connected successfully: {redis_url}")

        except ImportError:
            logger.error("redis package not installed. Install with: pip install redis")
            self._redis_client = None

        except Exception as e:
            logger.warning(
                f"Failed to connect to Redis: {e}. "
                f"Using in-memory blacklist (not suitable for production)"
            )
            self._redis_client = None

    def revoke_token(self, token: str, expires_at: datetime) -> bool:
        """
        Adiciona token à blacklist até sua expiração natural.

        Args:
            token: Token JWT completo
            expires_at: Quando o token expira naturalmente

        Returns:
            True se adicionado com sucesso
        """
        # Calcular TTL (tempo até expiração)
        ttl_seconds = int((expires_at - datetime.utcnow()).total_seconds())

        if ttl_seconds <= 0:
            # Token já expirou naturalmente, não precisa blacklist
            return True

        # Chave no Redis/memory
        key = f"blacklist:{token}"

        if self._redis_client:
            try:
                # Redis: armazena com TTL automático
                self._redis_client.setex(key, ttl_seconds, "1")
                logger.info(f"Token revoked in Redis (TTL: {ttl_seconds}s)")
                return True

            except Exception as e:
                logger.error(f"Failed to revoke token in Redis: {e}")
                # Fallback para memory
                self._memory_blacklist.add(key)
                return True

        else:
            # In-memory: adiciona à blacklist
            self._memory_blacklist.add(key)
            logger.debug(f"Token revoked in memory (TTL: {ttl_seconds}s)")

            # Agendar limpeza (simples, sem threading)
            # Em produção, use Redis ou background task
            self._schedule_cleanup(key, ttl_seconds)
            return True

    def is_revoked(self, token: str) -> bool:
        """
        Verifica se token está na blacklist.

        Args:
            token: Token JWT completo

        Returns:
            True se token foi revogado
        """
        key = f"blacklist:{token}"

        if self._redis_client:
            try:
                # Redis: verificar se chave existe
                return bool(self._redis_client.exists(key))

            except Exception as e:
                logger.error(f"Failed to check Redis blacklist: {e}")
                # Fallback para memory
                return key in self._memory_blacklist

        else:
            # In-memory: verificar set
            return key in self._memory_blacklist

    def revoke_all_user_tokens(self, user_id: int, current_token_exp: datetime) -> bool:
        """
        Revoga TODOS os tokens de um usuário (ex: ao mudar senha).

        Nota: Implementação simplificada. Em produção real, use:
        - Redis SET para armazenar "user:{user_id}:token_version"
        - Incrementar versão ao mudar senha
        - Verificar versão no token vs Redis

        Args:
            user_id: ID do usuário
            current_token_exp: Expiração do token atual (para TTL)

        Returns:
            True se marcado para revogação
        """
        key = f"user_revoked:{user_id}"
        ttl_seconds = int((current_token_exp - datetime.utcnow()).total_seconds())

        if ttl_seconds <= 0:
            return True

        if self._redis_client:
            try:
                # Armazena timestamp de revogação
                self._redis_client.setex(
                    key,
                    ttl_seconds,
                    str(int(time.time()))
                )
                logger.info(f"All tokens revoked for user {user_id}")
                return True

            except Exception as e:
                logger.error(f"Failed to revoke user tokens: {e}")
                return False

        else:
            # In-memory: marcar usuário
            self._memory_blacklist.add(key)
            self._schedule_cleanup(key, ttl_seconds)
            return True

    def is_user_revoked(self, user_id: int, token_issued_at: datetime) -> bool:
        """
        Verifica se todos os tokens do usuário foram revogados.

        Args:
            user_id: ID do usuário
            token_issued_at: Quando o token foi emitido (claim 'iat')

        Returns:
            True se tokens do usuário foram revogados após emissão deste token
        """
        key = f"user_revoked:{user_id}"

        if self._redis_client:
            try:
                revoked_at_str = self._redis_client.get(key)
                if not revoked_at_str:
                    return False

                revoked_at = int(revoked_at_str)
                token_issued_ts = int(token_issued_at.timestamp())

                # Se revogação foi DEPOIS da emissão do token, token é inválido
                return revoked_at > token_issued_ts

            except Exception as e:
                logger.error(f"Failed to check user revocation: {e}")
                return False

        else:
            # In-memory simplificado: se key existe, considera revogado
            return key in self._memory_blacklist

    def _schedule_cleanup(self, key: str, delay_seconds: int):
        """
        Agenda remoção da blacklist in-memory após TTL.

        Nota: Implementação simplificada. Em produção use:
        - Background task com asyncio
        - Ou Redis que faz isso automaticamente
        """
        # Em produção, use asyncio.create_task ou background worker
        # Por agora, apenas loga (limpeza será feita na próxima verificação)
        pass

    def clear_expired(self):
        """
        Remove tokens expirados da blacklist in-memory.

        Deve ser chamado periodicamente por background task.
        Redis faz isso automaticamente via TTL.
        """
        if self._redis_client:
            # Redis já limpa automaticamente
            return

        # In-memory: não temos como saber quais expiraram
        # Em produção, armazene tupla (key, expires_at)
        # Por agora, aceite que memory cresce até restart
        logger.debug(f"In-memory blacklist size: {len(self._memory_blacklist)}")

    def get_stats(self) -> dict:
        """Retorna estatísticas da blacklist"""
        if self._redis_client:
            try:
                # Contar chaves blacklist:* no Redis
                keys = self._redis_client.keys("blacklist:*")
                user_keys = self._redis_client.keys("user_revoked:*")

                return {
                    "backend": "redis",
                    "tokens_revoked": len(keys),
                    "users_revoked": len(user_keys),
                    "redis_connected": True
                }

            except Exception as e:
                logger.error(f"Failed to get Redis stats: {e}")
                return {
                    "backend": "redis",
                    "error": str(e),
                    "redis_connected": False
                }

        else:
            return {
                "backend": "memory",
                "tokens_revoked": len(self._memory_blacklist),
                "warning": "In-memory blacklist not suitable for production!"
            }


# Singleton global
_blacklist_instance: Optional[TokenBlacklist] = None


def get_token_blacklist() -> TokenBlacklist:
    """
    Retorna instância singleton do TokenBlacklist.

    Usage:
        from app.core.token_blacklist import get_token_blacklist

        blacklist = get_token_blacklist()
        blacklist.revoke_token(token, expires_at)
    """
    global _blacklist_instance

    if _blacklist_instance is None:
        _blacklist_instance = TokenBlacklist()

    return _blacklist_instance
