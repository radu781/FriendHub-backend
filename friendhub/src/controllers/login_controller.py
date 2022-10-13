from datetime import datetime, timedelta
from uuid import uuid4

from database.token_dao import TokenDAO
from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request, session
from flask.wrappers import Response
from flask_api import status
from models.token_model import Token
from models.user_model import User
from utils.argument_parser import (
    ArgsNotFoundException,
    ArgType,
    Argument,
    ArgumentParser,
    Method,
)

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/api/login", methods=["POST"])
def login() -> Response:
    session.permanent = True
    parser = ArgumentParser(
        request,
        {
            Argument("email", ArgType.MANDATORY, None),
            Argument("password", ArgType.MANDATORY, None),
        },
        Method.POST,
    )
    try:
        values = parser.get_values()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify(
                {"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}
            ),
            status.HTTP_401_UNAUTHORIZED,
        )

    current_user = User(
        id_=uuid4(),
        email=values["email"],
        password=values["password"],
        join_time=datetime.now(),
    )

    if not UserDAO.user_exists(current_user.email):
        return make_response(
            jsonify({"reason": "user does not exist"}), status.HTTP_401_UNAUTHORIZED
        )

    if not current_user.password:
        return make_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not UserDAO.correct_password(current_user.email, current_user.password):
        return make_response(
            jsonify({"reason": "incorrect password"}), status.HTTP_401_UNAUTHORIZED
        )
    current_user = UserDAO.get_user_by_email(values["email"])

    if not current_user:
        return make_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    current_token = Token(
        owner_id=current_user.id_,
        valid_until=datetime.now() + timedelta(14),
        purpose=Token.Purpose.USER_LOGIN,
    )
    TokenDAO.add(current_token)
    session[Token.Purpose.USER_LOGIN] = current_token.value
    return make_response(jsonify({"token": vars(current_token)}))
