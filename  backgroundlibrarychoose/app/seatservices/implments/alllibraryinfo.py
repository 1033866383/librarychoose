from flask import current_app, request
from flask_restful import Resource

from app.dao.base import connect, Library
from app.util.response import response


class AllLibraryInfo(Resource):
    def get(self):
        current_app.logger.info("info")
        id = request.args.get("id")
        name = request.args.get("name")
        with connect() as session:
            if id:
                res = session.query(Library).filter(Library.id == id).all()
                return response(res)
            if name:
                res = session.query(Library).filter(Library.name.like("%{0}%".format(name))).all()
                return response(res)
            res = session.query(Library).all()
            return response(res)