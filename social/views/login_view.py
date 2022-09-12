from flask import Blueprint, make_response, request, jsonify, render_template
from flask.wrappers import Response

login_view_blueprint = Blueprint("login_view_blueprint", __name__)


@login_view_blueprint.route("/login", methods=["GET"])
def login_view() -> Response:
    return make_response(render_template("login.html"))
