from flask import Flask, request
from flask_babel import Babel

from controllers.deploy import deploy_blueprint
from controllers.login_controller import login_blueprint
from controllers.register_controller import register_blueprint
from controllers.upload_controller import upload_blueprint
from globals import DEBUG_ON, SESSION_KEY
from views.api_view import api_blueprint
from views.index_view import index_view_blueprint
from views.login_view import login_view_blueprint
from views.register_view import register_view_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.config["SECRET_KEY"] = SESSION_KEY
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"
app.config["UPLOAD_FOLDER"] = "../static/uploads"


app.register_blueprint(login_view_blueprint)
app.register_blueprint(register_view_blueprint)
app.register_blueprint(index_view_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(deploy_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(upload_blueprint)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    return request.accept_languages.best[:2]


if __name__ == "__main__":
    app.run(port=80, debug=DEBUG_ON)
