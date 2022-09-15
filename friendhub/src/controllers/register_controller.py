from datetime import datetime
from uuid import uuid4

from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from utils.argument_parser import (
    ArgsNotFoundException,
    ArgType,
    Argument,
    ArgumentParser,
    Method,
)

register_blueprint = Blueprint("register_blueprint", __name__)


@register_blueprint.route("/api/register", methods=["POST"])
def login() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("username", ArgType.Mandatory, None),
            Argument("password", ArgType.Mandatory, None),
            Argument("password-confirm", ArgType.Mandatory, None),
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

    if UserDAO.user_exists(values["username"]):
        return make_response(
            jsonify({"reason": "user already exists"}), status.HTTP_401_UNAUTHORIZED
        )
    if values["password"] != values["password-confirm"]:
        return make_response(
            jsonify({"reason": "passwords mismatch"}), status.HTTP_401_UNAUTHORIZED
        )

    UserDAO.register_user(
        User(
            id_=uuid4(),
            email=values["username"],
            password=values["password"],
            join_time=datetime.now(),
        )
    )
    return make_response("")
