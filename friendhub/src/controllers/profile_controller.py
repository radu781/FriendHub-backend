import uuid

from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from database.user_dao import UserDAO

profile_blueprint = Blueprint("profile_blueprint", __name__)


@profile_blueprint.route("/api/profile/<string:id_>", methods=["GET"])
def profile(id_: str) -> Response:
    try:
        target_user = UserDAO.get_user_by_id(uuid.UUID(id_))
    except ValueError:
        return make_response(
            jsonify({"reason": "given id is not a UUID", "id": id_}),
            status.HTTP_400_BAD_REQUEST,
        )
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)
    return make_response(jsonify({"user": vars(target_user.sanitize())}))
