import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, Blueprint
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from password import password

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db

# Blueprint Imports
from auth.auth import signup_bp

# CSV Reading
import csv
import pandas as pd
import requests
import random

CURR_USER_KEY = "curr_user"

# App and DB Config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', f"postgresql://postgres:{password}@localhost:5432/movie_buster"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# View config
# Blueprint Registrations

app.register_blueprint(signup_bp, url_prefix='/signup')

