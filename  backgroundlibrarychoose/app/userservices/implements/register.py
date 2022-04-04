import json
import os
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
            sup, _ = os.path.split(__file__)
            sup, _ = os.path.split(sup)
            sup, _ = os.path.split(sup)
            with open(sup + os.sep + "static" + os.sep + "icon.png", "rb") as img:
                with open(sup + os.sep + "static" + os.sep + "{0}_icon.png".format(params.get("username")),"w+") as img_copy:
                    pass
                with open(sup + os.sep + "static" + os.sep + "{0}_icon.png".format(params.get("username")), "rb+") as img_copy:
                    img_copy.write(img.read())
            info = {"icon": sup + os.sep + "static" + os.sep + "{0}_icon.png".format(params.get("username")), "credit": 100}
            item_user = User(username=params.get("username"),
                             password=params.get("password"),
                             email=params.get("email"),
                             iphone=params.get("iphone", ""),
                             name=params.get("name"),
                             role_id=Permissions.NORMAL_USER,
                             info=json.dumps(info))
            session.add(item_user)
            return response()
