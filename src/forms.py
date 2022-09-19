from flask_wtf import FlaskForm
from models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(
                min=1,
                max=20,
                message='Username must be between %(min)d and %(max)d characters long.',
            )
        ],
    )
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=6, message='Password must be %(min)d or more characters.'),
            EqualTo('confirm', message='Passwords must match.'),
        ],
    )
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
