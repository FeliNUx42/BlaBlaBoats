from crypt import methods
from email.mime import message
from flask import Blueprint, render_template, redirect, request, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from PIL import Image as PImage
from .models import User, Message, Trip
from .forms import MsgAboutForm, MsgContactForm, MsgReplyForm
from . import db
import os
import re


messages = Blueprint("messages", __name__)

@messages.route("/<uid>")
@login_required
def msg(uid):
  message = Message.query.filter_by(uid=uid).first_or_404()
  form = MsgReplyForm()

  return render_template("private/message.html", message=message, form=form, Trip=Trip)

@messages.route("/contact", methods=["POST"])
@login_required
def contact():
  form = MsgContactForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.subject = form.subject.data
    m.text = form.content.data

    m.sender = current_user
    rcv = User.query.filter_by(uid=form.u_uid.data).first()
    if not rcv:
      abort(500)
    m.receiver = rcv

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")
  return redirect(request.referrer)

@messages.route("/about", methods=["POST"])
@login_required
def about():
  form = MsgAboutForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.subject = form.subject.data
    m.text = form.content.data

    m.sender = current_user
    t = Trip.query.filter_by(uid=form.t_uid.data).first()
    if not t:
      abort(500)
    m.trip = t
    m.receiver = t.skipper

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")
  return redirect(request.referrer)

@messages.route("/reply", methods=["POST"])
@login_required
def reply():
  form = MsgReplyForm()

  if form.validate_on_submit():
    m = Message()
    m.uid = os.urandom(8).hex()
    m.text = form.content.data
    m.sender = current_user
    rep = Message.query.filter_by(uid=form.r_uid.data).first()
    if not rep:
      abort(500)
    m.reply = rep
    m.receiver = rep.sender
    m.subject = "Re: " + rep.subject
    m.subject = "Re: " + re.sub("^Re: ", "", rep.subject)

    db.session.add(m)
    db.session.commit()

    flash("Message sent successfully.", "success")
  return redirect(request.referrer)
    