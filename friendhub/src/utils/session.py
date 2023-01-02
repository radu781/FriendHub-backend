from database.token_dao import TokenDAO
from database.user_dao import UserDAO
from flask import request, session
from models.token_model import Token
from models.user_model import User


def get_user_in_session() -> User | None:
    if Token.Purpose.USER_LOGIN not in session:
        return None

    current_token = TokenDAO.get_token_by_value(session[Token.Purpose.USER_LOGIN])
    if not current_token or not current_token.is_valid:
        return None

    return UserDAO.get_user_by_id(current_token.owner_id)


def get_user_in_request() -> User | None:
    if not "Authorization" in request.headers:
        return None

    current_token = TokenDAO.get_token_by_value(
        request.headers["Authorization"].removeprefix("Bearer ")
    )
    if not current_token or not current_token.is_valid:
        return None

    return UserDAO.get_user_by_id(current_token.owner_id)


def set_session_token(token: Token, purpose: Token.Purpose) -> None:
    session[purpose] = token.value
