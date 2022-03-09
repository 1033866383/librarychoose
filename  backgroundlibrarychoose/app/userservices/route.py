from flask_restful import Api

from app.userservices import user_service
from app.userservices.implements.login import Login
from app.userservices.implements.register import Register

api = Api(user_service)
api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')