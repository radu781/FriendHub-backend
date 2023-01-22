import json

from controllers.all_posts_controller import all_posts
from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from utils.session import get_user_in_session
from models.post_wrapper import PostWrapper
from models.user_model import User
from models.post_model import Post
from models.vote_model import Vote

index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/", methods=["GET"])
def index_view() -> Response:
    current_user = get_user_in_session()
    posts = all_posts(current_user=current_user)
    if posts.status_code >= 400:
        return make_response(render_template("index.html", posts=None, user=current_user))
    resp_json = json.loads(posts.data)
    ui_posts: list[PostWrapper] = []
    for post_wrapper in resp_json["data"]:
        post = post_wrapper["post"]
        user = post_wrapper["author"]
        vote = post_wrapper["vote"]
        ui_posts.append(
            PostWrapper(Post(**post), User(**user), None if vote is None else Vote(**vote))
        )
    return make_response(
        render_template(
            "index.html",
            posts=ui_posts,
            user=current_user,
        )
    )
