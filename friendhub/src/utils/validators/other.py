import re

from config_keys import DEPLOYING


def check_password(password: str) -> None:
    if not DEPLOYING:
        return
    if not re.match(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', password):
        raise ValueError("incorrect password format")


def check_email(email: str) -> None:
    if not DEPLOYING:
        return
    if not re.match(r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        raise ValueError("incorrect email format")


def check_name(name: str) -> None:
    if not DEPLOYING:
        return
    if not re.match(
        r"^[A-Za-z\x{00C0}-\x{00FF}][A-Za-z\x{00C0}-\x{00FF}\'\-]+"
        r"([\ A-Za-z\x{00C0}-\x{00FF}][A-Za-z\x{00C0}-\x{00FF}\'\-]+)*$",
        name,
    ):
        raise ValueError("incorrect name format")
