import sys
#sys.path.append("/var/www/social")
#sys.path.append("/var/www/social/social")
import os
os.chdir("/var/www/social")
from datetime import datetime
from flask import Flask, render_template, request
import config

from controllers.deploy import deploy_blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SESSION_KEY
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"

app.register_blueprint(deploy_blueprint)


@app.route("/")
def hello_world():
    return render_template("index.html", time=datetime.now(), ip=request.remote_addr, pwd=config.pwd)


if __name__ == "__main__":
    app.run(port=80, debug=False)
