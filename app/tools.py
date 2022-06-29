from flask import current_app
from PIL import Image as PImage
from .models import Destination
from .forms.trips import Place
from . import db
import os


def save_picture(filename, data):
  i = PImage.open(data)
  full_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], filename)
  i.save(full_path)

def remove_picture(path):
  if path in ("default.png",):
    return False
  
  full_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], path)
  os.remove(full_path)

def create_destination(order, dic, trip):
  dest = Destination()
  dest.name = dic["place"]
  dest.lat = dic["lat"]
  dest.lng = dic["lng"]
  dest.order = order
  dest.arrival = dic["arr_date"]
  dest.departure = dic["dep_date"]
  dest.trip = trip

  return dest

def create_place(dest):
  place = Place()
  place.place = dest.name
  place.lat = dest.lat
  place.lng = dest.lng
  place.arr_date = dest.arrival
  place.dep_date = dest.departure
  return place

def delete_trip(trip):
  remove_picture(trip.banner)

  for dest in trip.destinations.all():
    db.session.delete(dest)
  
  for img in trip.images.all():
    remove_picture(img.url)
    db.session.delete(img)
  
  db.session.delete(trip)