from flask import Blueprint, make_response, render_template
from flask.wrappers import Response

from utils.session import get_user_in_session

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/api")
def api() -> Response:
    current_user = get_user_in_session()
    return make_response(render_template("api.html", user=current_user))
