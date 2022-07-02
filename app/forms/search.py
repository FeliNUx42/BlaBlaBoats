from flask import request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange


class SearchForm(FlaskForm):
  q = StringField("Search", validators=[Optional()])
  lat = DecimalField(validators=[Optional()])
  lng = DecimalField(validators=[Optional()])
  dist = IntegerField(label="Max. distance to location", validators=[Optional(), NumberRange(min=0, max=3000)])
  unit = SelectField(choices=("km", "mi", "nmi"), validators=[DataRequired()])
  start_date = DateField(validators=[Optional()])
  end_date = DateField(validators=[Optional()])
  boat_type = SelectField(label="Boat type", choices=("All", "Sailingboat", "Motorboat"), validators=[DataRequired()])
  sailing_mode = SelectField(label="Sailing mode", choices=("All", "Costal", "Offshore", "Regatta", "Boat Delivery"), validators=[DataRequired()])
  sort_by = SelectField(label="Sort by", choices=("Most relevant", "Nearest to location", "Alphabetically, A-Z", "Alphabetically, Z-A", "Created, new to old", "Created, old to new"), validators=[Optional()])
  results_per_page = IntegerField(label="Results per page", validators=[Optional(), NumberRange(min=0, max=100)], default=lambda:current_app.config["RES_PER_PAGE"])

  def __init__(self, *args, **kwargs):
    if 'formdata' not in kwargs:
      kwargs['formdata'] = request.args
    if 'meta' not in kwargs:
      kwargs['meta'] = {'csrf': False}
      super(SearchForm, self).__init__(*args, **kwargs)


class MsgSearchForm(FlaskForm):
  q = StringField(label="Search for messages...", validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    if 'formdata' not in kwargs:
      kwargs['formdata'] = request.args
    if 'meta' not in kwargs:
      kwargs['meta'] = {'csrf': False}
      super(MsgSearchForm, self).__init__(*args, **kwargs)