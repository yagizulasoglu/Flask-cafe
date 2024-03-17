"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, Length, Email

class CafeInfoForm(FlaskForm):
    """Form for adding/editing info about a cafe."""

    name = StringField(
        'Name',
        validators=[InputRequired()]
    )

    description = StringField(
        'Description',
        validators=[Optional()]
    )

    url = StringField(
        'URL',
        validators=[Optional(), URL()]
    )

    address = StringField(
        'Address',
        validators=[InputRequired()]
    )

    city_code = SelectField(
        'City Code',
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), Length(max=255)]
    )

    specialities = StringField(
        'Specialties',
        default="",
        validators=[Optional(),  Length(max=100)],
    )

class SignupForm(FlaskForm):
    """Form for user signup"""

    username = StringField(
        'Username',
        validators=[InputRequired()]
    )

    first_name = StringField(
        'First Name',
        validators=[InputRequired()]
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired()]
    )

    description = StringField(
        'Description',
        validators=[Optional()]
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), Length(max=255)]
    )

class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )


class ProfileEditForm(FlaskForm):
    """Form for user signup"""

    first_name = StringField(
        'First Name',
        validators=[InputRequired()]
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired()]
    )

    description = StringField(
        'Description',
        validators=[Optional()]
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), Length(max=255)]
    )


class CsrfForm(FlaskForm):
    """For actions where we want CSRF protection, but don't need any fields."""