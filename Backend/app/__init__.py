
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .config import DevelopmentConfig

from .extensions import ma, db


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    #CORS
    CORS(
        app,
        resources={r"/*": {"origins": [
            "http://localhost:5173",  # Vite development server
            "http://localhost:5000",  # Flask development server
            "https://cruchq.com",  # Production domain
            "https://staging.cruchq.com"  # Staging domain
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Accept"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    #config
    app.config.from_object(DevelopmentConfig)

    #extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    #import models
    from . import models
    from .blueprints.auth import auth_bp
    from .blueprints.users import uses_bp
    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(uses_bp, url_prefix='/users')
    
    @app.get("/")
    def home():
        return {"message": "Welcome to the CruChq API!"}

    return app


#This does four things:

# Creates the Flask app

# Loads your config

# Initializes SQLAlchemy

# Initializes Flask‑Migrate