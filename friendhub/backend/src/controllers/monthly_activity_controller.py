import uuid

from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from database.user_dao import UserDAO
from utils.validators.decorators import Types, check_params
from database.dao.users_activity_dao import UsersActivityDAO
from flask import request
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from database.objects.users_activity import UsersActivity

monthly_activity_blueprint = Blueprint("monthly_activity_blueprint", __name__)


@monthly_activity_blueprint.route("/api/monthly/<string:id_>", methods=["GET", "PUT"])
@check_params({"id_": Types.UUID})
def find_online_activity(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)

