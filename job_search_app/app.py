"""File containing app contents such as:
    URL endpoints, database configurations and file connections."""

# App imports
import os
import Flask

# Local file imports


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
    # DB.init(app)
