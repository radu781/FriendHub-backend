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

online_activity_blueprint = Blueprint("online_activity_blueprint", __name__)


@online_activity_blueprint.route("/api/online_activity/<string:id_>", methods=["GET", "PUT"])
@check_params({"id_": Types.UUID})
def find_online_activity(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        online_status = UsersActivityDAO.get(target_user.id_)
        return make_response(jsonify({"activity": vars(online_status)}), status.HTTP_200_OK)

    else:
        parser = ArgumentParser(request, {Argument("status", ArgType.MANDATORY, None)}, Method.PUT)
        try:
            values = parser.parse()
        except ArgsNotFoundException as ex:
            return make_response(
                jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
                status.HTTP_401_UNAUTHORIZED,
            )
        if values["status"] not in UsersActivity.Activity.values():
            return make_response(
                jsonify(
                    {
                        "reason": f"unknown activity status '{values['status']}'",
                        "supported": list(UsersActivity.Activity.values()),
                    }
                ),
                status.HTTP_400_BAD_REQUEST,
            )
        UsersActivityDAO.update(
            target_user.id_,
            UsersActivity.Activity(values["status"]),
            request.user_agent.string,
            request.remote_addr if request.remote_addr is not None else "???",
        )
        return make_response("", status.HTTP_200_OK)
