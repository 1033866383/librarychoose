import json

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Seat, Library
from app.util.response import response


class AddSeat(Resource):
    def post(self):
        params = request.json
        if not params:
            return response(status_code=500, msg="illegal param")
        library = params.get("library")
        position = params.get("position")
        price = params.get("price")
        current_app.logger.info("info {0}".format(params))
        if not library:
            return response(status_code=500, msg="illegal param 缺少图书馆位置")
        if not isinstance(position, dict):
            """
            {'local': "A", 'left': 0, 'top': 0 }
            """
            return response(status_code=500, msg="illegal param 错误的位置信息")
        self.add_price(price)
        with connect() as session:
            library_item = session.query(Library).filter(Library.id == library).first()
            if not library_item:
                return response(status_code=500, msg="illegal param 没有此自习室")
            seat_item = session.query(Seat).filter(Seat.library == library).filter(Seat.position == json.dumps(position)).first()
            if seat_item:
                return response(status_code=500, msg="当前座位已被添加")
            seat_item = Seat(library=library, position=json.dumps(position), price=json.dumps(price))
            session.add(seat_item)
            return response()

    def add_price(self, price):
        if not price:
            price = {}
        for i in range(1, 25):
            if not price.get(str(i)):
                price[str(i)] = 10
