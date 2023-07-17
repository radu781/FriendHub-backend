import uuid

from database.post_dao import PostDAO, UserDAO
from database.relationship_dao import RelationshipDAO
from models.relationship_model import Relationship
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from utils.validators.decorators import Types, check_params

user_stats_blueprint = Blueprint("user_stats_blueprint", __name__)

# TODO: add activity tracker
@user_stats_blueprint.route("/api/stats/<string:id_>", methods=["GET"])
@check_params({"id_": Types.UUID})
def stats(*, id_: uuid.UUID) -> Response:
    target_user = UserDAO.get_user_by_id(id_)
    if not target_user or not target_user.is_ok:
        return make_response(jsonify({"reason": "user not found"}), status.HTTP_404_NOT_FOUND)

    post_count = PostDAO.get_post_count_by_user(target_user.id_)
    post_score = PostDAO.get_score_by_user(target_user.id_)
    friends = RelationshipDAO.get_relationship_count(target_user.id_, Relationship.Type.FRIEND)
    return make_response(
        jsonify(
            {
                "postCount": post_count,
                "score": post_score,
                "friendCount": friends,
                "joinTime": target_user.join_time,
            }
        ),
        status.HTTP_200_OK,
    )
