import json

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, connect
from app.util.jwtutil import verify_jwt
from app.util.response import response


class UpdateInfo(Resource):

    def put(self):
        current_app.logger.info("update info {0}".format(request.json))
        token = request.headers.get("token")
        token = verify_jwt(token)
        username = token.get("username", "")
        params: dict = request.json
        if not params:
            return response(status_code=500, msg="illegal param ")
        password = params.get("password", None)
        info = params.get("info", "")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                return response(status_code=500, msg="用户不存在")
            if password:
                if password == user.password:
                    return response(status_code=500, msg="新旧密码相同修改失败")
                else:
                    session.query(User).filter(User.username == username).update({"password": password})
            if info:
                session.query(User).filter(User.username == username).update({"info": info})
            return response()
