import json
import re

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, Permissions, connect, AlchemyEncoder, alchemy2json
from app.util.jwtutil import generate_jwt
from app.util.response import response


class Login(Resource):

    def post(self):
        current_app.logger.info("login {0}".format(request.json))
        params: dict = request.json
        if params:
            username = params.get("username", "")
            password = params.get("password", "")
            if not re.match("\d{10}", username) and not re.match(
                    "^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", username):
                return response(status_code=500, msg="账号无效")
            if not re.match("\S{6,20}", password):
                return response(status_code=500, msg="密码错误")
        else:
            return response(status_code=500, msg="illegal param")
        with connect() as session:
            res_status = None
            if "@" in username:
                res_status = session.query(User).filter(User.email == username).filter(
                    User.password == password).first()
            else:
                res_status = session.query(User).filter(User.username == username).filter(
                    User.password == password).first()
            if res_status:
                jwt = generate_jwt({"username": res_status.username, "role_id": res_status.role_id})
                return response(data={"token": jwt, "name": res_status.name, "info": res_status.info})
            else:
                return response(status_code=500, msg="账号或密码错误")
