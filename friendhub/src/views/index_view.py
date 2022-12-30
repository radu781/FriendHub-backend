from database.post_dao import PostDAO
from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from utils.session import get_user_in_session

index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/", methods=["GET"])
def index_view() -> Response:
    current_user = get_user_in_session()

    return make_response(
        render_template(
            "index.html",
            posts=PostDAO.get_visible_posts(current_user),
            user=current_user,
        )
    )
