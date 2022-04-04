import json

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, User, Permissions, Goods, alchemy2json, Seat, Library
from app.util.jwtutil import verify_jwt
from app.util.response import response


class AllGoodsInfo(Resource):
    def get(self):
        current_app.logger.info("update info {0}".format(request.json))
        token = request.headers.get("token")
        token = verify_jwt(token)
        username = token.get("username", "")
        if not username:
            return response(status_code=500, msg="用户未登录")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            res = None
            if user.role_id == Permissions.USER_MANAGE and request.args.get("isall"):
                res = session.query(Goods).filter(Goods.status == 0).all()
            elif user.role_id == Permissions.USER_MANAGE and request.args.get("userid"):
                res = session.query(Goods).filter(Goods.status == 0).filter(Goods.user == request.args.get("userid")).all()
            elif user.role_id == Permissions.NORMAL_USER or user.role_id == Permissions.BADE_USER or user.role_id == Permissions.USER_MANAGE:
                res = session.query(Goods, Seat.position, Library, Seat.library).join(Seat, Seat.id == Goods.seat).join(Library, Seat.library == Library.id).filter(Goods.status == 0).filter(Goods.user == user.username).all()
            res_new = []
            for i in res:
                i[0].position = json.loads(i[1])
                i[0].library = alchemy2json(i[2])
                res_new.append(i[0])
            res_new.reverse()
            return response(alchemy2json(res_new))
