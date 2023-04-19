from database.token_dao import TokenDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.token_model import JwtToken

logout_blueprint = Blueprint("logout_blueprint", __name__)


@logout_blueprint.route("/api/logout", methods=["POST"])
def logout() -> Response:
    if "Authorization" not in request.headers:
        return make_response(jsonify({"error": "already logged out"}), status.HTTP_400_BAD_REQUEST)
    token = JwtToken.from_str(request.headers["Authorization"].removeprefix("Bearer "))
    TokenDAO.invalidate(token.build())
    return make_response()
