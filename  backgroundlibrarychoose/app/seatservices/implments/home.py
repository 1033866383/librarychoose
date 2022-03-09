from flask import current_app
from flask_restful import Resource

from app.dao.base import connect, Seat
from app.util.response import response


class Home(Resource):
    def get(self):
        current_app.logger.info("info")
        with connect() as session:
            res = session.query(Seat).all()
            return response(res)
