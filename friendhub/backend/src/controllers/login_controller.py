from datetime import datetime, timedelta
from uuid import uuid4

from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status

from database.dao.login_location_dao import LoginLocationDAO
import logger
from database.token_dao import TokenDAO
from database.user_dao import UserDAO
from invoke.email import Email, Location
from models.token_model import JwtToken
from models.user_model import User
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.session import setup_session
from utils.validators.decorators import log_endpoint, needs_logout

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/api/login", methods=["POST"])
@setup_session
@log_endpoint
@needs_logout
def login() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("email", ArgType.MANDATORY, None),
            Argument("password", ArgType.MANDATORY, None),
        },
        Method.POST,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
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
    logger.debug(str(vars(current_user)))

    if not current_user:
        return make_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    current_token = JwtToken(
        owner_id=current_user.id_,
        valid_until=datetime.now() + timedelta(14),
        purpose=JwtToken.Purpose.USER_LOGIN,
    ).build()
    TokenDAO.insert(current_token)

    # if not LoginLocationDAO.known_ip(request.remote_addr):
    loc = Location(request.remote_addr)
    loc.new(current_user)
    Email.new_login(current_user.email, current_user.first_name, loc)

    return make_response(jsonify({"token": current_token}), status.HTTP_200_OK)
