import uuid
from datetime import date

from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status

from database.activity_dao import ActivityDAO
from database.user_dao import UserDAO
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.validators.decorators import Types, check_params

activity_blueprint = Blueprint("activity_blueprint", __name__)


@activity_blueprint.route("/api/activity/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def search(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)

    today = date.today()
    last_month = today - relativedelta(year=1)

    parser = ArgumentParser(request, {Argument("computed", ArgType.OPTIONAL, "false")})
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )

    activities = ActivityDAO.get_activities(target_user.id_, last_month, today)
    if values["computed"] == "true":
        value = sum(a.score for a in activities)
        level = __badge_level(value)
        return make_response(
            jsonify({"score": value, "level": level, "image": f"assets/icons/badge_{level}.svg"})
        )
    else:
        return make_response(
            jsonify({"count": len(activities), "data": list((vars(act) for act in activities))})
        )


def __badge_level(score: int) -> int:
    if score < 25:
        return 1
    if score < 75:
        return 2
    if score < 150:
        return 3
    if score < 250:
        return 4
    return 5
