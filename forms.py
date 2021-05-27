from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class BandForm(FlaskForm):
    token = StringField('Token', [DataRequired()])
    name = StringField('Name', [DataRequired()])
    submit = SubmitField('Submit')