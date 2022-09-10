from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
	return render_template("index.html", time=datetime.now(), ip=request.remote_addr)


if __name__ == "__main__":
    app.run(port=80, debug=True)
