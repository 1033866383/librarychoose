from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, connect, alchemy2json
from app.util.jwtutil import verify_jwt
from app.util.response import response


class AllUserInfo(Resource):

    def get(self):
        current_app.logger.info("all userinfo info {0}".format(request.json))
        token = request.headers.get("token")
        token = verify_jwt(token)
        current_app.logger.info("token {0}".format(token))
        with connect() as session:
            user = session.query(User).all()
            res = alchemy2json(user)
            return response(res)
