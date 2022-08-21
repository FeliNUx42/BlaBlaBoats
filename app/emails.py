from flask import current_app, url_for
from requests import request
from sendgrid.helpers.mail import Mail, Email, To, Content


def send_confirm_email(user, command="confirm_email"):
  subject = "BlaBlaBoat: Verify Email"

  token = user.get_token(command)

  with open("app/templates/emails/compiled/confirm.html", "r") as f:
    html = f.read()
    html = html.replace("CONFIRM_LINK", url_for("auth.confirm_account", token=token, _external=True))
    html = html.replace("CONTACT_LINK", url_for("home.index", _external=True))

  msg = Mail(
    from_email=current_app.config["SENDGRID_EMAIL"],
    to_emails=user.email,
    subject=subject,
    html_content=html
  )

  current_app.sendgrid.send(msg)

def send_reset_email(user, command="reset_password"):
  subject = "BlaBlaBoat: Reset Password"

  token = user.get_token(command)

  with open("app/templates/emails/compiled/reset.html", "r") as f:
    html = f.read()
    html = html.replace("RESET_LINK", url_for("auth.reset_password", token=token, _external=True))
    html = html.replace("CONTACT_LINK", url_for("home.index", _external=True))

  msg = Mail(
    from_email=current_app.config["SENDGRID_EMAIL"],
    to_emails=user.email,
    subject=subject,
    html_content=html
  )

  current_app.sendgrid.send(msg)

  