import json

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, connect, alchemy2json
from app.util.jwtutil import verify_jwt
from app.util.response import response


class UserInfo(Resource):

    def get(self):
        current_app.logger.info("userinfo info {0}".format(request.json))
        token = request.headers.get("token")
        token = verify_jwt(token)
        current_app.logger.info("token {0}".format(token))
        if token:
            username = token.get("username", "")
            with connect() as session:
                user = session.query(User).filter(User.username == username).first()
                res = alchemy2json(user)
                del res["password"]
                del res["id"]
                return response(res)
        else:
            return response(status_code=500, msg="用户未登录")
