from django.db import IntegrityError
from flask import Blueprint, render_template, g, session, flash, redirect
from forms import GiveGuessForm
from models import db, connect_db, User, Movie
# CSV Reading
import csv
import pandas as pd
import requests
import random

APIKEY = 'dc9c7e58'

game_bp = Blueprint('game_bp', __name__,
                    template_folder="templates",
                    static_folder="static", static_url_path="assets")
CURR_USER_KEY = "curr_user"


@game_bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# Game main route, this is where players will start. Randomly selects an imdb_id and presents the plot of a film. Plot is uninteractable (Players cannot highlight the text in order to paste it into another window to find the film / answer)


@game_bp.route('/', methods=["GET", "POST"])
def game_home():
    form = GiveGuessForm()
    user = g.user

    # Gather data
    # df = pd.read_csv('csv/movies.csv')
    # imdb_df = df.imdb
    # random_imdb_id = imdb_df[random.randint(0, 1795)]
    # response = requests.get(
    #     f"http://omdbapi.com/?apikey={APIKEY}&i={random_imdb_id}"
    # )
    # data = response.json()

    # Define Variables
    # plot = data["Plot"]
    # title = data["Title"]
    # poster = data["Poster"]
    # year = data["Year"]
    # Parse our data range
    # for source in data['Ratings']:
    #     if source['Source'] == 'Rotten Tomatoes':
    #         actual_score = int(source['Value'][:-1])
    #         actual_score_low = actual_score - 10
    #         actual_score_high = actual_score + 10
    # On form submission, get user input and calculate whether user was within +/- 10 of the actual score
    if form.validate_on_submit():
        user_input = int(form.guess.data)
        # score_range = range(actual_score_low, actual_score_high)

        # if user_input in score_range:
        #     user.score = user.score + 10
        #     db.session.commit()
        #     return redirect("/movie/{data.imdb}")
            # return render_template("answer.html", title=title, plot=plot, year=year, poster=poster, actual_score=actual_score)

    return render_template('game.html', plot=plot, form=form, user=user, title=title, actual_score=actual_score, actual_score_low=actual_score_low)


@game_bp.route('/movie/<int:movie_id>', methods=["GET", "POST"])
def game_answer_page(movie_id):
    """Show Movie Page"""
    movie = Movie.query.get_or_404(movie_id)
    response = requests.get(
        f"http://omdbapi.com/?apikey={APIKEY}&i={movie.imdb}"
    )
    data = response.json()
    plot = data["Plot"]
    poster = data["Poster"]

    return render_template('movie.html', movie=movie, plot=plot, poster=poster)
