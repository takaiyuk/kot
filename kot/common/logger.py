import logging
import sys
from typing import Any


class Logger:
    def __init__(self) -> None:
        self.logger = self._get_logger()

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
        return logger

    def info(self, message: Any) -> None:
        self.logger.info(message)

    def warning(self, message: Any) -> None:
        self.logger.warning(message)

    def error(self, message: Any) -> None:
        self.logger.error(message)


logger = Logger()
