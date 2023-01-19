from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS
from flask_socketio import SocketIO

flask_app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
socketio = SocketIO(flask_app, async_mode=None)
babel = Babel(flask_app)
babel_js = BabelJS(flask_app)
