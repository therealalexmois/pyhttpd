"""Настройка журналирования."""

import logging

from pyhttpd.config import LOG_FILE, LOG_LEVEL


def setup_logger() -> logging.Logger:
    """Устанавливает конфигурацию протоколирования для веб-сервера."""
    logger = logging.getLogger('pyhttpd')
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
