import uuid

from database.script_dao import ScriptDAO
from flask import Blueprint, jsonify, make_response, render_template
from flask.wrappers import Response
from flask_api import status
from utils.validators.decorators import Types, check_params

js_redirect_blueprint = Blueprint("js_redirect_blueprint", __name__)


@js_redirect_blueprint.route("/api/js_runner/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def js_redirect_view(*, id_: uuid.UUID) -> Response:
    script = ScriptDAO.get(id_)
    if script is None:
        return make_response(jsonify({"error": "script not found"}), status.HTTP_404_NOT_FOUND)
    return make_response(render_template("js_runner.html", script=script.code), status.HTTP_200_OK)
