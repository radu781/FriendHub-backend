from datetime import datetime
import random
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
def register() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("email", ArgType.Mandatory, None),
            Argument("password", ArgType.Mandatory, None),
            Argument("password-confirm", ArgType.Mandatory, None),
            Argument("first-name", ArgType.Mandatory, None),
            Argument("middle-name", ArgType.Optional, ""),
            Argument("last-name", ArgType.Optional, ""),
            Argument("country", ArgType.Optional, ""),
            Argument("city", ArgType.Optional, ""),
            Argument("education", ArgType.Optional, ""),
            Argument("extra", ArgType.Optional, ""),
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

    if UserDAO.user_exists(values["email"]):
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
            first_name=values["first-name"],
            middle_name=values["middle-name"],
            last_name=values["last-name"],
            join_time=datetime.now(),
            country=values["country"],
            city=values["city"],
            education=values["education"],
            extra=values["extra"],
            profile_picture=f"assets/images/default_profile_picture/default_profile_picture_{random.randint(1, 10)}.png",
            banner_picture="",
            password=values["password"],
            email=values["email"],
        )
    )
    return make_response("")
