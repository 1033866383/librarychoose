from flask_restful import Api

from app.goodsservices import goods_services
from app.goodsservices.implements.addgoods import AddGoods
from app.goodsservices.implements.allgoodsinfo import AllGoodsInfo

api = Api(goods_services)
api.add_resource(AllGoodsInfo, '/allgoodsinfo', endpoint='allgoodsinfo')
api.add_resource(AddGoods, '/addgoods', endpoint='addgoods')
