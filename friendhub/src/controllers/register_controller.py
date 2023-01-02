import random
from datetime import datetime
from uuid import uuid4

from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request, session
from flask.wrappers import Response
from flask_api import status
from models.token_model import Token
from models.user_model import User
from utils import validators
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method

register_blueprint = Blueprint("register_blueprint", __name__)


@register_blueprint.route("/api/register", methods=["POST"])
def register() -> Response:
    if Token.Purpose.USER_LOGIN in session:
        return make_response(jsonify({"reason": "logged in"}), status.HTTP_403_FORBIDDEN)

    parser = ArgumentParser(
        request,
        {
            Argument("email", ArgType.MANDATORY, None),
            Argument("password", ArgType.MANDATORY, None),
            Argument("password-confirm", ArgType.MANDATORY, None),
            Argument("first-name", ArgType.MANDATORY, None),
            Argument("middle-name", ArgType.OPTIONAL, ""),
            Argument("last-name", ArgType.OPTIONAL, ""),
            Argument("country", ArgType.OPTIONAL, ""),
            Argument("city", ArgType.OPTIONAL, ""),
            Argument("education", ArgType.OPTIONAL, ""),
            Argument("extra", ArgType.OPTIONAL, ""),
        },
        Method.POST,
    )
    try:
        values = parser.get_values()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_401_UNAUTHORIZED,
        )
    try:
        validators.validate_email(values["email"])
        validators.validate_password(values["password"])
    except ValueError as ex:
        return make_response(
            jsonify({"reason": "one of the inputs has an incorrect format", "error": ex.args[0]}),
            status.HTTP_400_BAD_REQUEST,
        )

    if UserDAO.user_exists(values["email"]):
        return make_response(
            jsonify({"reason": "user already exists"}), status.HTTP_401_UNAUTHORIZED
        )
    if values["password"] != values["password-confirm"]:
        return make_response(
            jsonify({"reason": "passwords mismatch"}), status.HTTP_401_UNAUTHORIZED
        )

    DEFAULT_PROFILE_PICTURE = "assets/images/default_profile_picture/default_profile_picture"
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
            profile_picture=f"{DEFAULT_PROFILE_PICTURE}_{random.randint(1, 10)}.png",
            banner_picture="",
            password=values["password"],
            email=values["email"],
        )
    )
    return make_response("")
