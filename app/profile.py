from flask import Blueprint, render_template, redirect, request, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from PIL import Image as PImage
from .models import User
from .forms import MsgContactForm
from . import db
import os


profile = Blueprint("profile", __name__)

@profile.route("/<uid>")
def user_page(uid):
  user = User.query.filter_by(uid=uid).first_or_404()
  form = MsgContactForm()

  if user == current_user:
    return redirect(url_for("private.dashboard"))
  
  trips=user.trips.all()

  return render_template("profile/prof.html", user=user, trips=trips, form=form)