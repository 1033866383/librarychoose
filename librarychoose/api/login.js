import { request } from './server.js'

export const MobileLogin =
  function(params) {//手机号登录
    return request.post('/user/login',params)
    .then(data=>{return data.data})
  }