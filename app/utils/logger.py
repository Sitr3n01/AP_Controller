"""
Sistema de logging centralizado usando Loguru.
Logs técnicos em inglês, mensagens de usuário em português.
"""
import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_level: str = "INFO", app_name: str = "Sentinel") -> None:
    """
    Configura o logger da aplicação.

    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        app_name: Nome da aplicação para o arquivo de log
    """
    # Remove handlers padrão do loguru
    logger.remove()

    # Console handler - formatação colorida e legível
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # File handler - logs rotacionados diariamente
    log_path = Path("data/logs")
    log_path.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path / f"{app_name.lower()}_{{time:YYYY-MM-DD}}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="00:00",  # Nova arquivo à meia-noite
        retention="30 days",  # Mantém logs por 30 dias
        compression="zip",  # Comprime logs antigos
        encoding="utf-8",
    )

    # File handler para erros - arquivo separado
    logger.add(
        log_path / f"{app_name.lower()}_errors_{{time:YYYY-MM-DD}}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        level="ERROR",
        rotation="00:00",
        retention="90 days",  # Mantém logs de erro por mais tempo
        compression="zip",
        encoding="utf-8",
        backtrace=True,  # Inclui traceback completo
        diagnose=True,  # Informações de diagnóstico detalhadas
    )

    logger.info(f"Logger initialized - Level: {log_level}, App: {app_name}")


def get_logger(name: str = None):
    """
    Retorna uma instância do logger.

    Args:
        name: Nome do módulo/componente (opcional)

    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger


# Logger padrão da aplicação
app_logger = logger
