from flask import Blueprint, make_response, request
from flask.wrappers import Response
from models.user_model import User
from utils.validators.decorators import needs_login

settings_blueprint = Blueprint("settings_blueprint", __name__)


@settings_blueprint.route("/api/settings", methods=["GET", "POST"])
@needs_login
def settings(*, current_user: User) -> Response:
    if request.method == "GET":
        return make_response({"userPreferences": None})

    return make_response(request.json)
