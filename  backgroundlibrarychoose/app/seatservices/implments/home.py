from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker

from app.dao.base import engine, User

class Home(Resource):
    def get(self):
        current_app.logger.info("info")
        Session = sessionmaker(engine)
        with Session() as session:
            res = session.query(User).all()
            print("===", res)
            return res