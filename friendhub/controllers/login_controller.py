from datetime import datetime
from uuid import uuid4

from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from database.user_dao import UserDAO
from utils.argument_parser import Method
from utils.argument_parser import (
    ArgsNotFoundException,
    ArgType,
    Argument,
    ArgumentParser,
)

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/api-login", methods=["POST"])
def login() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("username", ArgType.Mandatory, None),
            Argument("password", ArgType.Mandatory, None),
        },
        Method.Post,
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
        email=values["username"],
        password=values["password"],
        join_time=datetime.now(),
    )

    if not UserDAO.user_exists(current_user.email):
        return make_response(
            jsonify({"reason": "user does not exist"}), status.HTTP_401_UNAUTHORIZED
        )

    if not UserDAO.correct_password(current_user.email, current_user.password):
        return make_response(
            jsonify({"reason": "incorrect password"}), status.HTTP_401_UNAUTHORIZED
        )

    return make_response("")
