from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.search import add_to_index, remove_from_index, query_index
from datetime import datetime, date
from dateutil import relativedelta
from flask import current_app
from flask_login import UserMixin
from . import db


class SearchableMixin(object):
  @classmethod
  def search(cls, expression, **kwargs):
    data = query_index(cls.__tablename__, expression, **kwargs).body
    ids = [int(hit["_id"]) for hit in data["hits"]["hits"]]
    total = data["hits"]["total"]["value"]
    if not total:
      return cls.query.filter_by(id=0)
    when = zip(ids, range(len(ids)))
    models = cls.query.filter(cls.id.in_(ids)).order_by(db.case(list(when), value=cls.id))
    return models

  @classmethod
  def before_commit(cls, session):
    session._changes = {
      "add" : list(session.new),
      "update" : list(session.dirty),
      "delete" : list(session.deleted)
    }
  
  @classmethod
  def after_commit(cls, session):
    for obj in session._changes['add']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__, obj)
    for obj in session._changes['update']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__, obj)
    for obj in session._changes['delete']:
      if isinstance(obj, SearchableMixin):
        remove_from_index(obj.__tablename__, obj)
    session._changes = None

  @classmethod
  def reindex(cls):
    for obj in cls.query:
      add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(db.Model, UserMixin, SearchableMixin):
  __searchable__ = ["uid", "email", "username", "full_name", "description"]
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(), unique=True)
  email = db.Column(db.String(16), unique=True)
  #public_email = db.Column(db.Boolean, default=True)
  username = db.Column(db.String(128), unique=True)
  first_name = db.Column(db.String(128))
  last_name = db.Column(db.String(128))
  description = db.Column(db.String(1024), default="This user does not have a description...")
  #birthday = db.Column(db.Date)
  #created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
  #confirmed = db.Column(db.Boolean, default=False)
  profile_pic = db.Column(db.String(24), default="default.png")
  password_hash = db.Column(db.String(128))

  trips = db.relationship("Trip", backref="skipper", lazy="dynamic")
  msg_sent = db.relationship("Message", foreign_keys="Message.sender_id", backref="sender", lazy="dynamic")
  msg_received = db.relationship("Message", foreign_keys="Message.receiver_id", backref="receiver", lazy="dynamic")

  @property
  def password(self):
    raise AttributeError("password is not a readable attribute")

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  """
  @property
  def age(self):
    today = date.today()
    age = relativedelta.relativedelta(today, self.birthday)

    return age.years
  """
  
  @property
  def full_name(self):
    return self.first_name + " " + self.last_name
  
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


class Trip(db.Model, SearchableMixin):
  __searchable__ = ["uid", "title", "description"]
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(16), unique=True)
  title = db.Column(db.String(72), unique=True)
  description = db.Column(db.String(2048), default="This user does not have a description...")
  boat_type = db.Column(db.String(64))
  boat_model = db.Column(db.String(64))
  sailing_mode = db.Column(db.String(64))
  travel_expenses = db.Column(db.String(64))
  qualif_level = db.Column(db.String(64))
  created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  destinations = db.relationship("Destination", backref="trip", lazy="dynamic")
  banner = db.Column(db.String(24), default="default.png")
  images = db.relationship("Image", backref="trip", lazy="dynamic")

  messages = db.relationship("Message", backref="trip", lazy="dynamic")

  def __repr__(self):
    return f'<Trip({self.id}, {self.uid}, {self.title})>'


class Destination(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order = db.Column(db.Integer)
  name = db.Column(db.String(128))
  arrival = db.Column(db.Date)
  departure = db.Column(db.Date)

  d_trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

  def __repr__(self):
    return f'<Destination({self.id}, {self.name})>'


class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(24))

  i_trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))


class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(16), unique=True)
  subject = db.Column(db.String(64))
  text = db.Column(db.String(2048))
  created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
  read = db.Column(db.Boolean, default=False)
  m_trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

  reply_id = db.Column(db.Integer, db.ForeignKey('message.id'))
  reply = db.relationship('Message', remote_side=[id])

  sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))