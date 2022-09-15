from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from utils.argument_parser import (
    ArgsNotFoundException,
    ArgType,
    Argument,
    ArgumentParser,
    Method,
)
from werkzeug.utils import secure_filename

upload_blueprint = Blueprint("upload_blueprint", __name__)


@upload_blueprint.route("/api/upload", methods=["POST"])
def upload() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("text", ArgType.Mandatory, None),
        },
        Method.Post,
    )
    try:
        values = parser.get_values()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify(
                {"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}
            ),
            status.HTTP_401_UNAUTHORIZED,
        )
    file = request.files["image-upload"]
    if file.filename is None:
        return make_response(
            jsonify({"reason": "filename is null"}),
            status.HTTP_406_NOT_ACCEPTABLE,
        )
    file.save(f"friendhub/uploads/{secure_filename(file.filename)}")

    return make_response("")
