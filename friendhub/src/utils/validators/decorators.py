import uuid
from enum import Enum, auto
from typing import Any, Callable

from flask import jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from utils.session import get_user_in_request, get_user_in_session


class Types(Enum):
    UUID = auto()
    POS_INT = auto()


def __check_uuid(val: Any) -> uuid.UUID:
    if isinstance(val, uuid.UUID):
        return val
    return uuid.UUID(val)


def __check_pos_int(val: Any) -> int:
    try:
        int_ = int(val)
    except ValueError:
        raise
    if int_ < 0:
        raise ValueError(f"{val} is a negative integer")
    return int_


__functions = {Types.UUID: __check_uuid, Types.POS_INT: __check_pos_int}


def check_params(names: dict[str, Types]) -> Callable:
    def decorator(func: Callable[[uuid.UUID], Response]) -> Callable[[], Response]:
        def wrapper(*args, **kwargs) -> Response:
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

            return func(*args, **kwargs)

        return wrapper

    return decorator


def needs_login(func: Callable) -> Callable[[], Response]:
    def decorator(*args, **kwargs) -> Response:
        session_user = get_user_in_session()
        request_user = get_user_in_request()
        if session_user is None and request_user is None:
            return make_response(
                jsonify({"error": "not logged in"}),
                status.HTTP_401_UNAUTHORIZED,
            )
        if session_user and request_user and session_user != request_user:
            return make_response(
                jsonify(
                    {
                        "error": "different user IDs in session and bearer token",
                        "session": session_user.id_,
                        "token": request_user.id_,
                        "action": "clear cookies",
                    },
                    status.HTTP_401_UNAUTHORIZED,
                )
            )
        if session_user is None:
            session_user = request_user
        kwargs["current_user"] = session_user
        return func(*args, **kwargs)

    return decorator


def needs_logout(func: Callable) -> Callable[[], Response]:
    def decorator(*args, **kwargs) -> Response:
        session_user = get_user_in_session()
        request_user = get_user_in_request()
        if session_user and request_user:
            return make_response(
                jsonify({"error": "not logged out"}),
                status.HTTP_401_UNAUTHORIZED,
            )
        if session_user or request_user:
            if session_user:
                return make_response(
                    jsonify({"error": "not logged out", "action": "clear session cookies"})
                )
            return make_response(
                jsonify({"error": "not logged out", "action": "clear bearer token or cookies"})
            )
        return func(*args, **kwargs)

    return decorator
