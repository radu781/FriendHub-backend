import random
from datetime import datetime
from uuid import uuid4

import utils.validators.other as validators
from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request, session
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from utils.argument_parser import *
from utils.validators.decorators import needs_logout

register_blueprint = Blueprint("register_blueprint", __name__)


@register_blueprint.route("/api/register", methods=["POST"])
@needs_logout
def register() -> Response:
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
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        validators.check_email(values["email"])
        validators.check_password(values["password"])
        validators.check_name(values["first-name"])
        if values["middle-name"] != "":
            validators.check_name(values["middle-name"])
        if values["last-name"] != "":
            validators.check_name(values["last-name"])
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
