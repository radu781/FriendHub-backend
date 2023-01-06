import datetime
import logging
import os
import time

from flask import request

__logger: logging.Logger | None = None


def create() -> logging.Logger:
    try:
        os.mkdir("friendhub/logs")
    except FileExistsError:
        pass

    dt = datetime.datetime.fromtimestamp(time.time())
    logger = logging.getLogger("friendhub")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s"
    )

    file_handler = logging.FileHandler(
        f"friendhub/logs/{dt.isoformat().replace(':', '-')}.log", encoding="utf-16"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


if __logger is None:
    __logger = create()

    for file in os.listdir("friendhub/logs"):
        if os.path.isfile(file) and os.path.getsize("file") == 0:
            os.remove(f"friendhub/logs/{file}")


def __ip() -> str:
    if request and request.remote_addr:
        return request.remote_addr
    return "unknown"


def debug(msg: str) -> None:
    __logger.debug(f"({__ip()}){msg}")  # pylint: disable=logging-fstring-interpolation


def info(msg: str) -> None:
    __logger.info(f"({__ip()}){msg}")  # pylint: disable=logging-fstring-interpolation


def warning(msg: str) -> None:
    __logger.warning(f"({__ip()}){msg}")  # pylint: disable=logging-fstring-interpolation


def error(msg: str) -> None:
    __logger.error(f"({__ip()}){msg}")  # pylint: disable=logging-fstring-interpolation


def critical(msg: str) -> None:
    __logger.critical(f"({__ip()}){msg}")  # pylint: disable=logging-fstring-interpolation
