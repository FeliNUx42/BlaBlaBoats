from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from .config import Config


db = SQLAlchemy()
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
  from .models import User
  return User.query.get(int(id))

def create_app():
  from .models import User, Trip, Destination, Image, Message
  app = Flask(__name__)

  app.config.from_object(Config)

  db.init_app(app)
  db.create_all(app=app)
  login_manager.init_app(app)
  moment.init_app(app)

  from .home import home
  from .profile import profile
  from .messages import messages
  from .trips import trips
  from .auth import auth
  from .errors import errors

  app.register_blueprint(home)
  app.register_blueprint(profile, url_prefix="/user")
  app.register_blueprint(messages, url_prefix="/message")
  app.register_blueprint(trips, url_prefix="/trip")
  app.register_blueprint(auth, url_prefix="/auth")
  app.register_blueprint(errors)

  return app