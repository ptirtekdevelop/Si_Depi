from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_minify import Minify
from flask_login import LoginManager
from werkzeug.serving import WSGIRequestHandler
from flask_session import Session

from datetime import timedelta

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

CORS(app, resources={r"/socket.io/*": {"origins": "*"}})


# Create database connection object
db = SQLAlchemy()
db.init_app(app)

# create SocketIO Instance
socketio = SocketIO(app, cors_allowed_origins='*')

bcrypt = Bcrypt()
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message_category = "info"

Minify(app=app, html=True, js=True, cssless=True)


from .auth import auth
from .detect import detect
from .views import views

# Routes

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(detect, url_prefix='/')
app.register_blueprint(views, url_prefix='/')

# Models
from .models_db import Users, RoadDamage, RoadData

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
