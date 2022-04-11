"""Seed DB from CSVs"""

from csv import DictReader
from app import db
from models import User, Movie
import pandas as pd
import requests

APIKEY = 'dc9c7e58'

db.drop_all()
db.create_all()

# Add our movies.
df = pd.read_csv('csv/movies.csv')
for index, row in df.iterrows():
    # Gather data from our DF
    title = row.title
    year = row.year
    imdb = row.imdb
    # Gather data from our API
    response = requests.get(
        f"http://omdbapi.com/?apikey={APIKEY}&i={imdb}")
    data = response.json()
    # Get the remaining data we need from our api request.
    plot = data["Plot"]
    poster = data["Poster"]
    # Ratings are a bit tricky as there can be more than one source of a rating, such as metacritic or imdb.
    # We also must remove the '%' from the end of our string.
    for source in data['Ratings']:
        rating_len = len(source)
        if source['Source'] == 'Rotten Tomatoes':
            actual_score = int(source['Value'][:-1])
    # Adds one film to our db
    movie = Movie.addfilm(
        title=title,
        year=year,
        imdb=imdb,
        plot=plot,
        poster=poster,
        actual_score=actual_score
    )
    db.session.commit()


# Opens CSV and reads data, adding to DB. Starts with movies, then users.
# with open('csv/movies.csv') as movies:
#     db.session.bulk_insert_mappings(Movie, DictReader(movies))

with open('csv/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

db.session.commit()
