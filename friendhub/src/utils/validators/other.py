import os
import re
import uuid
from datetime import datetime

from config_keys import DEPLOYING


def check_password(password: str, *, force_validation: bool = False) -> None:
    if not force_validation and not DEPLOYING:
        return
    if not re.match(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', password):
        raise ValueError("incorrect password format")


def check_email(email: str, *, force_validation: bool = False) -> None:
    if not force_validation and not DEPLOYING:
        return
    if not re.match(r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        raise ValueError("incorrect email format")


def check_name(name: str, *, force_validation: bool = False) -> None:
    if not force_validation and not DEPLOYING:
        return
    if not re.match(r"^[A-Z][a-z]+$", name):
        raise ValueError("incorrect name format")


def is_datetime(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        return True
    except ValueError:
        return False


def is_uuid(uuid_: str) -> bool:
    try:
        uuid.UUID(uuid_)
        return True
    except ValueError:
        return False


def __is_path(path: str) -> bool:
    return os.path.exists("friendhub/static/" + path)


def is_image_path(path: str | None) -> bool:
    if path is None:
        return False
    return __is_path(path) and not not re.match(r"^.*\.(jpg|png|jpeg)$", path)


def is_video_path(path: str | None) -> bool:
    if path is None:
        return False
    return __is_path(path) and not not re.match(r"^.*\.(mp4|mkv)$", path)


def is_audio_path(path: str | None) -> bool:
    if path is None:
        return False
    return __is_path(path) and not not re.match(r"^.*\.(mp3|wav)$", path)
