import re
import uuid
from enum import Enum, auto
from typing import Callable

from flask import jsonify, make_response
from flask.wrappers import Response
from flask_api import status


class Types(Enum):
    UUID = auto()
    POS_Int = auto()


def __check_uuid(val) -> uuid.UUID:
    return uuid.UUID(val)


def __check_pos_int(val) -> int:
    try:
        int_ = int(val)
    except ValueError:
        raise
    if int_ < 0:
        raise ValueError(f"{val} is a negative integer")
    return int_


__functions = {Types.UUID: __check_uuid, Types.POS_Int: __check_pos_int}


def check_params(names: dict[str, Types]) -> Callable:
    def decorator(endpoint: Callable[[uuid.UUID], Response]) -> Callable[[], Response]:
        def wrapper(**kwargs) -> Response:
            for key in names:
                type_ = names[key]
                try:
                    current_value = __functions[type_](kwargs[key])
                except ValueError as ex:
                    key_no_suf = key.removesuffix("_")
                    return make_response(
                        jsonify(
                            {
                                "reason": f"given '{key_no_suf}' is not a {type_.name}",
                                "error": ex.args[0],
                                f"{key_no_suf}": kwargs[key],
                            }
                        ),
                        status.HTTP_400_BAD_REQUEST,
                    )
                kwargs[key] = current_value

            return endpoint(*kwargs.values())

        return wrapper

    return decorator


def validate_password(password: str) -> None:
    if not re.match("", password):
        raise ValueError("incorrect password format")


def validate_email(email: str) -> None:
    if not re.match("", email):
        raise ValueError("incorrect email format")
