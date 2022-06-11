from flask import Blueprint, render_template, redirect, request, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from PIL import Image as PImage
from .models import Message, User, Trip
from .forms import SettingsForm
from . import db
import os


private = Blueprint("private", __name__)

@private.route("/")
@login_required
def dashboard():
  
  trips = current_user.trips.all()

  return render_template("profile/prof.html", user=current_user, trips=trips)

@private.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
  form = SettingsForm()

  if form.validate_on_submit():
    if form.username.data == current_user.username or not User.query.filter_by(username=form.username.data).first():
      current_user.username = form.username.data
      current_user.description = form.description.data
      current_user.first_name = form.first_name.data
      current_user.last_name = form.last_name.data
      #current_user.birthday = form.birthday.data

      if form.picture.data:
        if current_user.profile_pic != "default.png":
          old_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], current_user.profile_pic)
          os.remove(old_path)

        i = PImage.open(form.picture.data)
        filename = os.urandom(8).hex() + os.path.splitext(form.picture.data.filename)[-1]
        new_path = os.path.join(current_app.root_path, current_app.config["PICTURES_FOLDER"], filename)
        i.save(new_path)

        current_user.profile_pic = filename

      db.session.commit()

      flash("Personal data updated successfully.", "success")

      return redirect(url_for("profile.user_page", uid=current_user.uid))

    else:
      flash("This Username is already taken.", "danger")
  
  return render_template("private/settings.html", form = form)


@private.route("/inbox")
@login_required
def inbox():
  i_messages = current_user.msg_received.order_by(Message.created.desc()).all()
  s_messages = current_user.msg_sent.order_by(Message.created.desc()).all()

  return render_template("private/messages.html", i_messages=i_messages, s_messages=s_messages, Trip=Trip)
    
