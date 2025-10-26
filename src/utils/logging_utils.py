import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logging(
    log_file: str = "app.log",
    level: int = logging.INFO,
    logger_name: Optional[str] = None,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5
):
    """
    Set up logging with console + rotating file handlers.

    Args:
        log_file: Path to log file.
        level: Logging level (e.g., logging.INFO).
        logger_name: Name of the logger. If None, root logger is used.
        max_bytes: Maximum size of log file before rotation.
        backup_count: Number of backup log files to keep.
    """
    # Get logger (root if logger_name is None)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False  # prevent double logging if root also logs

    # Remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(
        "Logging initialized. Logger=%s, Level=%s, File=%s",
        logger_name or "root",
        logging.getLevelName(level),
        log_file,
    )

    return logger
