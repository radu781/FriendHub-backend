import os
import uuid

from config_keys import DEBUG_ON
from flask import jsonify, make_response, render_template, request, send_from_directory
from flask_api import status
from utils.validators.decorators import Types, check_params
from werkzeug.exceptions import NotFound

import app.flask
from app import flask_app, babel


@babel.localeselector
def get_locale() -> str:
    return request.accept_languages.best[:2]


@flask_app.errorhandler(403)
def access_forbidden(err):
    return make_response("Access forbidden" + str(err), status.HTTP_403_FORBIDDEN)


@flask_app.errorhandler(404)
def page_not_found(err):
    return make_response("Page not found" + str(err), status.HTTP_404_NOT_FOUND)


@flask_app.route("/chat")
def chat():
    return render_template("chat.html")


@flask_app.route("/static/uploads/<string:id_>/<string:name>")
@check_params({"id_": Types.UUID})
def multimedia(*, id_: uuid.UUID, name: str):
    try:
        return send_from_directory("../../static", f"uploads/{id_}/{name}")
    except NotFound as ex:
        return make_response(jsonify({"error": ex.description}), status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    if "PROFILE" in os.environ:
        from threading import Thread

        import perf

        mover = Thread(target=perf.move_files)
        mover.start()

    flask_app.run(port=80, debug=DEBUG_ON)
