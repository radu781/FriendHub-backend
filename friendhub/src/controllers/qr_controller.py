import json

import logger
from config_keys import DEPLOYING
from database.script_dao import ScriptDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from models.script_model import Script
from models.user_model import User
from qr.builder import QRCodeBuilder
from utils.validators.decorators import needs_login

qr_blueprint = Blueprint("qr_blueprint", __name__)


@qr_blueprint.route("/api/qr", methods=["POST"])
@needs_login
def qr_code(*, current_user: User) -> Response:
    if not request.json:
        return make_response(jsonify({"error": "missing body"}), status.HTTP_400_BAD_REQUEST)
    if "for" not in request.json or "data" not in request.json:
        return make_response(jsonify({"error": "invalid body"}), status.HTTP_400_BAD_REQUEST)

    src = "https://friendhub.social" if DEPLOYING else "http://127.0.0.1"
    uid = current_user.id_
    match request.json["for"]:
        case "relationship":
            script = Script(
                author_id=uid,
                code=json.dumps(
                    {
                        "method": "POST",
                        "endpoint": "/api/relationship",
                        "params": {
                            "userId": request.json["data"]["userId"],
                            "type": "request_sent",
                        },
                        "body": {},
                        "redirect": "/",
                    }
                ),
            )
            script.encrypt()
            link = f"{src}/api/js_runner/{script.id_}"
            qr = QRCodeBuilder(link)
            logger.debug(f"created {link=}")
            ScriptDAO.add(script)
            qr.make("purple", "white")
            qr.save(uid)

        case "login":
            qr = QRCodeBuilder(str(request.json["data"]))
            qr.make("aqua", "white")
            qr.save(uid)

        case _:
            logger.error(f"unknown {request.json['for']=} value in body")
            return make_response(
                jsonify({"error": "unknown 'for' value in body"}), status.HTTP_400_BAD_REQUEST
            )

    return make_response(
        jsonify({"link": f"{src}/static/uploads/{uid}/qr.png"}), status.HTTP_201_CREATED
    )
