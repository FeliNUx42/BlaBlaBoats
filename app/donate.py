from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from .forms.donate import DonateForm
import locale


locale.setlocale(locale.LC_MONETARY, 'de_CH.UTF-8')
donate = Blueprint("donate", __name__)

@donate.route("/", methods=["GET", "POST"])
def donate_page():
  form = DonateForm()
  
  if form.validate_on_submit():
    amount = int(float(form.amount.data) * 100)
    user_uid = current_user.uid if current_user.is_authenticated else "null"

    session = current_app.stripe.checkout.Session.create(
      success_url=url_for("donate.success", _external=True) + "?id={CHECKOUT_SESSION_ID}",
      cancel_url=url_for("donate.cancel", _external=True),
      payment_method_types=["card"],
      submit_type="donate",
      line_items=[{
        "amount" : amount,
        "currency" : "chf",
        "quantity" : 1,
        "name" : "Donation",
        "images" : ["https://picsum.photos/300/300?random=4"]
      }],
      payment_intent_data={
        "metadata" : {
          "user_uid" : user_uid
        }
      },
      metadata={
        "user_uid" : user_uid
      }
    )

    return redirect(session["url"])

  return render_template("main/donate.html", form=form)


@donate.route("/success")
def success():
  session = current_app.stripe.checkout.Session.retrieve(request.args["id"])

  value = locale.currency(session.amount_total / 100)
  flash(f"Thank you for donating {value} to BlaBlaBoat.", "success")

  return redirect(url_for("donate.donate_page"))


@donate.route("/cancel")
def cancel():
  flash("Unfortunately the donation was aborted. Please try again.", "danger")

  return redirect(url_for("donate.donate_page"))