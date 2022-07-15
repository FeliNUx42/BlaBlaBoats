from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Destination, Trip, Image
from .forms.messages import MsgAboutForm
from .forms.trips import CreateEditTripForm, DeleteTrip, AddImage, DeleteImage
from .tools import save_picture, remove_picture, create_destination, create_place, delete_trip, confirmed_required
from . import db
import os


trips = Blueprint("trips", __name__)

@trips.route("/<uid>")
def trip_page(uid):
  form = MsgAboutForm()
  del_form = DeleteTrip()
  trip = Trip.query.filter_by(uid=uid).first_or_404()

  dest = trip.destinations.order_by(Destination.order.asc()).all()
  markers = [d.to_json() for d in dest]

  return render_template("trips/trip.html", trip=trip, dest=dest, markers=markers, form=form, del_form=del_form)


@trips.route("/<uid>/edit", methods=["GET", "POST"])
@login_required
@confirmed_required
def edit(uid):
  form = CreateEditTripForm()
  trip = Trip.query.filter_by(uid=uid).first_or_404()

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
      filename = os.urandom(8).hex() + os.path.splitext(form.banner.data.filename)[-1]

      remove_picture(trip.banner)
      save_picture(filename, form.banner.data)

      trip.banner = filename
    
    for d in trip.destinations.all():
      db.session.delete(d)
    
    for i, d in enumerate(form.dest.data):
      db.session.add(create_destination(i, d, trip))

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
  
  for d in trip.destinations.order_by(Destination.order.asc()).all():
    form.dest.append_entry(create_place(d))
  
  for i, d in enumerate(form.dest):
    if not i:
      d.place.label.text = "Departure"
    elif i == len(form.dest)-1:
      d.place.label.text = "Arrival"
    else:
      d.place.label.text = f"Stopover {i}"

  return render_template("trips/create_edit.html", form=form, title="Edit Trip", trip=trip)


@trips.route("/create", methods=["GET", "POST"])
@login_required
@confirmed_required
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
      filename = os.urandom(8).hex() + os.path.splitext(form.banner.data.filename)[-1]
      save_picture(filename, form.banner.data)

      trip.banner = filename
 
    for i, d in enumerate(form.dest.data):
      db.session.add(create_destination(i, d, trip))

    db.session.commit()

    flash("Trip created successfully.", "success")

    return redirect(url_for("trips.trip_page", uid=trip.uid))
  
  for i, d in enumerate(form.dest):
    if not i:
      d.place.label.text = "Departure"
    elif i == len(form.dest)-1:
      d.place.label.text = "Arrival"
    else:
      d.place.label.text = f"Stopover {i}"

  return render_template("trips/create_edit.html", form=form, title="Create new Trip")


@trips.route("/<uid>/delete", methods=["POST"])
@login_required
@confirmed_required
def delete(uid):
  form = DeleteTrip()
  trip = Trip.query.filter_by(uid=uid).first_or_404()

  if trip.skipper != current_user:
    abort(403)
  
  if form.validate_on_submit():
    delete_trip(trip)
    
    db.session.commit()
    flash("Trip deleted successfully.", "success")

    return redirect(url_for("profile.user_page", uid=current_user.uid))
  
  return redirect(request.referrer)


@trips.route("/<uid>/pictures", methods=["GET", "POST"])
@login_required
@confirmed_required
def pictures(uid):
  add_form = AddImage()
  del_form = DeleteImage()
  trip = Trip.query.filter_by(uid=uid).first_or_404()

  if trip.skipper != current_user:
    abort(403)
  
  if add_form.add_submit.data and add_form.validate():
    filename = os.urandom(8).hex() + os.path.splitext(add_form.image.data.filename)[-1]
    save_picture(filename, add_form.image.data)

    img = Image()
    img.url = filename
    img.trip = trip

    db.session.add(img)
    db.session.commit()

    flash("Image added successfully.", "success")

  if del_form.del_submit.data and del_form.validate():
    img = trip.images.filter_by(url=del_form.image.data).first()
    if not img: abort(500)

    remove_picture(img.url)
    
    db.session.delete(img)
    db.session.commit()

    flash("Image deleted successfully.", "success")
  
  return render_template("trips/edit_pictures.html", add_form=add_form, del_form=del_form, trip=trip)