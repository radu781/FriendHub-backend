import os
import uuid

from database.post_dao import PostDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Request, Response
from flask_api import status
from models.post_model import Post
from models.user_model import User
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method
from utils.validators.decorators import needs_login
from werkzeug.utils import secure_filename

upload_blueprint = Blueprint("upload_blueprint", __name__)
UPLOAD_PATH = "friendhub/static/uploads"
try:
    os.mkdir(UPLOAD_PATH)
except FileExistsError:
    pass


@upload_blueprint.route("/api/upload", methods=["POST"])
@needs_login
def upload(*, current_user: User) -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("text", ArgType.MANDATORY, None),
            Argument("image-upload", ArgType.OPTIONAL, None),
            Argument("video-upload", ArgType.OPTIONAL, None),
            Argument("audio-upload", ArgType.OPTIONAL, None),
        },
        Method.POST,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )
    if values["text"] == "":
        return make_response(jsonify({"reason": "text missing"}), status.HTTP_406_NOT_ACCEPTABLE)

    post_got = __treat_file_upload(request, current_user.id_)
    post_got.text = values["text"]
    PostDAO.create_post(post_got)

    return make_response(jsonify({"post": vars(post_got)}), status.HTTP_201_CREATED)


def __treat_file_upload(req: Request, user_id: uuid.UUID) -> Post:
    if not req.files:
        return Post(
            owner_id=user_id,
            likes=0,
            dislikes=0,
            text="",
            image=None,
            video=None,
            audio=None,
        )

    names: list[str] = ["image-upload", "video-upload", "audio-upload"]
    args_found: dict[str, str] = {}
    for name in names:
        try:
            file = req.files[name]
        except KeyError:
            continue
        if file.filename is not None and file.filename != "":
            args_found[name] = secure_filename(file.filename)
            try:
                os.mkdir(f"{UPLOAD_PATH}/{user_id}")
            except FileExistsError:
                pass
            file.save(f"{UPLOAD_PATH}/{user_id}/{args_found[name]}")

    current_post = Post(
        owner_id=user_id,
        likes=0,
        dislikes=0,
        text="",
        image=None,
        video=None,
        audio=None,
    )
    if "image-upload" in args_found:
        current_post.image = args_found["image-upload"]
    if "video-upload" in args_found:
        current_post.video = args_found["video-upload"]
    if "audio-upload" in args_found:
        current_post.audio = args_found["audio-upload"]

    return current_post
