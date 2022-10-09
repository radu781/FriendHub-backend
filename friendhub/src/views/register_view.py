from flask import Blueprint, make_response, render_template
from flask.wrappers import Response

register_view_blueprint = Blueprint("register_view_blueprint", __name__)


@register_view_blueprint.route("/register", methods=["GET"])
def register_view() -> Response:
    return make_response(render_template("register.html"))
