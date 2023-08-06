from datetime import date
import uuid
from database.activity_dao import ActivityDAO

from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from flask_api import status
from database.user_dao import UserDAO
from utils.validators.decorators import Types, check_params
from dateutil.relativedelta import relativedelta

activity_blueprint = Blueprint("activity_blueprint", __name__)


@activity_blueprint.route("/api/activity/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def search(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)

    today = date.today()
    last_year = today - relativedelta(years=1)

    activities = ActivityDAO.get_activities(target_user.id_, last_year, today)
    return make_response(
        jsonify({"count": len(activities), "data": list((vars(act) for act in activities))})
    )
