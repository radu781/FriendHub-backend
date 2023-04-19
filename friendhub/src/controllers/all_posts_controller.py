from database.post_dao import PostDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.validators.decorators import needs_login

all_post_blueprint = Blueprint("all_post_blueprint", __name__)


@all_post_blueprint.route("/api/post/all", methods=["GET"])
# @needs_login
def all_posts() -> Response:
    parser = ArgumentParser(
        request,
        {Argument("from", ArgType.OPTIONAL, 0), Argument("to", ArgType.OPTIONAL, 20)},
        Method.GET,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )
    values["from"] = max(0, int(values["from"]))  # type: ignore
    values["to"] = max(0, int(values["to"]))  # type: ignore
    posts = PostDAO.get_visible_posts(User(), int(values["from"]), int(values["to"]))
    pretty_posts = [
        {"post": pw.post, "author": pw.user.sanitize(), "vote": pw.vote} for pw in posts
    ]
    return make_response(jsonify({"count": len(pretty_posts), "data": pretty_posts}))
