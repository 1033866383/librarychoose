from flask_restful import Api

from app.seatservices import seat_service
from app.seatservices.implments.home import Home

api = Api(seat_service)
api.add_resource(Home, '/', endpoint='')
