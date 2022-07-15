from click import confirm
from flask import Blueprint, render_template, redirect, request, flash, abort
from flask_login import login_required, current_user
from .models import User, Message, Trip
from .tools import confirmed_required
from .forms.messages import MsgAboutForm, MsgContactForm, MsgReplyForm
from . import db
import os, re


messages = Blueprint("messages", __name__)

@messages.route("/<uid>")
@login_required
@confirmed_required
def msg(uid):
  form = MsgReplyForm()
  message = Message.query.filter_by(uid=uid).first_or_404()

  if not current_user in (message.sender, message.receiver):
    abort(403)
  
  if current_user == message.receiver:
    message.read = True
    db.session.commit()

  return render_template("private/message.html", message=message, form=form)


@messages.route("/contact", methods=["POST"])
@login_required
@confirmed_required
def contact():
  form = MsgContactForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.subject = form.subject.data
    m.text = form.content.data

    m.sender = current_user
    receiver = User.query.filter_by(uid=form.u_uid.data, confirmed=True).first()
    if not receiver or current_user == receiver:
      abort(500)
    m.receiver = receiver

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")

  return redirect(request.referrer)


@messages.route("/about", methods=["POST"])
@login_required
@confirmed_required
def about():
  form = MsgAboutForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.subject = form.subject.data
    m.text = form.content.data

    m.sender = current_user
    trip = Trip.query.filter_by(uid=form.t_uid.data).first()
    if not trip or trip.skipper == current_user:
      abort(500)
    m.trip = trip
    m.receiver = trip.skipper

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")

  return redirect(request.referrer)


@messages.route("/reply", methods=["POST"])
@login_required
@confirmed_required
def reply():
  form = MsgReplyForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.text = form.content.data

    m.sender = current_user
    replying_to = Message.query.filter_by(uid=form.r_uid.data).first()
    if not replying_to or replying_to.sender == current_user:
      abort(500)
    m.reply = replying_to
    m.receiver = replying_to.sender

    m.subject = "Re: " + replying_to.subject
    m.subject = "Re: " + re.sub("^Re: ", "", replying_to.subject)

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")

  return redirect(request.referrer)
    