from flask import request
from flask_restful import Resource

from main import app


class Home(Resource):
    def get(self):
        app.logger.info("join")
        return request.path