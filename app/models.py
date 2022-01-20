from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, date
from dateutil import relativedelta
from flask import current_app
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(), unique=True)
  email = db.Column(db.String(16), unique=True)
  #public_email = db.Column(db.Boolean, default=True)
  username = db.Column(db.String(128), unique=True)
  first_name = db.Column(db.String(128))
  last_name = db.Column(db.String(128))
  description = db.Column(db.String(1024), default="This user does not have a description...")
  birthday = db.Column(db.Date)
  #created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
  #confirmed = db.Column(db.Boolean, default=False)
  #profile_pic = db.Column(db.String(128), default="default.png")
  password_hash = db.Column(db.String(128))

  trips = db.relationship("Trip", backref="skipper", lazy=True)

  @property
  def password(self):
    raise AttributeError("password is not a readable attribute")

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  @property
  def age(self):
    today = date.today()
    age = relativedelta.relativedelta(today, self.birthday)

    return age.years
  
  def get_token(self, command, expire_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
    return s.dumps({'user_id': self.id, 'command': command}).decode('utf-8')
  
  @staticmethod
  def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except:
      return None, None
    return User.query.get(data['user_id']), data['command']


  def __repr__(self):
    return f'<User({self.id}, {self.uid}, {self.username})>'


class Trip(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(), unique=True)
  title = db.Column(db.String(128), unique=True)
  description = db.Column(db.String(1024), default="This user does not have a description...")
  mode = db.Column(db.String(128))
  #created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
  #picture = db.Column(db.String(128), default="default.png")

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

  def __repr__(self):
    return f'<Trip({self.id}, {self.uid}, {self.title})>'


class Destination(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  arrival = db.Column(db.Date)
  departure = db.Column(db.Date)

  def __repr__(self):
    return f'<Destination({self.id}, {self.name})>'
