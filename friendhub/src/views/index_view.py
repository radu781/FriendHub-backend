from uuid import UUID
from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response

from database.post_dao import PostDAO
from database.user_dao import UserDAO

index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/", methods=["GET"])
def index_view() -> Response:
    current_user = UserDAO.get_user_by_id(UUID("ff4df6fb-2ee4-45f8-8e79-bc5d1eedd57c"))
    return make_response(
        render_template(
            "index.html",
            posts=PostDAO.get_visible_posts(current_user.id_),
            user=current_user,
        )
    )
