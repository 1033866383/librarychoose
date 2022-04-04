import { request } from './server.js'

export const GenerPrice = 
function(data) {
    return request.post('goods/generprice',data)
    .then(data=>{return data.data})
}

export const AddGoods = 
function(data) {
    return request.post('goods/addgoods',data)
    .then(data=>{return data.data})
}

export const UsingSeat = 
function(starttime, endtime) {
    return request.get('goods/usingseat?start_time='+starttime + "&end_time="+endtime)
    .then(data=>{return data.data})
}

export const AllGoodsInfo = 
function() {
    return request.get('goods/allgoodsinfo')
    .then(data=>{return data.data})
}

export const CancelGoods = 
function(id) {
    return request.get('goods/cancelgoods?id='+id)
    .then(data=>{return data.data})
}
