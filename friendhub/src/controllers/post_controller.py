from uuid import UUID

from database.post_dao import PostDAO
from database.vote_dao import VoteDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.vote_model import Vote
from utils.argument_parser import (
    ArgsNotFoundException,
    ArgType,
    Argument,
    ArgumentParser,
    Method,
)
from utils.session import get_user_in_session

post_blueprint = Blueprint("post_blueprint", __name__)


@post_blueprint.route("/api/post/<string:id_>", methods=["GET", "PUT"])
def post(id_: str) -> Response:
    if request.method == "GET":
        try:
            target_post = PostDAO.get_post_by_id(UUID(id_))
        except ValueError:
            return make_response(
                jsonify({"reason": "given id is not a UUID", "id": id_}),
                status.HTTP_400_BAD_REQUEST,
            )
        if target_post is None:
            return make_response(jsonify({"reason": "post not found"}), status.HTTP_404_NOT_FOUND)
        target_post = VoteDAO.get_votes_for_post(target_post)
        return make_response(jsonify(vars(target_post)))

    current_user = get_user_in_session()
    if current_user is None:
        return make_response(
            jsonify({"reason": "you need to be logged in"}),
            status.HTTP_401_UNAUTHORIZED,
        )
    parser = ArgumentParser(
        request,
        {
            Argument("upvote", ArgType.OPTIONAL, None),
            Argument("downvote", ArgType.OPTIONAL, None),
            Argument("clear", ArgType.OPTIONAL, None),
        },
        Method.POST,
    )
    try:
        values = parser.get_values()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_401_UNAUTHORIZED,
        )
    if len([v for v in values.items() if v is not None]) != 1:
        return make_response(
            jsonify({"reason": "only one of 'upvote', 'downvote', 'clear' is supported"}),
            status.HTTP_400_BAD_REQUEST,
        )

    db_vote = VoteDAO.get_vote(UUID(id_), current_user.id_)
    user_intent = Vote.Value([v for v in values.items() if v is not None][0])

    if db_vote is None and user_intent == Vote.Value.CLEAR:
        return make_response(jsonify(), status.HTTP_202_ACCEPTED)

    if db_vote is None and user_intent != Vote.Value.CLEAR:
        VoteDAO.add(Vote(parent_id=UUID(id_), author_id=current_user.id_, value=user_intent))
        return make_response(jsonify(), status.HTTP_201_CREATED)

    if db_vote is not None and user_intent == Vote.Value.CLEAR:
        VoteDAO.delete(db_vote.id_)
        return make_response(status.HTTP_205_RESET_CONTENT)

    if db_vote is not None and db_vote.value == user_intent:
        return make_response(jsonify(), status.HTTP_202_ACCEPTED)

    if db_vote is not None and db_vote.value != user_intent:
        VoteDAO.delete(db_vote.id_)
        VoteDAO.add(Vote(parent_id=UUID(id_), author_id=current_user.id_, value=user_intent))
        return make_response(jsonify(), status.HTTP_201_CREATED)
    return make_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
