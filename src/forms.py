from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    FormField, DecimalField, IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LocationForm(FlaskForm):
    latitude = DecimalField('Latitude', validators=[])

    longitude = DecimalField('Longitude', validators=[])

    city = StringField('City', validators=[DataRequired()])

    zipcode = IntegerField('Zip', validators=[Length(max=5)])


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    location = FormField(LocationForm)

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')
