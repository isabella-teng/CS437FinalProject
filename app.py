import sqlite3
from flask import g
from flask import Flask, render_template, request, redirect, url_for
import os
import random
app = Flask(__name__)

DATABASE = os.path.abspath('final_project1.db')

# Source: Flask Sqlite3 Documentation
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Source: Flask Sqlite3 Documentation
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def playlistAlgorithm(artists):
    # Algorithm:
    # Get user's input of 5 sorted artists
    # Example of the first ranked artist: Get all artists that are familiar to Artist #1 -> Rank the songs by familiarity and output 10 of them
    # Get artists' similar_to artist
    # Output 30 recommended songs
    # input - lst, list of 5 sorted artist ids (1 being favorite, 5 being least favorite)
    playlist = []
    artist1 = artists[0]
    # print(artist1)
    artist2 = artists[1]
    artist3 = artists[2]
    artist4 = artists[3]
    artist5 = artists[4]

    # ARTIST 1:
    similar_artists_id_1 = []
    i = 0
    similar_artists_1 = query_db('select * from artist where id in (select artist2_id from similar_to where artist1_id = (?)) ORDER BY familiarity DESC', (artist1,))
    # print(similar_artists_1)
    if len(similar_artists_1) >= 10:
        for row in similar_artists_1[0:10]:
            similar_artists_id_1.append(row[0]) # row[0] = 'id'
    else:
        for row in similar_artists_1:
            similar_artists_id_1.append(row[0]) # row[0] = 'id'
            i += 1
        while len(similar_artists_id_1) < 10:
            for x in range(i):
                similar_artists_id_1.append(similar_artists_id_1[x])
                if len(similar_artists_id_1) == 10:
                    break

    for s in similar_artists_id_1:
        similar_artist_query = query_db('select * from sings where artist_id = (?)', (s,))
        playlist.append(random.choice(similar_artist_query)[0]) # 'track_id'

    # ARTIST 2:
    similar_artists_id_2 = []
    i = 0
    similar_artists_2 = query_db('select * from artist where id in (select artist2_id from similar_to where artist1_id = (?)) ORDER BY familiarity DESC', (artist2,))
    if len(similar_artists_2) >= 8:
        for row in similar_artists_2[0:8]:
            similar_artists_id_2.append(row[0])
    else:
        for row in similar_artists_2:
            similar_artists_id_2.append(row[0])
            i += 1
        while len(similar_artists_id_2) < 8:
            for x in range(i):
                similar_artists_id_2.append(similar_artists_id_2[x])
                if len(similar_artists_id_2) == 8:
                    break

    for s in similar_artists_id_2:
        similar_artist_query = query_db('select * from sings where artist_id = (?)', (s,))
        playlist.append(random.choice(similar_artist_query)[0])

    # ARTIST 3:
    similar_artists_id_3 = []
    i = 0
    similar_artists_3 = query_db('select * from artist where id in (select artist2_id from similar_to where artist1_id = (?)) ORDER BY familiarity DESC', (artist3,))
    if len(similar_artists_3) >= 6:
        for row in similar_artists_3[0:6]:
            similar_artists_id_3.append(row[0])
    else:
        for row in similar_artists_3:
            similar_artists_id_3.append(row[0])
            i += 1
        while len(similar_artists_id_3) < 6:
            for x in range(i):
                similar_artists_id_3.append(similar_artists_id_3[x])
                if len(similar_artists_id_3) == 6:
                    break

    for s in similar_artists_id_3:
        similar_artist_query = query_db('select * from sings where artist_id = (?)', (s,))
        playlist.append(random.choice(similar_artist_query)[0])

    # ARTIST 4:
    similar_artists_id_4 = []
    i = 0
    similar_artists_4 = query_db('select * from artist where id in (select artist2_id from similar_to where artist1_id = (?)) ORDER BY familiarity DESC', (artist4,))
    if len(similar_artists_4) >= 4:
        for row in similar_artists_4[0:4]:
            similar_artists_id_4.append(row[0])
    else:
        for row in similar_artists_4:
            similar_artists_id_4.append(row[0])
            i += 1
        while len(similar_artists_id_4) < 4:
            for x in range(i):
                similar_artists_id_4.append(similar_artists_id_4[x])
                if len(similar_artists_id_4) == 4:
                    break

    for s in similar_artists_id_4:
        similar_artist_query = query_db('select * from sings where artist_id = (?)', (s,))
        playlist.append(random.choice(similar_artist_query)[0])

    # ARTIST 5:
    similar_artists_id_5 = []
    i = 0
    similar_artists_5 = query_db('select * from artist where id in (select artist2_id from similar_to where artist1_id = (?)) ORDER BY familiarity DESC', (artist5,))
    if len(similar_artists_5) >= 2:
        for row in similar_artists_5[0:2]:
            similar_artists_id_5.append(row[0])
    else:
        for row in similar_artists_5:
            similar_artists_id_5.append(row[0])
            i += 1
        while len(similar_artists_id_5) < 2:
            for x in range(i):
                similar_artists_id_5.append(similar_artists_id_5[x])
                if len(similar_artists_id_5) == 2:
                    break

    for s in similar_artists_id_5:
        similar_artist_query = query_db('select * from sings where artist_id = (?)', (s,))
        playlist.append(random.choice(similar_artist_query)[0])

    playlist_wo_duplicates = list(set(playlist))
    return playlist_wo_duplicates


@app.route('/')
def index():
    table_data = query_db('SELECT * from artist ORDER BY hotness DESC LIMIT 100')
    return render_template('index.html', data=table_data)


@app.route('/receivedSortings', methods = ['GET','POST'])
def fetchPlaylist():
    if request.method == 'POST':
        rankings = request.json
        rankingsID = []
        for ranking in rankings:
            rankingsID.append(ranking[0])
        playlist = playlistAlgorithm(rankingsID)
        playlistSongs = []
        for songID in playlist:
            songName = query_db('SELECT title from song where id=(?)', (songID,))
            playlistSongs.append(songName[0][0])
        print(playlistSongs)
    return returnPlaylist(playlistSongs)

@app.route('/results')
def returnPlaylist(songs):
    print("here")
    return render_template('recommendations.html', songs=songs)



if __name__ == '__main__':
    app.run(debug=True)
