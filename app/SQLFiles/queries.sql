SELECT artist.name AS artistName, event.name AS eventName, event.date AS eventDate
FROM artist
JOIN event ON artist.id = event.artistID
ORDER BY event.date;

SELECT venue.name AS venueName
FROM venue
LEFT JOIN event ON venue.id = event.venueID
WHERE event.id IS NULL;

