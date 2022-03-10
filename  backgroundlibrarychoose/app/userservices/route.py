from flask_restful import Api

from app.userservices import user_service
from app.userservices.implements.alluserinfo import AllUserInfo
from app.userservices.implements.login import Login
from app.userservices.implements.register import Register
from app.userservices.implements.setuserrole import LowUserRole, SetUserRoleNormal
from app.userservices.implements.updateinfo import UpdateInfo
from app.userservices.implements.upload import Upload
from app.userservices.implements.userinfo import UserInfo

api = Api(user_service)
api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(UserInfo, '/userinfo', endpoint='userinfo')
api.add_resource(UpdateInfo, '/updateinfo', endpoint='updateinfo')
api.add_resource(Upload, '/upload', endpoint='upload')
api.add_resource(AllUserInfo, '/alluserinfo', endpoint='alluserinfo')
api.add_resource(LowUserRole, '/lowuserrole', endpoint='lowuserrole')
api.add_resource(SetUserRoleNormal, '/setuserrolenormal', endpoint='setuserrolenormal')
