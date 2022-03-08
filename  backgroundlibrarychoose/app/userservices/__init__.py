from flask import Blueprint

user_service = Blueprint('user', __name__)
# must use
from . import route
