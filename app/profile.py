from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user
from .models import User
from .forms.messages import MsgContactForm


profile = Blueprint("profile", __name__)

@profile.route("/<uid>")
def user_page(uid):
  form = MsgContactForm()
  user = User.query.filter_by(uid=uid).first_or_404()

  page = request.args.get("page", 1, type=int)
  
  if user == current_user:
    return redirect(url_for("private.dashboard"))
  
  trips = user.trips.paginate(page=page, per_page=current_app.config["RES_PER_PAGE"]/2)

  trip_ids = {t.id : [d.to_json() for d in t.destinations.all()] for t in user.trips.all()}

  return render_template("profile/prof.html", user=user, trips=trips, trip_ids=trip_ids, form=form)