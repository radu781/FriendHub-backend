import subprocess
from datetime import datetime

import config_keys
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status

deploy_blueprint = Blueprint("deploy_blueprint", __name__)


@deploy_blueprint.route("/api/deploy", methods=["POST"])
def deploy() -> Response:
    if not "key" in request.args:
        return make_response(
            jsonify({"reason": "'key' argument required"}), status.HTTP_401_UNAUTHORIZED
        )
    if request.args["key"] != config_keys.DEPLOY_KEY:
        return make_response(jsonify({"reason": "wrong deploy key"}), status.HTTP_401_UNAUTHORIZED)

    time = datetime.now()
    try:
        pull_output = subprocess.check_output(
            ["sudo", "sh", "-c", "cd /var/www/friendhub && git pull"]
        )
    except subprocess.CalledProcessError as ex:
        return make_response(
            jsonify({"reason": str(ex)}),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        reload_output = subprocess.check_output(["sudo", "sh", "-c", "systemctl reload apache2"])
    except subprocess.CalledProcessError as ex:
        return make_response(
            jsonify({"reason": str(ex), "git pull": pull_output.decode()}),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return make_response("", status.HTTP_200_OK)
