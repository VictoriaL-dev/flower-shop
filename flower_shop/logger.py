import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings


def setup_logging(level=logging.INFO, log_filename="app.log", max_bytes=10*1024*1024, backup_count=5):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(format=log_format, level=level)

    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)


setup_logging(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    log_filename=settings.LOG_FILENAME,
    max_bytes=settings.LOG_MAX_BYTES,
    backup_count=settings.LOG_BACKUP_COUNT,
)
