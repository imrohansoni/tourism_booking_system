from routers.bookings import booking_bp
from routers.tours import tour_bp

from utils.authentication import authenticate
from flask import Flask, redirect, render_template, send_from_directory, session, g
from controllers.auth_controllers import signup, login
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
    return render_template("home.html", user=g.get("user_data"))


@app.get("/about")
@authenticate
def render_about():
    return render_template("about.html", user=g.get("user_data"))


@app.get("/login")
def render_login():
    return render_template("login.html")


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
def not_found_handler(error):
    return render_template("error.html", message="404 : page not found")


@app.errorhandler(500)
def server_internal_error(error):
    return render_template("error.html", message="server internal error")


@app.errorhandler(Exception)
def unhandled_exception(err):
    print(err)
    return render_template("error.html", message="something went wrong")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.icon', mimetype='image/png')


app.run("localhost", port=4000, debug=True)
