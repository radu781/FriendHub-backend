import uuid

from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from database.user_dao import UserDAO

profile_blueprint = Blueprint("profile_blueprint", __name__)


@profile_blueprint.route("/api/profile/<string:id>", methods=["GET"])
def profile(id: str) -> Response:
    current_user = UserDAO.get_user_by_id(uuid.UUID(id))
    if not current_user.email:
        return make_response(
            jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND
        )
    return make_response(jsonify({"user": vars(current_user)}))
