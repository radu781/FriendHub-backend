import uuid
from datetime import datetime

from database.relationship_dao import RelationshipDAO
from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.relationship_model import Relationship
from models.user_model import User
from utils.argument_parser import *
from utils.etc import is_uuid_valid
from utils.validators.decorators import needs_login

relationship_blueprint = Blueprint("relationship_blueprint", __name__)


@relationship_blueprint.route("/api/relationship", methods=["POST"])
@needs_login
def relationship(*, current_user: User) -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("userId", ArgType.MANDATORY, None),
            Argument("type", ArgType.MANDATORY, None),
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
    if not is_uuid_valid(values["userId"]):
        return make_response(
            jsonify({"error": "given id is not a UUID", "id": values["userId"]}),
            status.HTTP_400_BAD_REQUEST,
        )
    if not UserDAO.get_user_by_id(uuid.UUID(values["userId"])):
        return make_response(jsonify({"reason": "user does not exist"}), status.HTTP_404_NOT_FOUND)
    if not values["type"] in Relationship.Type.values():
        return make_response(
            jsonify(
                {
                    "reason": "'type' does not exist",
                    "supportedTypes": list(Relationship.Type.values()),
                }
            ),
            status.HTTP_400_BAD_REQUEST,
        )
    created_relationship = Relationship(
        user_id1=current_user.id_,
        user_id2=uuid.UUID(values["userId"]),
        type=Relationship.Type(values["type"]),
        change_time=datetime.now(),
    )
    RelationshipDAO.insert_or_update(created_relationship)
    return make_response(vars(created_relationship), status.HTTP_201_CREATED)
