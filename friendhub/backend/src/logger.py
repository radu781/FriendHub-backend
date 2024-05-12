import datetime
import enum
import logging
import os
import time
from typing import Any

from flask import has_request_context, request, session

from config_keys import DEBUG_ON

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


class LogCategory(str, enum.Enum):
    DEFAULT = ""
    DB = "DB"
    EMAIL = "EMAIL"

    def __str__(self) -> str:
        return f"[{self.value}] " if self != LogCategory.DEFAULT else ""

    def __repr__(self) -> str:
        return str(self)


if __logger is None:
    __logger = create()

    for file in os.listdir("friendhub/backend/logs"):
        if os.path.isfile(file) and os.path.getsize("file") == 0:
            os.remove(f"friendhub/backend/logs/{file}")


def debug(msg: Any, category: LogCategory = LogCategory.DEFAULT) -> None:
    msg = f"{__log_extra()}{category} {msg}"
    if DEBUG_ON:
        print("[D]" + msg)
    __logger.debug(msg)


def info(msg: Any, category: LogCategory = LogCategory.DEFAULT) -> None:
    msg = f"{__log_extra()}{category} {msg}"
    if DEBUG_ON:
        print("[I]" + msg)
    __logger.info(msg)


def warning(msg: Any, category: LogCategory = LogCategory.DEFAULT) -> None:
    msg = f"{__log_extra()}{category} {msg}"
    if DEBUG_ON:
        print("[W]" + msg)
    __logger.warning(msg)


def error(msg: Any, category: LogCategory = LogCategory.DEFAULT) -> None:
    msg = f"{__log_extra()}{category} {msg}"
    if DEBUG_ON:
        print("[E]" + msg)
    __logger.error(msg)


def critical(msg: Any, category: LogCategory = LogCategory.DEFAULT) -> None:
    msg = f"{__log_extra()}{category} {msg}"
    if DEBUG_ON:
        print("[C]" + msg)
    __logger.critical(msg)


def __log_extra() -> str:
    if not has_request_context():
        return ""
    ip = "unknown"
    if request and request.remote_addr:
        ip = request.remote_addr
    sid = session.get("session_id", "null")
    return f"[{ip}:{sid}]"
