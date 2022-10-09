import json
from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from controllers.profile_controller import profile
from models.user_model import User
from flask_api import status

profile_view_blueprint = Blueprint("profile_view_blueprint", __name__)


@profile_view_blueprint.route("/profile/<string:id_>", methods=["GET"])
def profile_view(id_: str) -> Response:
    res = profile(id_)
    if res.status_code == status.HTTP_404_NOT_FOUND:
        return make_response(render_template("profile.html", user=None))

    target_user = User.from_dict(json.loads(res.data)["user"])
    return make_response(render_template("profile.html", user=target_user))
