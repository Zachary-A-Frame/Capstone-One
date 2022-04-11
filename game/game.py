from django.db import IntegrityError
from flask import Blueprint, render_template, g, session, flash, redirect, url_for
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
        print("Global user")
        print(g.user)
        print(g.user.score)
    else:
        g.user = None

# Game main route, this is where players will start. Randomly selects an imdb_id and presents the plot of a film. Plot is uninteractable (Players cannot highlight the text in order to paste it into another window to find the film / answer)
@game_bp.route('/', methods=["GET", "POST"])
def game_home():
    # Make sure user is signed in or signed up.
    if not g.user:
        flash("Try signing up or logging in!", "error")
        return redirect("/auth/signup")
    user = g.user
    form = GiveGuessForm()

    # Due to API Call restrictions, we have ~600 films.
    random_num = random.randint(0, 635)
    movie = Movie.query.get(random_num)
    # On submit we want to check to see if the player won. There are three cases, for simplicity.
    # 1. Perfect guess, +25 points
    # 2. Close, within 10 points, +10 points.
    # 3. Complete miss. No points awarded.
    if form.validate_on_submit():
        user_input = int(form.guess.data)
        if user_input == movie.actual_score:
            user.score = user.score + 25
            db.session.commit()
            flash("WOW! You were spot on! 25 Points!", "success")
            return redirect(f'/movie/{random_num}')
        elif (user_input >= (movie.actual_score - 10)) and (user_input <= (movie.actual_score + 10)):
            user.score = user.score + 10
            db.session.commit()
            flash("Close enough! 10 Points to Griffindor!", "success")
            return redirect(f'/movie/{random_num}')
        else:
            flash("No such luck, try again!", "error")
            return redirect(f'/movie/{random_num}')

    return render_template('game.html', form=form, user=user, movie=movie)


@game_bp.route('/movie/<int:movie_id>', methods=["GET", "POST"])
def game_answer_page(movie_id):
    """Show Movie Page"""
    user = g.user
    movie = Movie.query.get_or_404(movie_id)
    print("User score")
    print(user.score)
    return render_template('movie.html', movie=movie, user=user)
