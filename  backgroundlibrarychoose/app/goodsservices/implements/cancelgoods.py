# _*_ coding: utf-8 _*_
import datetime
import json
import time

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Goods, User
from app.util.jwtutil import verify_jwt
from app.util.response import response


class CancelGoods(Resource):
    def get(self):
        current_app.logger.info("info")
        token = request.headers.get("token")
        token = verify_jwt(token)
        username = token.get("username", "")
        if not username:
            return response(status_code=500, msg="用户未登录")
        id = request.args.get("id")
        if not id:
            return response(status_code=500, msg="illegal param id")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                return response(status_code=500, msg="用户未登录")
            goods = session.query(Goods).filter(Goods.id == id).first()
            if goods.start_time < datetime.datetime.now():
                return response(status_code=500, msg="订单已开始无法取消")
            info = json.loads(user.info)
            if int(info["credit"]) <= 50:
                info["credit"] = 0
            else:
                info["credit"] -= 50
            session.query(User).filter(User.username == username).update({"info": json.dumps(info)})
            res = session.query(Goods).filter(Goods.id == id).update({"status": 1})
            return response(res)
