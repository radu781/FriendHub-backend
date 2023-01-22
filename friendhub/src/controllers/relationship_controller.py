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


@relationship_blueprint.route("/api/relationship", methods=["GET", "POST"])
@needs_login
def relationship(*, current_user: User) -> Response:
    if request.method == "POST":
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
                status.HTTP_400_BAD_REQUEST,
            )
        if not is_uuid_valid(values["userId"]):
            return make_response(
                jsonify({"error": "given id is not a UUID", "id": values["userId"]}),
                status.HTTP_400_BAD_REQUEST,
            )
        if not UserDAO.get_user_by_id(uuid.UUID(values["userId"])):
            return make_response(
                jsonify({"reason": "user does not exist"}), status.HTTP_404_NOT_FOUND
            )
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
        rel_type = Relationship.Type(values["type"])
        created_relationship = Relationship(
            from_=current_user.id_,
            to=uuid.UUID(values["userId"]),
            type=rel_type,
            change_time=datetime.now(),
        )
        db_rel = RelationshipDAO.get_relationship(
            created_relationship.from_, created_relationship.to
        )
        if db_rel["to"].type == Relationship.Type.REQUEST_SENT == created_relationship.type:
            created_relationship.type = Relationship.Type.FRIEND
            RelationshipDAO.upsert(created_relationship)
            db_rel["to"].type = Relationship.Type.FRIEND
            RelationshipDAO.upsert(db_rel["to"])
        else:
            if created_relationship.type == Relationship.Type.NONE:
                RelationshipDAO.upsert(created_relationship)
                db_rel["to"].type = Relationship.Type.NONE
                RelationshipDAO.upsert(db_rel["to"])
            else:
                RelationshipDAO.upsert(created_relationship)
        return make_response(vars(created_relationship), status.HTTP_201_CREATED)

    if request.method == "GET":
        parser = ArgumentParser(
            request,
            {
                Argument("userId", ArgType.MANDATORY, None),
            },
            Method.GET,
        )
        try:
            values = parser.get_values()
        except ArgsNotFoundException as ex:
            return make_response(
                jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
                status.HTTP_400_BAD_REQUEST,
            )
        if not is_uuid_valid(values["userId"]):
            return make_response(
                jsonify({"error": "given id is not a UUID", "id": values["userId"]}),
                status.HTTP_400_BAD_REQUEST,
            )
        if not UserDAO.get_user_by_id(uuid.UUID(values["userId"])):
            return make_response(
                jsonify({"reason": "user does not exist"}), status.HTTP_404_NOT_FOUND
            )
        relationships = RelationshipDAO.get_relationship(
            current_user.id_, uuid.UUID(values["userId"])
        )
        return make_response(
            jsonify({"count": len(relationships), "data": [vars(ele) for ele in relationships]})
        )
    return make_response()
