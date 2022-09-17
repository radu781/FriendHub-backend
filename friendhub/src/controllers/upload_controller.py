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
            Argument("image-upload", ArgType.Optional, None),
            Argument("video-upload", ArgType.Optional, None),
            Argument("audio-upload", ArgType.Optional, None),
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
    if "text" in request.form and request.form["text"] == "" or "text" in request.args and request.args["text"] == "":
        return make_response(
            jsonify({"reason": "text missing"}), status.HTTP_406_NOT_ACCEPTABLE
        )

    if request.files:
        names: list[str] = ["image-upload", "video-upload", "audio-upload"]
        none_names: list[str] = []
        for name in names:
            file = request.files[name]
            if file.filename is None:
                none_names.append(name)
            elif file.filename != "":
                file.save(f"friendhub/uploads/{secure_filename(file.filename)}")
        if none_names != []:
            return make_response(
                jsonify(
                    {"reason": "filenames are null", "filenames": ", ".join(none_names)}
                ),
                status.HTTP_406_NOT_ACCEPTABLE,
            )

    return make_response("")
