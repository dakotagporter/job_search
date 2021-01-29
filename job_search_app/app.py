"""File containing app contents such as:
    URL endpoints, database configurations and file connections."""

# App imports
import os
from flask import Flask, render_template, request, flash, redirect, url_for

# Local file imports
from .models import DB, Job
from .stuff import STATES
from .indeed_scraper import verify, filter


def create_app():
    """Create Flask application object.

    Args:
        None
    Returns:
        app: Flask app object
    """
    app = Flask(__name__)

    # Set app configurations and initialize database
    UPLOAD_FOLDER = "static/"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = "secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("base.html", title="Home")

    @app.route("/discover")
    def discover():
        return render_template("discover.html", title="Discover",
                               states=STATES)

    @app.route("/discover", methods=["POST"])
    def discover_post():
        title = request.form.get("title")
        city = request.form.get("city")
        state = request.form.get("state")
        # Retrieve user description for model
        user_desc = request.form.get("desc")

        # Check for search errors using the scraper's verify function
        results, url = verify(title, city, state)
        if isinstance(results, list):
            flash(results)
            return redirect(url_for("discover"))

        # Filter search results
        jobs = filter(results, url)

        # Reset Database before each query
        DB.drop_all()
        DB.create_all()

        # Add jobs to database
        for job in jobs:
            new_job = Job(title=job["title"],
                          comp=job["comp"],
                          loc=job["loc"],
                          salary=job["salary"],
                          desc=job["desc"])

            DB.session.add(new_job)

        DB.session.commit()

        # Input data into model
        data = Job.query.filter_by(Job.desc)
        return str(data)
        preprocessor(data)

    return app
