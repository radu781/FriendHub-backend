from datetime import datetime
import uuid
from database.dbmanager import DBManager
from database.relationship_dao import RelationshipDAO

from database.user_dao import UserDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.relationship_model import Relationship
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.session import get_user_in_session
from utils.etc import is_uuid_valid

relationship_blueprint = Blueprint("relationship_blueprint", __name__)


@relationship_blueprint.route("/api/relationship", methods=["POST"])
def relationship() -> Response:
    current_user = get_user_in_session()
    if current_user is None:
        return make_response(status.HTTP_403_FORBIDDEN)

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
            jsonify({"reason": "given id is not a UUID", "id": values["userId"]}),
            status.HTTP_400_BAD_REQUEST,
        )
    if not UserDAO.get_user_by_id(uuid.UUID(values["userId"])):
        return make_response(jsonify({"reason": "user does not exist"}), status.HTTP_404_NOT_FOUND)
    if not values["type"] in Relationship.Type.values():
        return make_response(
            jsonify(
                {
                    "reason": "type does not exist",
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
