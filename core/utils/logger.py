import sys
from loguru import logger
from core.utils.path_manager import PathManager

def setup_logging(level="INFO"):
    """
    Configures loguru for structured logging.
    """
    # Remove default handler
    logger.remove()
    
    # Add stdout handler with custom format
    logger.add(
        sys.stdout, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level
    )
    
    # Add file handler for persistence
    log_file = PathManager.LOGS / "sovereign_ai.log"
    logger.add(
        log_file,
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level
    )
    
    return logger

# Default logger instance
sovereign_logger = setup_logging()
