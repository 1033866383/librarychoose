import json
import re

import requests
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
        if not max_seat or not re.match("\d{1,4}$", max_seat):
            return response(status_code=500, msg="可容纳人数有误")
        if int(max_seat) > 50:
            return response(status_code=500, msg="可容纳人数不能超过50")
        if not position or not re.match("\S{1,100}$", position):
            return response(status_code=500, msg="位置有误")
        with connect() as session:
            item = session.query(Library).filter(Library.name == name).first()
            if item:
                return response(status_code=500, msg="该图书馆已存在")
            item = Library(name=name, max_seat=max_seat, position=position)
            session.add(item)
            top = int(item.max_seat) // 10
            last_left = int(item.max_seat) % 10
            add_seats = []
            for l in range(top + 1):
                for t in range(10):
                    add_seats.append({"left": l, "right": t, "local": "A"})
            for i in range(last_left + 1):
                add_seats.append({"left": top + 1, "right": i, "local": "A"})
            current_app.logger.info(add_seats)
            session.commit()
            res = requests.post(request.host_url + "seat/addseat", headers={"token": request.headers.get("token")},
                                json={"library": item.id, "position": add_seats})
            current_app.logger.info(res.text)
            if json.loads(res.text).get("msg") != "success":
                raise Exception("添加 seat 失败")
            return response()
