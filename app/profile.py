from flask import Blueprint, render_template, redirect, request, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from PIL import Image as PImage
from .models import User
from .forms import SettingsForm
from . import db
import os


profile = Blueprint("profile", __name__)

@profile.route("/<uid>")
def user_page(uid):
  user = User.query.filter_by(uid=uid).first_or_404()
  if user == current_user:
    form = SettingsForm()
  else:
    form = False
  
  trips=user.trips.all()

  return render_template("profile/prof.html", user=user, form=form, trips=trips)


@profile.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
  form = SettingsForm()

  if request.method == "GET":
    return redirect(url_for("profile.user_page", uid=current_user.uid) + "#settings")

  if not form.validate_on_submit():
    return redirect(url_for("profile.user_page", uid=current_user.uid))

  if form.username.data == current_user.username or not User.query.filter_by(username=form.username.data).first():
    current_user.username = form.username.data
    current_user.description = form.description.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.birthday = form.birthday.data

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
  else:
    flash("This Username is already taken.", "danger")
  
  return redirect(url_for("profile.user_page", uid=current_user.uid) + "#settings")

