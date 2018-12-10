import sqlite3
from flask import g
from flask import Flask, render_template, request
import os
app = Flask(__name__)

DATABASE = os.path.abspath('final_project.db')

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

@app.route('/')
def index():
	# Example of how to query in the database, delete later
	# for artist in query_db('SELECT * from artist') :
		# print("the artists are:", artist[1])
        table_data = query_db('SELECT * from artist')
        return render_template('index.html', data=table_data) #TODO: we only want hottest 100

@app.route('/receivedSortings', methods = ['POST'])
def fetchPlaylist():
    if request.method == 'POST':
        data = request.json

        for artist in data:
            print("query the songs for artist id: " + artist)

    return render_template('hello.html') #TODO replace with html file for the returned playlist page


if __name__ == '__main__':
    app.run(debug=True)
