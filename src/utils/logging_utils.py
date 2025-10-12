# src/utils/logging_utils.py
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str = "app.log", level=logging.INFO):
    """Set up logging for console + file with rotation."""
    
    # root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # rotating file handler
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Logging initialized. Level=%s, file=%s", logging.getLevelName(level), log_file)
