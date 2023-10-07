from flask import render_template, flash, redirect, request, session
from app import app, db
from app.forms import addArtistForm
from app.models import Artist, Event, Venue, ArtistToEvent
import csv
from pandas import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/artists')
def artists():
    Artists = [
        {
            'artistName': 'Rancid',
            'bio': 'N/A',
            'homeTown': 'Albany, California',
            'events': 'Music4Cancer 2023'
        },
        {
            'artistName': 'Descendants',
            'bio': 'N/A',
            'homeTown': 'Manhattan Beach, California',
            'events': 'New Jersey Concert'
        },
        {
            'artistName': 'AntiFlag',
            'bio': 'N/A',
            'homeTown': 'Pittsburgh, Pennsylvania',
            'events': 'California Concert'
        }
    ]
    return render_template('artistList.html', Artists=Artists)

@app.route('/artist1')
def artist1():
    Artists = [
    {
        'artistName': 'Rancid',
        'bio': 'N/A',
        'homeTown': 'Albany, California',
        'events': 'Music4Cancer 2023'
    }]
    return render_template('artist1.html', Artists=Artists)

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
        session['artistData'] = artistData
        flashMessage = "Artist Creation Requested for Artist {}".format(form.artistName.data)
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
    artistData = read_csv('dataFiles/artists.csv')
    with open(artistData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            #not sure about relationships here, may be automatic 
            item = Artist(id=row[0], name=row[1], hometown=row[2], bio=row[3]) 
            db.session.add(item)
    #populate event data
    eventData = read_csv('dataFiles/events.csv')
    with open(eventData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            item = Event(id=row[0], name=row[1], date=row[2], price=row[3])
            db.session.add(item)
    venueData = read_csv('dataFiles/venues.csv')
    with open(venueData, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            item = Venue(id=row[0], name=row[1], location=row[2])
            db.session.add(item)

    #adding relationships
    #querying 10th event, appending Artist10...to artists attribute in ArtistToEvent
    Event.query.get(10).artists.append(Artist.query.get(10))
    Event.query.get(10).artists.append(Artist.query.get(7))
    Event.query.get(10).artists.append(Artist.query.get(3))

    Event.query.get(1).artists.append(Artist.query.get(1))
    Event.query.get(1).artists.append(Artist.query.get(5))

    Event.query.get(2).artists.append(Artist.query.get(2))

    Venue.query.get(1).events.append(Event.query.get(10))
    Venue.query.get(1).events.append(Event.query.get(1))
    Venue.query.get(1).events.append(Event.query.get(2))

    db.session.commit()

