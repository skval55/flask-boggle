from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/', methods=["GET", 'POST'])
def make_html_table():
    """makes the table from boggle.make_board into an html table and 
    sets the table in the session"""
    max_score = session.get("max_score", 0)
    times_played = session.get("times_played", 0)
    table = boggle_game.make_board()
    session['table'] = table
    return render_template("index.html", table=table, max_score=max_score, times_played=times_played )


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    print(word)
    table = session["table"]
    response = boggle_game.check_valid_word(table, word)
    print(response)

    return jsonify({'result': response})

@app.route("/get-score", methods=['POST'])
def post_score():
    """send a response to the front end containing 
    the max score, if it is new and times played"""
    score = request.json['score']
    times_played = session.get("times_played", 0)
    session['times_played'] = times_played + 1
    resp = new_max_score(score)
    return (jsonify({"score": session['max_score'], "new_highscore": resp, "times": session['times_played'] }))

def new_max_score(score):
    """checks to see if score is new highscore and updates highscore
    

    >>> new_max_score(10)
    'new high score'

    session[max_score] == 10
   
    >>> new_max_score(5)
    "nice try, but no high score"
    
    >>> new_max_score(10)
    "nice try, but no high score"
    
    """
    max_score = session.get("max_score", 0)
    if score > max_score :
        max_score= int(score)
        resp = "new high score"
    else:
        resp = "nice try, but no high score"
    session['max_score'] = max(score, max_score)
    return resp