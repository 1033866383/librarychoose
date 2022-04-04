from flask_restful import Api

from app.goodsservices import goods_services
from app.goodsservices.implements.addgoods import AddGoods
from app.goodsservices.implements.allgoodsinfo import AllGoodsInfo
from app.goodsservices.implements.cancelgoods import CancelGoods
from app.goodsservices.implements.generprice import GenerPrice
from app.goodsservices.implements.usingseat import UsingSeat


api = Api(goods_services)
api.add_resource(AllGoodsInfo, '/allgoodsinfo', endpoint='allgoodsinfo')
api.add_resource(AddGoods, '/addgoods', endpoint='addgoods')
api.add_resource(GenerPrice, '/generprice', endpoint='generprice')
api.add_resource(UsingSeat, '/usingseat', endpoint='usingseat')
api.add_resource(CancelGoods, '/cancelgoods', endpoint='cancelgoods')
