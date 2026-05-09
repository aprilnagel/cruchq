from flask import Blueprint

uses_bp = Blueprint('users_bp', __name__)

from . import routes