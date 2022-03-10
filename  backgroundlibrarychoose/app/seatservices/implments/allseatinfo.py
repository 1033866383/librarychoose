from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Seat, alchemy2json
from app.util.response import response


class AllSeatInfo(Resource):
    def get(self):
        current_app.logger.info("info")
        id = request.args.get("id")
        with connect() as session:
            if id:
                res = session.query(Seat).filter(Seat.id == id).all()
                return response(alchemy2json(res))
            res = session.query(Seat).all()
            return response(alchemy2json(res))
