from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_moment import Moment
from flask_sitemap import Sitemap
from elasticsearch import Elasticsearch
from sendgrid import SendGridAPIClient
import stripe
from .config import Config
from .adminViews import IndexView


db = SQLAlchemy()
moment = Moment()
admin = Admin(name='Admin Panel', template_mode='bootstrap4', index_view=IndexView(), base_template="layout/admin.html")
sitemap = Sitemap()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
  from .models import User
  return User.query.get(int(id))

def create_app():
  from .models import User, Trip, Destination, Image, Message, UserMsg
  from .adminViews import UserView, TripView, MessageView, UserMsgView
  from .forms.search import SearchForm
  app = Flask(__name__)

  app.config.from_object(Config)

  app.elasticsearch = Elasticsearch(app.config["ELASTICSEARCH_URL"])
  app.sendgrid = SendGridAPIClient(app.config["SENDGRID_API_KEY"])

  app.stripe = stripe
  app.stripe.api_key = app.config["STRIPE_SECRET_KEY"]


  db.init_app(app)
  db.create_all(app=app)

  login_manager.init_app(app)
  moment.init_app(app)
  sitemap.init_app(app)

  @app.context_processor
  def globals():
    return {
      "search_form": SearchForm(),
      "User": User,
      "Trip": Trip,
      "Message": Message,
      "UserMsg": UserMsg,
      "enumerate": enumerate,
      "len": len,
      "current_app": current_app
    }

  admin.add_view(UserView(User, db.session))
  admin.add_view(TripView(Trip, db.session))
  admin.add_view(MessageView(Message, db.session))
  admin.add_view(UserMsgView(UserMsg, db.session, "UserMsg"))
  admin.init_app(app)


  from .home import home
  from .donate import donate
  from .profile import profile
  from .private import private
  from .messages import messages
  from .trips import trips
  from .auth import auth
  from .errors import errors

  app.register_blueprint(home)
  app.register_blueprint(donate, url_prefix="/donate")
  app.register_blueprint(profile, url_prefix="/user")
  app.register_blueprint(private, url_prefix="/private")
  app.register_blueprint(messages, url_prefix="/message")
  app.register_blueprint(trips, url_prefix="/trip")
  app.register_blueprint(auth, url_prefix="/auth")
  app.register_blueprint(errors)

  return app