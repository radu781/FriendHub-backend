from flask import Blueprint, make_response, render_template
from flask.wrappers import Response

from utils.session import get_user_in_session

settings_base_blueprint = Blueprint("settings_base_blueprint", __name__)


@settings_base_blueprint.route("/settings")
def settings() -> Response:
    current_user = get_user_in_session()
    return make_response(render_template("settings.html", user=current_user))
