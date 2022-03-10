import re

from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Library
from app.util.response import response


class AddLibrary(Resource):
    def post(self):
        current_app.logger.info("info")
        params = request.json
        if not params:
            return response(status_code=500, msg="illegal param")
        name = params.get("name")
        max_seat = params.get("max_seat")
        position = params.get("position")
        if not name or not re.match("\S{1,100}$", name):
            return response(status_code=500, msg="名称有误")
        if not max_seat or not re.match("\d{1,10}$", max_seat):
            return response(status_code=500, msg="可容纳人数有误")
        if not position or not re.match("\S{1,100}$", position):
            return response(status_code=500, msg="位置有误")
        with connect() as session:
            item = session.query(Library).filter(Library.name == name).first()
            if item:
                return response(status_code=500, msg="该图书馆已存在")
            item = Library(name=name, max_seat=max_seat, position=position)
            session.add(item)
            return response()
