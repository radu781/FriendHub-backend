import uuid

from config_keys import DELETE_PROFILE_KEY
from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.validators.decorators import Types, check_params

delete_user_blueprint = Blueprint("delete_user_blueprint", __name__)


@delete_user_blueprint.route("/api/profile/<string:id_>", methods=["DELETE"])
@check_params({"id_": Types.UUID})
def delete_user(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)
    parser = ArgumentParser(
        request,
        {
            Argument("key", ArgType.MANDATORY, None),
        },
        Method.POST,
    )
    try:
        values = parser.get_values()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_401_UNAUTHORIZED,
        )

    if values["key"] != DELETE_PROFILE_KEY:
        return make_response(
            jsonify({"reason": "incorrect profile deletion key"}),
            status.HTTP_403_FORBIDDEN,
        )

    UserDAO.delete_user(id_)

    return make_response("")
