from flask import Blueprint, abort, current_app, render_template, redirect, request, url_for, flash, request
from flask_login import login_required, current_user
from PIL import Image as PImage
from datetime import datetime
from .models import Destination, User, Trip, Image
from .forms import ContactForm, CreateEditTripForm, Place
from . import db
import os


trips = Blueprint("trips", __name__)

@trips.route("/<uid>")
def trip_page(uid):
  trip = Trip.query.filter_by(uid=uid).first_or_404()
  form = ContactForm()

  destinations = trip.destinations.order_by(Destination.order.asc()).all()

  return render_template("trips/trip.html", trip=trip, destinations=destinations, form=form)
   

@trips.route("/<uid>/edit", methods=["GET", "POST"])
@login_required
def edit(uid):
  trip = Trip.query.filter_by(uid=uid).first_or_404()
  form = CreateEditTripForm()

  if trip.skipper != current_user:
    abort(403)

  if form.validate_on_submit():
    trip.title = form.title.data
    trip.description = form.description.data
    trip.boat_type = form.boat_type.data
    trip.boat_model = form.boat_model.data
    trip.sailing_mode = form.sailing_mode.data
    trip.travel_expenses = form.travel_expenses.data
    trip.qualif_level = form.qualif_level.data

    if form.banner.data:
      old_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], trip.banner.url)
      os.remove(old_path)

      i = PImage.open(form.banner.data)
      filename = os.urandom(8).hex() + os.path.splitext(form.banner.data.filename)[-1]
      new_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], filename)
      i.save(new_path)

      trip.banner.url = filename
    
    for d in trip.destinations.all():
      db.session.delete(d)
    
    for i, d in enumerate(form.dest.data):
      dest = Destination()
      dest.name = d["place"]
      dest.order = i
      dest.arrival = d["arr_date"]
      dest.departure = d["dep_date"]
      dest.trip = trip

      db.session.add(dest)

    db.session.commit()

    flash("Trip details updated successfully.", "success")

    return redirect(url_for("trips.trip_page", uid=trip.uid))
  
  form.submit.label.text = "Save changes"
  form.title.data = trip.title
  form.description.data = trip.description
  form.boat_type.data = trip.boat_type
  form.boat_model.data = trip.boat_model
  form.sailing_mode.data = trip.sailing_mode
  form.travel_expenses.data = trip.travel_expenses
  form.qualif_level.data = trip.qualif_level

  form.dest.pop_entry()
  form.dest.pop_entry()
  
  for i, d in enumerate(trip.destinations.order_by(Destination.order.asc()).all()):
    entry = Place()
    entry.place = d.name
    entry.arr_date = d.arrival
    entry.dep_date = d.departure
    form.dest.append_entry(entry)
  
  for i, d in enumerate(form.dest):
    if not i: d.place.label.text = "Departure"
    elif i == len(form.dest) - 1: d.place.label.text = "Arrival"
    else: d.place.label.text = f"Stopover {i}"

  return render_template("trips/create_edit.html", form=form, title="Edit Trip", enumerate=enumerate, len=len)


@trips.route("/create", methods=["GET", "POST"])
@login_required
def create():
  form = CreateEditTripForm()

  if form.validate_on_submit():
    trip = Trip()
    trip.skipper = current_user
    trip.uid = os.urandom(8).hex()
    trip.title = form.title.data
    trip.description = form.description.data
    trip.boat_type = form.boat_type.data
    trip.boat_model = form.boat_model.data
    trip.sailing_mode = form.sailing_mode.data
    trip.travel_expenses = form.travel_expenses.data
    trip.qualif_level = form.qualif_level.data

    db.session.add(trip)

    if form.banner.data:
      i = PImage.open(form.banner.data)
      filename = os.urandom(8).hex() + os.path.splitext(form.banner.data.filename)[-1]
      path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], filename)
      i.save(path)
    else:
      filename = "default.png"
      
    img = Image()
    img.url = filename
    img.trip = trip

    db.session.add(img)

    for i, d in enumerate(form.dest.data):
      dest = Destination()
      dest.name = d["place"]
      dest.order = i
      dest.arrival = d["arr_date"]
      dest.departure = d["dep_date"]
      dest.trip = trip

      db.session.add(dest)

    db.session.commit()

    flash("Trip created successfully.", "success")

    return redirect(url_for("trips.trip_page", uid=trip.uid))
  
  for i, d in enumerate(form.dest):
    if not i: d.place.label.text = "Departure"
    elif i == len(form.dest) - 1: d.place.label.text = "Arrival"
    else: d.place.label.text = f"Stopover {i}"

  return render_template("trips/create_edit.html", form=form, title="Create new Trip", enumerate=enumerate, len=len)


@trips.route("/<uid>/delete") # exploit: csrf
@login_required
def delete(uid):
  trip = Trip.query.filter_by(uid=uid).first_or_404()

  if trip.skipper != current_user:
    abort(403)

  if trip.banner.url != "default.png":
    banner = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], trip.banner.url)
    os.remove(banner)

  db.session.delete(trip)
  db.session.commit()

  return redirect(url_for("profile.user_page", uid=current_user.uid))
