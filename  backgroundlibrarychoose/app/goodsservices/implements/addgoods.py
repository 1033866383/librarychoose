import json
import time
import uuid
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Seat, Goods, User, Permissions, alchemy2json
from app.goodsservices.implements.util import all_price
from app.util.jwtutil import verify_jwt
from app.util.response import response


class AddGoods(Resource):
    def post(self):
        current_app.logger.info("info")
        token = request.headers.get("token")
        token = verify_jwt(token)
        username = token.get("username", "")
        if not username:
            return response(status_code=500, msg="用户未登录")
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
            user = session.query(User).filter(User.username == username).first()
            credit = json.loads(user.info).get("credit")
            if not user:
                return response(status_code=500, msg="用户未登录")
            elif user.role_id == Permissions.BADE_USER:
                return response(status_code=500, msg="您已被拉黑,无法进行座位预订")
            elif not credit:
                return response(status_code=500, msg="您的积分不足")
            elif int(credit) <=50:
                return response(status_code=500, msg="您的积分不足,无法预定")
            seat_item = session.query(Seat).filter(Seat.id == seat).first()
            if not seat_item:
                return response(status_code=500, msg="illegal param seat")
            goods = session.query(Goods).filter(Goods.seat == seat).filter(Goods.end_time >= datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")).filter(Goods.start_time <=datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")).filter(Goods.status == 0).first()
            if goods:
                return response(status_code=500, msg="illegal param 当前时间区间有用户使用该座位无法占用")
            goods_item = Goods(id=str(uuid.uuid1()), seat=seat, user=username, start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"), end_time=datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"), price=all_price(seat_item.price, start_time, end_time), status=0)
            session.add(goods_item)
            return response(alchemy2json(goods_item))


