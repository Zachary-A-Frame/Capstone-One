from flask import Blueprint, render_template, g, session, flash, redirect
from models import db, connect_db, User
from forms import UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError

signup_bp = Blueprint('signup_bp',__name__,
                      template_folder="templates",
                      static_folder="static", static_url_path="assets")

CURR_USER_KEY = "curr_user"

# Routes
@signup_bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# @signup_bp.route('/')
# def signup():
#     variable = 'Hello!'
#     return render_template('signup/signup.html', variable=variable)

@signup_bp.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user sign ups. Creates and adds users to DB. Redirect to Home. Validate."""
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Email already taken", 'danger')
            return render_template('signup/signup.html', form=form)

        do_login(user)

        return redirect("/auth/welcome")

    else:
        return render_template('signup/signup.html', form=form)

@signup_bp.route("/welcome")
def welcome():
    """Welcome landing page explaining the game."""
    user = "user"
    return render_template('signup/welcome.html', user=user)


@signup_bp.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.email}!", "success")
            return redirect("/")
        else:
            flash("Invalid credentials.", 'danger')

    return render_template('login/login.html', form=form)


@signup_bp.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    if CURR_USER_KEY not in session:
        flash("Logout successful!", "success")
        return redirect("auth/login")
