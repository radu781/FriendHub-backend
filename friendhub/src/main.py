import os

from config_keys import DEBUG_ON
from flask import make_response, request
from flask_api import status

from friendhub.src import app, babel


@babel.localeselector
def get_locale() -> str:
    return request.accept_languages.best[:2]


@app.errorhandler(403)
def access_forbidden(err):
    return make_response("Access forbidden" + str(err), status.HTTP_403_FORBIDDEN)


@app.errorhandler(404)
def page_not_found(err):
    return make_response("Page not found" + str(err), status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    if "PROFILE" in os.environ:
        from threading import Thread

        import perf

        mover = Thread(target=perf.move_files)
        mover.start()

    app.run(port=80, debug=DEBUG_ON)
