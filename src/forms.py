from flask_wtf import FlaskForm
from models import User
from wtforms import BooleanField, FieldList, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, NumberRange, StopValidation, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            InputRequired(message='Username is required.'),
            Length(
                min=1,
                max=20,
                message='Username must be between %(min)d and %(max)d characters long.',
            ),
        ],
    )
    password = PasswordField(
        'New Password',
        validators=[
            InputRequired(message='Password is required.'),
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
    username = StringField('Username', validators=[InputRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[InputRequired(message='Password is required.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ListForm(FlaskForm):
    rank = FieldList(
        IntegerField(
            'Rank',
            validators=[
                InputRequired(message='Rank is required.'),
                NumberRange(min=0, message='Rank must be greater than or equal to 0.'),
                NumberRange(max=99999, message='Rank must be less than or equal to 5 characters.'),
            ],
        ),
    )
    content = FieldList(
        StringField(
            'Content',
            validators=[
                Length(max=5, message='Content must be less than or equal to 80 characters.'),
            ],
        ),
    )
    comment = FieldList(
        StringField(
            'Comment',
            validators=[
                Length(max=5, message='Comment must be less than or equal to 255 characters.'),
            ],
        ),
    )
    submit = SubmitField('Done')
