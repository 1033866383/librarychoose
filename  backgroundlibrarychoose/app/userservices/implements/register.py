import re

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, Permissions, connect
from app.util.response import response


class Register(Resource):

    def post(self):
        current_app.logger.info("register {0}".format(request.json))
        params: dict = request.json
        if params:
            if not re.match("\d{10}$", params.get("username", "")):
                return response(status_code=500, msg="illegal param 账号必须使用学号")
            if not re.match("\S{6,20}$", params.get("password", "")):
                return response(status_code=500, msg="illegal param 密码长度必须大于6小于20")
            if not re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", params.get("email", "")):
                return response(status_code=500, msg="illegal param 邮箱格式不正确")
            iphone = params.get("iphone")
            if iphone and not re.match("\d{11}$", iphone):
                return response(status_code=500, msg="illegal param 手机号不合法")
        else:
            return response(status_code=500, msg="illegal param")
        with connect() as session:
            res = session.query(User).filter(User.username == params.get("username")).all()
            if len(res) > 0:
                return response(status_code=500, msg="账户已存在")
            res = session.query(User).filter(User.email == params.get("email")).all()
            if len(res) > 0:
                return response(status_code=500, msg="邮箱已使用")
            item_user = User(username=params.get("username"),
                             password=params.get("password"),
                             email=params.get("email"),
                             iphone=params.get("iphone", ""),
                             name=params.get("name"),
                             role_id=Permissions.USER_MANAGE)
            session.add(item_user)
            return response()
