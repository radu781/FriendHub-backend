from flask import Blueprint, request, make_response, jsonify
from flask_api import status
from flask.wrappers import Response
from utils.argument_parser import ArgsNotFoundException

from utils.argument_parser import ArgumentParser, Argument, ArgType

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/api-login", methods=["POST"])
def login() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("username", ArgType.Mandatory, None),
            Argument("password", ArgType.Mandatory, None),
        },
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
    return make_response("")
