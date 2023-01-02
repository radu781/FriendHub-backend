import uuid

from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from utils.validators.decorators import Types, check_params

profile_blueprint = Blueprint("profile_blueprint", __name__)


@profile_blueprint.route("/api/profile/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def profile(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)
    return make_response(jsonify({"user": vars(target_user.sanitize())}))
