import json
import uuid

from controllers.profile_controller import profile
from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from utils.session import get_user_in_session
from utils.validators.decorators import Types, check_params

profile_view_blueprint = Blueprint("profile_view_blueprint", __name__)


@profile_view_blueprint.route("/profile/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def profile_view(*, id_: uuid.UUID) -> Response:
    res = profile(id_=id_)
    if res.status_code == status.HTTP_404_NOT_FOUND:
        return make_response(render_template("profile.html", user=None))

    target_user = User.from_dict(json.loads(res.data)["user"])
    return make_response(
        render_template("profile.html", target_user=target_user, user=get_user_in_session())
    )
