import os
import uuid
from enum import Enum, auto
from typing import Any, Callable

import logger
from database.user_dao import UserDAO
from flask import jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.token_model import JwtToken


class Types(Enum):
    UUID = auto()
    POS_INT = auto()
    FILE = auto()


def __check_uuid(val: Any) -> uuid.UUID:
    if isinstance(val, uuid.UUID):
        return val
    return uuid.UUID(val)


def __check_pos_int(val: Any) -> int:
    int_ = int(val)
    if int_ < 0:
        raise ValueError(f"{val} is a negative integer")
    return int_


def __check_file(val: Any) -> str:
    root, ext = os.path.splitext(val)
    if root != "" and ext in ["png", "jpg"]:
        return str(val)
    raise ValueError(f"{val} is not a path")


__functions = {Types.UUID: __check_uuid, Types.POS_INT: __check_pos_int, Types.FILE: __check_file}


def check_params(names: dict[str, Types]) -> Callable:
    def decorator(func: Callable[[uuid.UUID], Response]) -> Callable[..., Response]:
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


def needs_login(func: Callable[..., Response]) -> Callable[..., Response]:
    def decorator(*args, **kwargs) -> Response:
        request_user = __get_user_in_request()
        if request_user is None:
            return make_response(
                jsonify({"error": "not logged in"}),
                status.HTTP_401_UNAUTHORIZED,
            )
        kwargs["current_user"] = UserDAO.get_user_by_id(request_user)
        return func(*args, **kwargs)

    return decorator


def needs_logout(func: Callable[..., Response]) -> Callable[..., Response]:
    def decorator(*args, **kwargs) -> Response:
        request_user = __get_user_in_request()
        if request_user:
            return make_response(
                jsonify({"error": "not logged out"}),
                status.HTTP_401_UNAUTHORIZED,
            )
        return func(*args, **kwargs)

    return decorator


def raises(func: Callable) -> Any:
    def decorator(*exceptions: Exception) -> Any:
        def wrapper(*args, **kwargs) -> Any | None:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as ex:
                if ex in exceptions:
                    logger.debug("Uncaught exception in function that might throw exception")
                else:
                    logger.debug(f"Uncaught unexpected exception type {ex}")

            return None

        return wrapper

    return decorator


def log_endpoint(func: Callable[..., Response]) -> Callable[..., Response]:
    def decorator(*args, **kwargs) -> Response:
        try:
            result = func(*args, **kwargs)
        except Exception as ex:
            logger.error(f"In endpoint {request.full_path} - {type(ex)}:{ex}")
            return make_response(
                jsonify({"error": ex.args[0], "type": type(ex)}),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        logger.debug(f"{request.full_path} - {result.status}")
        return result

    return decorator


def __get_user_in_request() -> uuid.UUID | None:
    if "Authorization" not in request.headers:
        return None

    token = JwtToken.from_str(request.headers["Authorization"].removeprefix("Bearer "))
    if not token.is_valid:
        return None
    return token.owner_id
