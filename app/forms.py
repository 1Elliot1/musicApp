from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import app

class addArtistForm(FlaskForm):
    artistName = StringField('Artist Name:', validators=[DataRequired()])
    artistHomeTown = StringField('Artist Hometown:', validators=[DataRequired()])
    artistBio = StringField('Artist Bio:')

    submit = SubmitField()
    
