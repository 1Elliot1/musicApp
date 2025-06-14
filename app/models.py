from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True, unique = True)
    email = db.Column(db.String(64), index = True, unique = True)
    passwordHash = db.Column(db.String(128), index = True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    def checkPassword(self, hash):
        return check_password_hash(self.passwordHash, hash)

@login.user_loader
def loadUser(id):
    return User.query.get(int(id))

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    hometown = db.Column(db.String(64), index = True)
    bio = db.Column(db.String(256), index = True, unique = True)
    events = db.relationship('Event', secondary = 'Artist2Event', backref='artist', lazy='dynamic')

    #print class to console
    def __repr__(self):
        return '<Artist {}>'.format(self.name)

class Event(db.Model):
    __tablename__  = 'event'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    date = db.Column(db.String(64), index = True)
    price = db.Column(db.String(64), index = True)
    venues = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artists = db.relationship('Artist', secondary = 'Artist2Event', backref='event', lazy='dynamic')

    def __repr__(self):
        return '<Event {}>'.format(self.name)

class Venue(db.Model):
    __tablename__  = 'venue'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    location = db.Column(db.String(128), index = True)
    events = db.relationship('Event', backref='venue', lazy='dynamic')

    def __repr__(self):
        return '<Venue {}>'.format(self.name)

class ArtistToEvent(db.Model):
    __tablename__ = 'Artist2Event'

    id = db.Column(db.Integer, primary_key=True)
    artistID = db.Column(db.Integer, db.ForeignKey("artist.id"))
    eventID = db.Column(db.Integer, db.ForeignKey("event.id"))

class EventToVenue(db.Model):
    __tablename__ = 'Event2Venue'

    id =  db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey("event.id"))
    venueID = db.Column(db.Integer, db.ForeignKey("venue.id"))



