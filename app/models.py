from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.search import add_to_index, remove_from_index
from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
from . import db


class SearchableMixin(object):
  @classmethod
  def search(cls, query, sort, dest=False):
    data = current_app.elasticsearch.search(index=cls.__tablename__, query=query, sort=sort)
    data = data.body
    
    ids = [int(hit["_id"]) for hit in data["hits"]["hits"]]
    d_ids = None

    if dest:
      try: 
        d_ids = [[dest["_source"]["id"] for dest in hit["inner_hits"]["destinations"]["hits"]["hits"]] for hit in data["hits"]["hits"]]
        d_ids = sum(d_ids, [])
      except: pass

    if not ids:
      if dest: return cls.query.filter_by(id=0), None
      return cls.query.filter_by(id=0)
    
    ord_ids = list(zip(ids, range(len(ids))))
    models = cls.query.filter(cls.id.in_(ids)).order_by(db.case(ord_ids, value=cls.id))

    if d_ids: d_models = Destination.query.filter(Destination.id.in_(d_ids))
    else: d_models = None

    if dest: return models, d_models
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
    current_app.elasticsearch.options(ignore_status=400)\
          .indices.create(index=cls.__tablename__, mappings=cls.__mapping__)
    for obj in cls.query:
      add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(db.Model, UserMixin, SearchableMixin):
  __indexing__ = ["uid", "email", "username", "full_name", "description"]
  __mapping__ = {
    "properties": {
      "uid": {"type": "text"},
      "email": {"type": "text"},
      "username": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
      "full_name": {"type": "text"},
      "description": {"type": "text"}
    }
  }
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(), unique=True)
  email = db.Column(db.String(16), unique=True)
  username = db.Column(db.String(128), unique=True)
  first_name = db.Column(db.String(128))
  last_name = db.Column(db.String(128))
  description = db.Column(db.String(1024), default="This user does not have a description...")
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


class Destination(db.Model):
  __mapping__ = {
    "type": "nested",
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "text"},
      "location": {"type": "geo_point"},
      "arrival": {"type": "date"},
      "departure": {"type": "date"}
    }
  }
  id = db.Column(db.Integer, primary_key=True)
  order = db.Column(db.Integer)
  name = db.Column(db.String(1024))
  lat = db.Column(db.Float)
  lng = db.Column(db.Float)
  arrival = db.Column(db.Date)
  departure = db.Column(db.Date)

  d_trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

  @property
  def arr(self):
    if not self.arrival:
      return "?"
    return self.arrival.isoformat()
  
  @property
  def dep(self):
    if not self.departure:
      return "?"
    return self.departure.isoformat()
  
  def to_elastic(self):
    return {
      "id": self.id,
      "name": self.name,
      "location": {"lat": self.lat, "lon": self.lng} if (self.lat and self.lng) else None,
      "arrival": self.arrival and self.arrival.isoformat(),
      "departure": self.departure and self.departure.isoformat()
    }
  
  def to_json(self):
    return {
      "name": self.name,
      "location": {"lat": self.lat, "lng": self.lng} if (self.lat and self.lng) else None,
      "arrival": self.arrival and self.arrival.isoformat(),
      "departure": self.departure and self.departure.isoformat(),
      "trip_title": self.trip.title,
      "trip_url": url_for("trips.trip_page", uid=self.trip.uid)
    }

  def __repr__(self):
    return f'<Destination({self.id}, {self.name})>'


class Trip(db.Model, SearchableMixin):
  __indexing__ = ["uid", "title", "description", "boat_type", "boat_model", "sailing_mode", "created", "destinations"]
  __searchable__ = ["uid", "title", "description", "boat_model"]
  __mapping__ = {
    "properties": {
      "uid": {"type": "text"},
      "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
      "description": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
      "boat_type": {"type": "keyword"},
      "boat_model": {"type": "text"},
      "sailing_mode": {"type": "keyword"},
      "created": {"type": "date"},
      "destinations": Destination.__mapping__
    }
  }
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


class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(24))

  i_trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))


class Message(db.Model, SearchableMixin):
  __indexing__ = [
    "uid", "subject", "text",
    "trip_title", "trip_uid",
    "reply_title", "reply_uid",
    "sender.username", "sender.full_name", "sender.uid",
    "receiver.username", "receiver.full_name", "receiver.uid",
  ]
  __mapping__ = {
    "properties": {
      index: {"type": "text"} for index in __indexing__
    }
  }
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

  @property
  def trip_title(self): return self.trip.title if self.trip else None
  
  @property
  def trip_uid(self): return self.trip.uid if self.trip else None
  
  @property
  def reply_title(self): return self.reply.subject if self.reply else None
  
  @property
  def reply_uid(self): return self.reply.uid if self.reply else None