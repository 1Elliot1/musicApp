from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, SelectField, SelectMultipleField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app import app

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    reauth = PasswordField('Reenter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Already Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Already In Use')


class addArtistForm(FlaskForm):
    artistName = StringField('Artist Name:', validators=[DataRequired()])
    artistHomeTown = StringField('Artist Hometown:', validators=[DataRequired()])
    artistBio = StringField('Artist Bio:')
    submit = SubmitField()

class addVenueForm(FlaskForm):
    venueName = StringField('Venue Name:', validators=[DataRequired()])
    venueLocation = StringField('Venue Location:', validators=[DataRequired()])
    submit = SubmitField()

class addEventForm(FlaskForm):
    eventName = StringField('Event Name:', validators=[DataRequired()])
    eventVenue = SelectField('Event Venue:', coerce=int)
    eventArtists = SelectMultipleField('Event Artists:', coerce=int)
    eventDate= DateField('Event Start Time:', format='%Y-%m-%d')
    #Make price to int and a default value of zero if free:
    eventPrice = StringField('Ticket Price ("Free" if No Fee):',[DataRequired()])
    submit = SubmitField()
