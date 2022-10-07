from flask import Blueprint, make_response, render_template, session
from flask.wrappers import Response

from database.post_dao import PostDAO
from database.token_dao import TokenDAO
from database.user_dao import UserDAO
from models.token_model import Token
from models.user_model import User

index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/", methods=["GET"])
def index_view() -> Response:
    if not Token.Purpose.USER_LOGIN in session:
        current_user = User()
    else:
        current_token = TokenDAO.get_token_by_value(session[Token.Purpose.USER_LOGIN])
        if not current_token or not current_token.is_valid:
            current_user = None
        else:
            current_user = UserDAO.get_user_by_id(current_token.owner_id)
    return make_response(
        render_template(
            "index.html",
            posts=PostDAO.get_visible_posts(),
            user=current_user,
        )
    )
