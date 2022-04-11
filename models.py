"""SQLAlchemy models for Warbler."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    score = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Movie(db.Model):
    """A film"""

    __tablename__ = 'movies'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        unique=True
    )

    year = db.Column(
        db.Integer,
        nullable=True,
        unique=False
    )

    imdb = db.Column(
        db.String(10),
        nullable=False,
        unique=True
    )

    title = db.Column(
        db.String(140),
        nullable=False,
        unique=False
    )

    # V2
    plot = db.Column(
        db.String(1000),
        nullable=False,
        unique=False
    )

    poster = db.Column(
        db.String(1500),
        nullable=True,
        unique=False
    )

    actual_score = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    # views = db.Column(
    #     db.Integer
    # )

    @classmethod
    def addfilm(cls, title, year, imdb, plot, poster, actual_score):
        """Registers film to our DB"""

        movie = Movie(
            title=title,
            year=year,
            imdb=imdb,
            plot=plot,
            poster=poster,
            actual_score=actual_score
        )

        db.session.add(movie)
        return movie

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
