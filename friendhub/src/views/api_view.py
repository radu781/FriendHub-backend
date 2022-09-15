from flask import Blueprint, make_response, render_template
from flask.wrappers import Response

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/api")
def api() -> Response:
    return make_response(render_template("api.html"))
