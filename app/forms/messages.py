from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class MsgContactForm(FlaskForm):
  subject = StringField(label="Subject", validators=[DataRequired(), Length(max=128)])
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  u_uid = HiddenField(label="U_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")


class MsgAboutForm(FlaskForm):
  subject = StringField(label="Subject", validators=[DataRequired(), Length(max=64)])
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  t_uid = HiddenField(label="T_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")


class MsgReplyForm(FlaskForm):
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  r_uid = HiddenField(label="R_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")