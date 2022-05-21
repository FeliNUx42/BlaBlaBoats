from flask import Blueprint, render_template, redirect, request, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from PIL import Image as PImage
from .models import User, Message
from .forms import ContactForm, SettingsForm
from . import db
import os


messages = Blueprint("messages", __name__)

@messages.route("/<uid>")
@login_required
def msg(uid):
  message = Message.query.filter_by(uid=uid).first()
  #message = Message.query.filter_by(uid=uid).first_or_404()
  form = ContactForm()

  return render_template("messages/message.html", message=message, form=form)