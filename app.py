import sqlite3
from flask import g
from flask import Flask, render_template
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
	# for artist in query_db('SELECT * from artist'):
		# print("the artists are:", artist[1])
	return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run(debug=True)
