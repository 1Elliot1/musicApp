from flask import render_template, flash, redirect, request, session, url_for
from app import app, db
from app.forms import addArtistForm
from app.models import Artist, Event, Venue, ArtistToEvent
import csv

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('artistList.html', artists=artists)

@app.route('/artist/<name>')
def artist(name):
    #query the database for first result of passed name
    artist = Artist.query.filter_by(name=name).first()
    if artist:
        return render_template('artist.html', artist=artist)
    else:
        flash(f"Error: Artist {name} Not Found")
        return redirect(url_for('artists'))

@app.route('/addArtist', methods=['GET','POST'])
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
