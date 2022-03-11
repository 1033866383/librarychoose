from flask_restful import Api

from app.seatservices import seat_service
from app.seatservices.implments.addlibrary import AddLibrary
from app.seatservices.implments.addseat import AddSeat
from app.seatservices.implments.alllibraryinfo import AllLibraryInfo
from app.seatservices.implments.allseatinfo import AllSeatInfo

api = Api(seat_service)
api.add_resource(AllSeatInfo, '/allseatinfo', endpoint='allseatinfo')
api.add_resource(AllLibraryInfo, '/alllibraryinfo', endpoint='alllibraryinfo')
api.add_resource(AddLibrary, '/addlibrary', endpoint='addlibrary')
api.add_resource(AddSeat, '/addseat', endpoint='addseat')
