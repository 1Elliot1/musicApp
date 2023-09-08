from flask import render_template
from app import app

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

@app.route('/addArtist.html')
def addArtist():
    return render_template('addArtist.html')