import datetime
import logging
import os
import time

from flask import request, session

__logger: logging.Logger | None = None


def create() -> logging.Logger:
    try:
        os.mkdir("friendhub/backend/logs")
    except FileExistsError:
        pass

    dt = datetime.datetime.fromtimestamp(time.time())
    logger = logging.getLogger("friendhub")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s"
    )

    file_handler = logging.FileHandler(
        f"friendhub/backend/logs/{dt.isoformat().replace(':', '-')}.log", encoding="utf-16"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


if __logger is None:
    __logger = create()

    for file in os.listdir("friendhub/backend/logs"):
        if os.path.isfile(file) and os.path.getsize("file") == 0:
            os.remove(f"friendhub/backend/logs/{file}")


def debug(msg: str) -> None:
    __logger.debug(__log_extra() + msg)


def info(msg: str) -> None:
    __logger.info(__log_extra() + msg)


def warning(msg: str) -> None:
    __logger.warning(__log_extra() + msg)


def error(msg: str) -> None:
    __logger.error(__log_extra() + msg)


def critical(msg: str) -> None:
    __logger.critical(__log_extra() + msg)


def __log_extra() -> str:
    ip = "unknown"
    if request and request.remote_addr:
        ip = request.remote_addr
    sid = session.get("session_id", "null")
    return f"[{ip}:{sid}]"
