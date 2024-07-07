import os
from datetime import timedelta

from config_keys import SESSION_KEY
from controllers.activity_controller import activity_blueprint
from controllers.all_posts_controller import all_post_blueprint
from controllers.delete_user_controller import delete_user_blueprint
from controllers.deploy import deploy_blueprint
from controllers.login_controller import login_blueprint
from controllers.logout_controller import logout_blueprint
from controllers.post_controller import post_blueprint
from controllers.profile_controller import profile_blueprint
from controllers.qr_controller import qr_blueprint
from controllers.register_controller import register_blueprint
from controllers.relationship_controller import relationship_blueprint
from controllers.search_controller import search_blueprint
from controllers.settings_controller import settings_blueprint
from controllers.upload_controller import upload_blueprint
from controllers.user_stats import user_stats_blueprint
from views.js_runner import js_redirect_blueprint
from controllers.online_activity_controller import online_activity_blueprint
from controllers.friends_controller import friends_blueprint

from . import flask_app

flask_app.config["SECRET_KEY"] = SESSION_KEY
flask_app.config["SESSION_TYPE"] = "SameSite"
flask_app.config["CORD_HEADERS"] = "Content-Type"
flask_app.config["SESSION_COOKIE_PATH"] = "/"
flask_app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(weeks=52)
flask_app.config["BABEL_DEFAULT_LOCALE"] = "en"
flask_app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"
flask_app.config["UPLOAD_FOLDER"] = "../static/uploads"


flask_app.register_blueprint(activity_blueprint)
flask_app.register_blueprint(all_post_blueprint)
flask_app.register_blueprint(delete_user_blueprint)
flask_app.register_blueprint(deploy_blueprint)
flask_app.register_blueprint(js_redirect_blueprint)
flask_app.register_blueprint(login_blueprint)
flask_app.register_blueprint(logout_blueprint)
flask_app.register_blueprint(post_blueprint)
flask_app.register_blueprint(profile_blueprint)
flask_app.register_blueprint(qr_blueprint)
flask_app.register_blueprint(register_blueprint)
flask_app.register_blueprint(relationship_blueprint)
flask_app.register_blueprint(search_blueprint)
flask_app.register_blueprint(settings_blueprint)
flask_app.register_blueprint(upload_blueprint)
flask_app.register_blueprint(user_stats_blueprint)
flask_app.register_blueprint(online_activity_blueprint)
flask_app.register_blueprint(friends_blueprint)


if "PROFILE" in os.environ:
    import perf

    perf.profile(flask_app)
