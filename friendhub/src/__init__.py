import os
from datetime import timedelta

from config_keys import SESSION_KEY
from controllers.delete_user_controller import delete_user_blueprint
from controllers.deploy import deploy_blueprint
from controllers.login_controller import login_blueprint
from controllers.logout_controller import logout_blueprint
from controllers.post_controller import post_blueprint
from controllers.profile_controller import profile_blueprint
from controllers.register_controller import register_blueprint
from controllers.relationship_controller import relationship_blueprint
from controllers.upload_controller import upload_blueprint
from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS
from views.api_view import api_blueprint
from views.docs_view import docs_blueprint
from views.index_view import index_view_blueprint
from views.login_view import login_view_blueprint
from views.profile_view import profile_view_blueprint
from views.register_view import register_view_blueprint
from views.settings.base import settings_base_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.config["SECRET_KEY"] = SESSION_KEY
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(weeks=52)
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"
app.config["UPLOAD_FOLDER"] = "../static/uploads"


app.register_blueprint(login_view_blueprint)
app.register_blueprint(register_view_blueprint)
app.register_blueprint(index_view_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(docs_blueprint)
app.register_blueprint(deploy_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(profile_view_blueprint)
app.register_blueprint(delete_user_blueprint)
app.register_blueprint(settings_base_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(relationship_blueprint)

babel = Babel(app)
babel_js = BabelJS(app)


if "PROFILE" in os.environ:
    import shutil

    from werkzeug.middleware.profiler import ProfilerMiddleware

    try:
        shutil.rmtree("friendhub/performance/", ignore_errors=True)
        os.mkdir("friendhub/performance/")
    except (FileNotFoundError, FileExistsError):
        pass

    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[10], profile_dir="friendhub/performance/", stream=None  # type:ignore
    )
