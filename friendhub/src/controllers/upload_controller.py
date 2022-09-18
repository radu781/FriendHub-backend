import os
import uuid

from database.post_dao import PostDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Request, Response
from flask_api import status
from models.post_model import Post
from utils.argument_parser import (ArgsNotFoundException, ArgType, Argument,
                                   ArgumentParser, Method)
from werkzeug.utils import secure_filename

upload_blueprint = Blueprint("upload_blueprint", __name__)
UPLOAD_PATH = "friendhub/uploads"


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
    if values["text"] == "":
        return make_response(
            jsonify({"reason": "text missing"}), status.HTTP_406_NOT_ACCEPTABLE
        )

    post_got = __treat_file_upload(request)
    post_got.text = values["text"]
    PostDAO.create_post(post_got)

    return make_response("")


def __treat_file_upload(request: Request) -> Post:
    OWNER_ID = "ff4df6fb-2ee4-45f8-8e79-bc5d1eedd57c"
    if not request.files:
        return Post(owner_id=uuid.UUID(OWNER_ID))

    names: list[str] = ["image-upload", "video-upload", "audio-upload"]
    args_found: dict[str, str] = {}
    for name in names:
        file = request.files[name]
        if file.filename is not None and file.filename != "":
            args_found[name] = secure_filename(file.filename)
            try:
                os.mkdir(f"{UPLOAD_PATH}/{OWNER_ID}")
            except FileExistsError:
                pass
            file.save(f"{UPLOAD_PATH}/{OWNER_ID}/{args_found[name]}")

    current_post = Post(owner_id=uuid.UUID(OWNER_ID))
    if "image-upload" in args_found:
        current_post.image = args_found["image-upload"]
    if "video-upload" in args_found:
        current_post.video = args_found["video-upload"]
    if "audio-upload" in args_found:
        current_post.audio = args_found["audio-upload"]

    return current_post
