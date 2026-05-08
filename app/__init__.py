from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .database import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


#This does four things:

# Creates the Flask app

# Loads your config

# Initializes SQLAlchemy

# Initializes Flask‑Migrate