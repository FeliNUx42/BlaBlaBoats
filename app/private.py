from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .models import Message
from .forms.private import SettingsForm
from .forms.search import MsgSearchForm
from .tools import confirmed_required, save_picture, remove_picture
from . import db
import os


private = Blueprint("private", __name__)

@private.route("/")
@login_required
def dashboard():
  page = request.args.get("page", 1, type=int)
  trips = current_user.trips.paginate(page=page, per_page=current_app.config["RES_PER_PAGE"])

  trip_ids = {t.id : [d.to_json() for d in t.destinations.all()] for t in current_user.trips.all()}

  return render_template("profile/prof.html", user=current_user, trip_ids=trip_ids, trips=trips)


@private.route('/settings', methods=["GET", "POST"])
@login_required
@confirmed_required
def settings():
  form = SettingsForm()

  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.description = form.description.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data

    if form.picture.data:
      filename = os.urandom(8).hex() + os.path.splitext(form.picture.data.filename)[-1]
      
      remove_picture(current_user.profile_pic)
      save_picture(filename, form.picture.data)

      current_user.profile_pic = filename

    db.session.commit()

    flash("Personal data updated successfully.", "success")

    return redirect(url_for("profile.user_page", uid=current_user.uid))
  
  return render_template("private/settings.html", form=form)


@private.route("/inbox")
@login_required
@confirmed_required
def inbox():
  form = MsgSearchForm()

  page = request.args.get("page", 1, type=int)

  if form.validate():
    i_fields = [field for field in Message.__indexing__ if not "receiver" in field]
    s_fields = [field for field in Message.__indexing__ if not "sender" in field]

    i_query = {"multi_match":{"query":form.q.data, "fields":i_fields, "fuzziness":"AUTO:3,6"}}
    s_query = {"multi_match":{"query":form.q.data, "fields":s_fields, "fuzziness":"AUTO:3,6"}}

    i_messages = Message.search(i_query)
    s_messages = Message.search(s_query)

    i_messages = i_messages.filter_by(receiver_id=current_user.id).order_by(Message.created.desc())
    s_messages = s_messages.filter_by(sender_id=current_user.id).order_by(Message.created.desc())
  else:
    i_messages = current_user.msg_received.order_by(Message.created.desc())
    s_messages = current_user.msg_sent.order_by(Message.created.desc())
  
  i_messages = i_messages.paginate(page, current_app.config["RES_PER_PAGE"], error_out=False)
  s_messages = s_messages.paginate(page, current_app.config["RES_PER_PAGE"], error_out=False)

  args = dict(request.args)
  args.pop("page", None)
  args.pop("tab", None)

  return render_template("private/messages.html", i_messages=i_messages, s_messages=s_messages, form=form, query=args)