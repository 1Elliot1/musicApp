from flask import render_template, flash, redirect, request, session, url_for, Flask
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import addArtistForm, LoginForm, RegistrationForm, addVenueForm, addEventForm
from app.models import User, Artist, Event, Venue, ArtistToEvent
import csv

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/artists')
@login_required
def artists():
    artists = Artist.query.all()
    return render_template('artistList.html', artists=artists)

@app.route('/artist/<name>')
@login_required
def artist(name):
    #query the database for first result of passed name
    artist = Artist.query.filter_by(name=name).first()
    if artist:
        return render_template('artist.html', artist=artist)
    else:
        flash(f"Error: Artist {name} Not Found")
        return redirect(url_for('artists'))

@app.route('/addArtist', methods=['GET','POST'])
@login_required
def addArtist():
    form = addArtistForm()
    flashMessage = None
    artistData = {}
    
    if form.validate_on_submit():
        artistData = {
            'artistName': form.artistName.data,
            'artistHomeTown': form.artistHomeTown.data,
            'artistBio': form.artistBio.data
        }
        checkName = Artist.query.filter_by(name=artistData['artistName']).first()
        if checkName:
            flash("An Artist With This Name Already Exists")
        else:
            newArtist = Artist(name=artistData["artistName"], hometown=artistData["artistHomeTown"], bio=artistData["artistBio"])
            db.session.add(newArtist)
            flashMessage = f"Artist Creation Requested for Artist {artistData['artistName']}"
            db.session.commit()
            return redirect(url_for('artists'))
    return render_template('addArtist.html', title="Add Artist", form=form, flashMessage = flashMessage, artistData = artistData)

@app.route('/addVenue', methods=['GET', 'POST'])
@login_required
def addVenue():
    form = addVenueForm()
    flashMessage = None
    venueData = {}

    if form.validate_on_submit():
        venueData = {
            'venueName': form.venueName.data,
            'venueLocation': form.venueLocation.data
        }
        checkName = Venue.query.filter_by(name=venueData['venueName']).first()
        if checkName:
            flash("A Venue With This Name Already Exists")
        else:
            newVenue = Venue(name=venueData['venueName'], location=venueData['venueLocation'])
            db.session.add(newVenue)
            flashMessage = f"Venue Creation Requested for {venueData['venueName']}"
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('addVenue.html', title="Add Venue", form=form, flashMessage=flashMessage, venueData=venueData)

@app.route('/addEvent', methods=['GET','POST'])
@login_required
def addEvent():
    form = addEventForm()
    form.eventVenue.choices = [(v.id, v.name) for v in Venue.query.all()]
    form.eventArtists.choices = [(a.id,  a.name) for a in Artist.query.all()]
    flashMessage = None
    eventData = {}
    
    if form.validate_on_submit():
        eventData = {
            'eventName': form.eventName.data,
            'eventVenue': form.eventVenue.data,
            'eventArtists': form.eventArtists.data,
            'eventDate': form.eventDate.data,
            'eventPrice': form.eventPrice.data
        }
        checkName = Event.query.filter_by(name=eventData['eventName']).first()
        if checkName:
            flash("An Event With This Name Already Exists")
        else:
            newEvent = Event(name=eventData['eventName'], date=(eventData['eventDate']), price=(eventData['eventPrice']))
            for artistID in eventData['eventArtists']:
                newEvent.artists.append(Artist.query.get(artistID))
            Venue.query.get(eventData['eventVenue']).events.append(newEvent)
            db.session.add(newEvent)
            flashMessage = f"Event Creation Requested for {eventData['eventName']}"
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('addEvent.html', title="Add Event", form=form, flashMessage=flashMessage, eventData=eventData)    

@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating")
    # clear all data from all tables
    #grabs all data from the tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    #Add all artist data
    artistData = 'app/dataFiles/artists.csv'
    with open(artistData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            #not sure about relationships here, may be automatic 
            item = Artist(name=row[1], hometown=row[2], bio=row[3]) 
            db.session.add(item)
    #populate event data
    eventData = 'app/dataFiles/events.csv'
    with open(eventData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            item = Event(name=row[1], date=row[2], price=row[3])
            db.session.add(item)
    venueData = 'app/dataFiles/venues.csv'
    with open(venueData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            item = Venue(name=row[1], location=row[2])
            db.session.add(item)
    db.session.commit()
    #adding relationships
    #querying 10th event, appending Artist10...to artists attribute in ArtistToEvent
    #change to query by name at some point for ids
    event = Event.query.filter_by(name="X Punk Night").first()
    artist1=Artist.query.filter_by(name="Dead Kennedys").first()
    artist2=Artist.query.filter_by(name="Bad Brains").first()
    artist3=Artist.query.filter_by(name="X").first()
    event.artists.append(artist1)
    event.artists.append(artist2)
    event.artists.append(artist3)

    event = Event.query.filter_by(name="Misfits Halloween Bash").first()
    event.artists.append(Artist.query.filter_by(name="The Misfits").first())
    event.artists.append(Artist.query.filter_by(name="The Damned").first())

    # Corrected code for the third case:
    event = Event.query.filter_by(name="Sex Pistols Reunion").first()
    event.artists.append(Artist.query.filter_by(name="Sex Pistols").first())

    venue = Venue.query.filter_by(name="CBGB").first()
    venue.events.append(Event.query.filter_by(name="Misfits Halloween Bash").first())
    venue.events.append(Event.query.filter_by(name="Sex Pistols Reunion").first())
    venue.events.append(Event.query.filter_by(name="Dead Kennedys Live").first())

    db.session.commit()
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            flash('ERROR: Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #TODO: Add a next function to allow users to renavigate back to where they wanted to login from
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
