from flask_restful import Api

from app.goodsservices import goods_services
from app.goodsservices.implements.allgoodsinfo import AllGoodsInfo

api = Api(goods_services)
api.add_resource(AllGoodsInfo, '/allgoodsinfo', endpoint='allgoodsinfo')
