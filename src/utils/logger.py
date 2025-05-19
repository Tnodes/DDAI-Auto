import os
from loguru import logger
from src.config import LOG_DIR
import sys

os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)

logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="INFO"
) 