
from flask import Blueprint, make_response
from flask.wrappers import Response

settings_blueprint = Blueprint("settings_blueprint", __name__)


@settings_blueprint.route("/api/settings/<string:category>", methods=["POST"])
def settings(category:str) -> Response:
    return make_response()
