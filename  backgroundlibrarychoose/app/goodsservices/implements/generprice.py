import time
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Seat
from app.goodsservices.implements.util import all_price
from app.util.jwtutil import verify_jwt
from app.util.response import response


class GenerPrice(Resource):
    def post(self):
        current_app.logger.info("info")
        token = request.headers.get("token")
        token = verify_jwt(token)
        params = request.json
        if not params:
            return response(status_code=500, msg="illegal param")
        seat = params.get("seat")
        start_time = params.get("start_time")
        end_time = params.get("end_time")
        if not seat:
            return response(status_code=500, msg="illegal param seat")
        if not start_time:
            return response(status_code=500, msg="illegal param start_time")
        if not end_time:
            return response(status_code=500, msg="illegal param end_time")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_now_number = time.mktime(time.strptime(time_now, '%Y-%m-%d %H:%M:%S'))
        start_time_number = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        end_time_number = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        if start_time <= time_now:
            return response(status_code=500, msg="订单开始时间不能小于当前时间")
        if float(start_time_number) + 60 * 60 > float(end_time_number):
            return response(status_code=500, msg="订单时长不能小于1小时")
        if float(start_time_number) + 24 * 60 * 60 < float(end_time_number):
            return response(status_code=500, msg="订单时长不能大于24小时")
        with connect() as session:
            seat_item = session.query(Seat).filter(Seat.id == seat).first()
            if not seat_item:
                return response(status_code=500, msg="illegal param seat")
            res = all_price(seat_item.price, start_time, end_time)
            return response(res)
