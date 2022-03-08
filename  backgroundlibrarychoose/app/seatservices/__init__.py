from flask import Blueprint

seat_service = Blueprint('seat', __name__)
# must use
from . import route
