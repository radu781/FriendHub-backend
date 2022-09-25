import json
import uuid
from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response
from controllers.profile_controller import profile
from models.user_model import User

profile_view_blueprint = Blueprint("profile_view_blueprint", __name__)


@profile_view_blueprint.route("/profile/<string:id>", methods=["GET"])
def profile_view(id: str) -> Response:
    res = profile(id)
    if not "user" in json.loads(res.data):
        return make_response(render_template("profile.html", user=None))

    target_user = User.from_dict(json.loads(res.data)["user"])
    return make_response(render_template("profile.html", user=target_user))
