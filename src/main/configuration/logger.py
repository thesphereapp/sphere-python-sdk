import logging
from logging import Logger


def get_logger() -> Logger:
    return logging.getLogger(__name__)