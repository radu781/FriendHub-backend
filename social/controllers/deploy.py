from datetime import datetime
from flask import Blueprint, make_response, request, jsonify
from flask.wrappers import Response
import config
import subprocess
from flask_api import status

deploy_blueprint = Blueprint("deploy_blueprint", __name__)


@deploy_blueprint.route("/deploy", methods=["POST"])
def deploy() -> Response:
    if not "key" in request.args:
        return make_response(
            jsonify({"reason": "'key' argument required"}), status.HTTP_401_UNAUTHORIZED
        )
    if request.args["key"] != config.DEPLOY_KEY:
        return make_response(
            jsonify({"reason": "wrong deploy key"}), status.HTTP_401_UNAUTHORIZED
        )

    with open("deploy.log", "a") as file:
        time = datetime.now()
        try:
            pull_output = subprocess.check_output(["git", "pull"])
        except subprocess.CalledProcessError as ex:
            file.write(f"{time} [FAIL] {ex}")
        else:
            file.write(f"{time} [DONE] {pull_output.decode()}")
    return make_response("")
