# _*_ coding: utf-8 _*_
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, User, Permissions, Goods, alchemy2json
from app.util.jwtutil import verify_jwt
from app.util.response import response


class UsingSeat(Resource):
    def get(self):
        current_app.logger.info("update info {0}".format(request.json))
        token = request.headers.get("token")
        token = verify_jwt(token)
        username = token.get("username", "")
        if not username:
            return response(status_code=500, msg="用户未登录")
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        if not start_time:
            return response(status_code=500, msg="illegal param not start_time")
        if not end_time:
            return response(status_code=500, msg="illegal param not end_time")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            res = None
            if user.role_id == Permissions.NORMAL_USER or user.role_id == Permissions.BADE_USER or user.role_id == Permissions.USER_MANAGE:
                res = session.query(Goods.seat).filter(
                    Goods.end_time >= datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")).filter(
                    Goods.start_time <= datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")).all()
            return response([i[0] for i in res])
