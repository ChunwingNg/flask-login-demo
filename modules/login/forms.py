from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
        userN = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
        passW = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
        rememberBox = BooleanField('Remember Me')


class RegisForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    userN = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    passW = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])