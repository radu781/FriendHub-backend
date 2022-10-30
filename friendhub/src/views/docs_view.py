from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from utils.session import get_user_in_session

docs_blueprint = Blueprint("docs_blueprint", __name__)


@docs_blueprint.route("/docs")
def api() -> Response:
    current_user = get_user_in_session()
    return make_response(render_template("docs.html", user=current_user))
