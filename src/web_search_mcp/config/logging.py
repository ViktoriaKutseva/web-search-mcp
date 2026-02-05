import sys
from loguru import logger
from web_search_mcp.config.settings import settings

def configure_logging():
    """
    Configure application logging using loguru.
    """
    logger.remove()  # Remove default handler
    
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
