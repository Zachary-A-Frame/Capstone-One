from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.html5 import NumberInput


class GiveGuessForm(FlaskForm):
    """Form for users to submit guess"""

    guess = StringField('Guess!', widget=NumberInput(), render_kw={'max': "100", 'min': '0'}, validators=[
                        DataRequired(), Length(min=0, max=3)])
    movie_id = HiddenField("Movie Id")

class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)])
