from flask import current_app, request
from flask_restful import Resource

from app.dao.base import User, connect, Permissions
from app.util.response import response


class LowUserRole(Resource):

    def put(self):
        current_app.logger.info("set user role info {0}".format(request.json))
        param = request.json
        if not param:
            return response(status_code=500, msg="illegal param")
        username = param.get("username")
        if not username:
            return response(status_code=500, msg="illegal param")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user or user.role_id == Permissions.USER_MANAGE:
                return response(status_code=500, msg="illegal param")
            res = session.query(User).filter(User.username == username).update({"role_id": Permissions.BADE_USER})
            if res:
                return response()


class SetUserRoleNormal(Resource):

    def put(self):
        current_app.logger.info("set user role info {0}".format(request.json))
        param = request.json
        if not param:
            return response(status_code=500, msg="illegal param")
        username = param.get("username")
        if not username:
            return response(status_code=500, msg="illegal param")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user or user.role_id != Permissions.BADE_USER:
                return response(status_code=500, msg="illegal param")
            res = session.query(User).filter(User.username == username).update({"role_id": Permissions.NORMAL_USER})
            if res:
                return response()
