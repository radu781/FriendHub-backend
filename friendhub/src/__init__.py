from datetime import datetime

from flask import Flask, render_template, request

import config
from controllers.deploy import deploy_blueprint
from controllers.login_controller import login_blueprint
from controllers.register_controller import register_blueprint
from views.login_view import login_view_blueprint
from views.register_view import register_view_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = config.SESSION_KEY
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"

app.register_blueprint(deploy_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(login_view_blueprint)
app.register_blueprint(register_view_blueprint)


@app.route("/")
def hello_world():
    return render_template("index.html", time=datetime.now(), ip=request.remote_addr)


if __name__ == "__main__":
    app.run(port=80, debug=config.DEBUG_ON)
