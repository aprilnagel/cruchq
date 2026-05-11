from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
ma = Marshmallow()
limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day"]
)