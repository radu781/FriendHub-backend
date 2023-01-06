from database.token_dao import TokenDAO
from flask import Blueprint, jsonify, make_response, request, session
from flask.wrappers import Response
from flask_api import status
from models.token_model import Token
from utils.session import get_user_in_request

logout_blueprint = Blueprint("logout_blueprint", __name__)


@logout_blueprint.route("/api/logout", methods=["POST"])
def logout() -> Response:
    if Token.Purpose.USER_LOGIN not in session:
        return make_response(jsonify({"error": "already logged out"}), status.HTTP_400_BAD_REQUEST)
    if "Authorization" in request.headers:
        user = get_user_in_request()
        if not user:
            return make_response(
                jsonify({"error": "already logged out"}), status.HTTP_400_BAD_REQUEST
            )

    current_token = TokenDAO.get_token_by_value(session[Token.Purpose.USER_LOGIN])
    if not current_token:
        del session[Token.Purpose.USER_LOGIN]
        return make_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not current_token.is_valid:
        del session[Token.Purpose.USER_LOGIN]
        return make_response(jsonify({"error": "token was invalid"}), status.HTTP_400_BAD_REQUEST)

    TokenDAO.invalidate(current_token)
    del session[Token.Purpose.USER_LOGIN]
    return make_response()
