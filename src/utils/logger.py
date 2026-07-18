import logging
import sys
import structlog
from pathlib import Path
from config.config import Config

_logger_configured = False


def configure_structlog():
    global _logger_configured
    if _logger_configured:
        return

    # Create logs directory
    Path(Config.LOG_DIR).mkdir(parents=True, exist_ok=True)

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    )

    # Add file handler
    file_handler = logging.FileHandler(Config.LOG_DIR / "app.log", encoding="utf-8")
    logging.getLogger().addHandler(file_handler)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    _logger_configured = True


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Create and return a configured structlog logger.
    """
    configure_structlog()
    return structlog.get_logger(name)
