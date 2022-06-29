from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class DonateForm(FlaskForm):
  amount = DecimalField(label="Amount", validators=[DataRequired(), NumberRange(1)])
  submit = SubmitField("Donate")

  amount_values = [
    {"value": 2, "text": "2.-", "first": True},
    {"value": 5, "text": "5.-"},
    {"value": 10, "text": "10.-"},
    {"value": 20, "text": "20.-"},
    {"value": 50, "text": "50.-"},
    {"value": 100, "text": "100.-"},
  ]