import json
import os.path

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, User
from app.util.jwtutil import verify_jwt
from app.util.response import response


class Upload(Resource):

    def post(self):
        current_app.logger.info("upload {0}".format(request.form))
        token = request.headers.get("token")
        token = verify_jwt(token)
        if not token:
            return response(status_code=500, msg="未登录")
        username = token.get("username", "")
        icon = request.files.get("icon")
        parent_dir = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(parent_dir)
        parent_dir, _ = os.path.split(parent_dir)
        icon.save(parent_dir + os.sep + "static" + os.sep + username + "_" + "icon.png")
        with connect() as session:
            user = session.query(User).filter(User.username == username).first()
            info: dict = {}
            if user.info:
                try:
                    info = json.loads(user.info)
                except Exception as e:
                    current_app.logger.info(e)
            info["icon"] = "/static/" + username + "_icon.png"
            user = session.query(User).filter(User.username == username).update({"info": json.dumps(info)})
        return response()
