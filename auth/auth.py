from flask import Blueprint, render_template

signup_bp = Blueprint('signup_bp',__name__,
                      template_folder="templates",
                      static_folder="static", static_url_path="assets")

@signup_bp.route('/')
def signup():
    variable = 'Hello!'
    return render_template('signup/signup.html', variable=variable)
