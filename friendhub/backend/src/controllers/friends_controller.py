import uuid
from datetime import datetime

from database.relationship_dao import RelationshipDAO
from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.relationship_model import Relationship
from models.user_model import User
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.validators.decorators import needs_login

friends_blueprint = Blueprint("friends_blueprint", __name__)


@friends_blueprint.route("/api/friends", methods=["GET"])
@needs_login
def friends(*, current_user: User) -> Response:
    friends = RelationshipDAO.get_friends(current_user.id_)
    return make_response(jsonify(friends), status.HTTP_200_OK)
