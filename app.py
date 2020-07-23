# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import session
import os
import bcrypt
from flask import flash

# -- Initialization section --
app = Flask(__name__)

app.secret_key = "brunomars"

# name of database
app.config['MONGO_DBNAME'] = 'music'

MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.4lc7f.mongodb.net/music?retryWrites=true&w=majority'



mongo = PyMongo(app)


# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    session['error'] = ""
    return render_template('template.html')


# ADD SONGS

# @app.route('/add')

# def add():
#     # define a variable for the collection you want to connect to
#     music = mongo.db.music
    
#     # use some method on that variable to add/find/delete data

#     music.insert({"song" : "Uptown Funk",
#                 "artist": 'Bruno Mars',
#                 "description": "it's catchy"})
#     music.insert({"song" : "Power",
#                 "artist": 'Kanye West',
#                 "description": "it's powerful"})
#     music.insert({"song" : "Bad Blood",
#                 "artist": 'Taylor Swift',
#                 "description": "it's good for bad blood"})
#     music.insert({"song" : "Wish the Worst",
#                 "artist": 'Thouxanbanfauni',
#                 "description": "it's got a great beat"})
#     music.insert({"song" : "Mercy",
#                 "artist": 'Shawn Mendes',
#                 "description": "it's pretty cool"})
#     # music.insert({"song": "Uptown Funk"})

#     # return a message to the user (or pass data to a template)
    # return "song added"


# SHOW A LIST OF ALL SONG TITLES

@app.route('/show')

def show():
    mus = mongo.db.music
    musiclist= mus.find({}).sort("song", 1)
    # musiclist= mus.find({}).sort("artist", 1)
    #musiclist= mus.find({})[:3].sort("artist", 1)
    return render_template("show.html", music=musiclist)

@app.route('/usershow')
def usershow():
    try: 
        if session['username'] != None and len(session['username']) >=1:
            mus = mongo.db.music
            musiclist= mus.find({'user':session['username']}).sort("song", 1)
            # musiclist= mus.find({}).sort("artist", 1)
            #musiclist= mus.find({})[:3].sort("artist", 1)
            return render_template("show.html", music=musiclist)
    except:
        return render_template("login.html")

# ADVANCED: A FORM TO COLLECT USER-SUBMITTED SONGS

@app.route('/userinput')
def userinput():
    return render_template("userinput.html")

@app.route('/sendSong', methods = ['GET', 'POST'])
def sendSong():
    if request.method == 'GET':
        return "you are getting some info"
    else:
        try:
            if session['username'] != None and len(session['username']) >=1:
                songName = request.form['song_name']
                artistName = request.form['artist_name']
                descrip = request.form['description']
                music = mongo.db.music
                music.insert({"song" : songName,
                        "artist": artistName,
                        "description": descrip,
                        "user": session['username']})
                mus = mongo.db.music
                musiclist= mus.find({}).sort("song", 1)
                return render_template("show.html", music=musiclist)
        except:
            return render_template("login.html")


# DOUBLE-ADVANCED: SHOW ARTIST PAGE

@app.route('/artistpage/<artist>')
def artistpage(artist):
    mus = mongo.db.music
    artistlist= mus.find({'artist':artist})
    return render_template("artist.html", music=artistlist)



# TRIPLE-ADVANCED: SHOW SONG PAGE

@app.route('/song/<id>')
def song(id):
    mus = mongo.db.music
    song= list(mus.find({'_id':ObjectId(id)}))

    return render_template("songpage.html", music=song[0])


@app.route('/artist', methods = ['GET', 'POST'])
def artist():
    if request.method == 'GET':
        return "you are getting some info"
    else:
        mus = mongo.db.music
        artistlist= mus.find({'artist':request.form['artist_name']})
        return render_template("artist.html", music=artistlist)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logintomongo', methods = ['GET', 'POST'])
def logintomongo():
    users = mongo.db.users
    given_username = request.form['username']
    given_password = bcrypt.hashpw(request.form['password'].encode("utf-8"),bcrypt.gensalt())
    print(given_password)
    if request.method == 'GET':
        return "you are getting some info"
    else:
        if not list(users.find({'username':given_username})):
            users.insert({"username" : given_username,"password": str(given_password,'utf-8')})
            session['username'] = given_username
            return render_template("template.html")
        else:
            if list(users.find({'username':given_username}))[0]['password'] == str(given_password,'utf-8'):
                session['username'] = given_username
                return render_template('template.html')
            else:
                session['error'] = "username already taken"
                return render_template('login.html')

@app.route('/logout')
def logout():
    # session['username'] = None
    session.clear()
    return render_template('template.html')