import random
import string
from typing import Callable

from flask import Response, session


def setup_session(func: Callable[..., Response]) -> Callable[..., Response]:
    def decorator(*args, **kwargs) -> Response:
        if "session_id" not in session:
            session.permanent = True
            session["session_id"] = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
        return func(*args, **kwargs)

    return decorator
