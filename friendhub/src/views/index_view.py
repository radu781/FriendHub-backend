from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response

index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/", methods=["GET"])
def index_view() -> Response:
    return make_response(render_template("index.html"))
