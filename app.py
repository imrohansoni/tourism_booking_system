from routers.bookings import booking_bp
from routers.tours import tour_bp

from utils.authentication import authenticate
from flask import Flask, redirect, render_template, send_from_directory, session, g
from controllers.accommodation_controllers import get_accommodations
from controllers.feedback_controllers import create_feedback
from controllers.auth_controllers import signup, login, update_account
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET")
app.permanent_session_lifetime = timedelta(hours=2)

app.register_blueprint(booking_bp, url_prefix="/bookings")
app.register_blueprint(tour_bp, url_prefix="/tours")


@app.get("/")
@authenticate
def render_home():
    return render_template("home.html", user=g.get("user_data"), active_link="home")


@app.get("/about")
@authenticate
def render_about():
    return render_template("about.html", user=g.get("user_data"), active_link="about")


@app.get("/locations")
@authenticate
def render_locations():
    return render_template("locations.html", user=g.get("user_data"), active_link="locations")


@app.get("/feedback")
@authenticate
def render_feedback():
    return render_template("feedback.html", user=g.get("user_data"), active_link="feedback")


# @app.get("/centers")
# @authenticate
# def render_center():
#     return render_centers()


# @app.get("/feedback")
# @authenticate
# def render_feedback():
#     return render_template("feedback.html", user=g.get("user_data"))


@app.post("/feedback")
@authenticate
def post_feedback():
    return create_feedback()


@app.get("/login")
def render_login():
    return render_template("login.html")


@app.get("/accommodations")
def get_accommodations_route():
    return get_accommodations()


@app.get("/account")
@authenticate
def render_account():
    user = g.get("user_data")
    if user is None:
        return redirect("/login")
    return render_template("account.html", **user, user=user)


@app.post("/account")
def update_account_route():
    return update_account()


@app.get("/signup")
def render_signup():
    return render_template("signup.html")


@app.get("/logout")
def logout_route():
    session.pop("user_id")
    return redirect("/")


@app.post("/signup")
def signup_route():
    return signup()


@app.post("/login")
def login_route():
    return login()


@app.errorhandler(404)
@authenticate
def not_found_handler(error):
    return render_template("error.html", message="404 : page not found", user=g.get("user_data"))


@app.errorhandler(500)
def server_internal_error(error):
    return render_template("error.html", message="server internal error", user=g.get("user_data"))


@app.errorhandler(Exception)
@authenticate
def unhandled_exception(err):
    print(err)
    return render_template("error.html", message="something went wrong",  user=g.get("user_data"))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.icon', mimetype='image/png')


app.run("localhost", port=4000, debug=True)
