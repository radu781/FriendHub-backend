import uuid

from database.post_dao import PostDAO
from database.user_dao import UserDAO
from database.vote_dao import VoteDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.user_model import User
from models.vote_model import Vote
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.session import setup_session
from utils.validators.decorators import Types, check_params, log_endpoint, needs_login

post_blueprint = Blueprint("post_blueprint", __name__)


@post_blueprint.route("/api/post/<string:id_>", methods=["GET", "PUT"])
@check_params({"id_": Types.UUID})
@log_endpoint
@setup_session
@needs_login
def post(*, id_: uuid.UUID, current_user: User) -> Response:
    if request.method == "GET":
        target_post = PostDAO.get_post_by_id(id_)
        if target_post is None:
            return make_response(jsonify({"reason": "post not found"}), status.HTTP_404_NOT_FOUND)
        target_post = VoteDAO.update_votes_for_post(target_post)
        own_vote = VoteDAO.get_vote(target_post.id_, current_user.id_)
        post_author = UserDAO.get_user_by_id(target_post.owner_id)
        return make_response(
            jsonify(
                {
                    "data": {
                        "post": target_post,
                        "vote": own_vote,
                        "author": post_author,
                    },
                }
            ),
            status.HTTP_200_OK,
        )

    parser = ArgumentParser(
        request,
        {
            Argument("vote", ArgType.MANDATORY, None),
        },
        Method.POST,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )

    db_vote = VoteDAO.get_vote(id_, current_user.id_)
    user_intent = Vote.Value(values["vote"])

    if db_vote is None and user_intent.is_clear:
        return make_response("", status.HTTP_202_ACCEPTED)

    if db_vote is None and not user_intent.is_clear:
        VoteDAO.add(Vote(parent_id=id_, author_id=current_user.id_, value=user_intent))
        return make_response("", status.HTTP_201_CREATED)

    if db_vote is not None and user_intent.is_clear:
        VoteDAO.delete(db_vote.id_)
        return make_response("", status.HTTP_205_RESET_CONTENT)

    if db_vote is not None and db_vote.value == user_intent:
        return make_response("", status.HTTP_202_ACCEPTED)

    if db_vote is not None and db_vote.value != user_intent:
        VoteDAO.delete(db_vote.id_)
        VoteDAO.add(Vote(parent_id=id_, author_id=current_user.id_, value=user_intent))
        return make_response(jsonify({"vote": vars(db_vote)}), status.HTTP_201_CREATED)
    return make_response("unexpected error", status.HTTP_500_INTERNAL_SERVER_ERROR)
