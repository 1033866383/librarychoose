from flask import Blueprint

goods_services = Blueprint('goods', __name__)
# must use
from . import route
