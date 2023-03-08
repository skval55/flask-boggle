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
    
    table = boggle_game.make_board()
    return render_template("index.html", table=table)


