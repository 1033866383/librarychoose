import { request } from './server.js'

export const MobileLogin =
  function(params) {//手机号登录
    return request.post('/user/login',params)
    .then(data=>{return data.data})
  }

export const Register =
  function(params) {//手机号登录
    return request.post('/user/register',params)
    .then(data=>{return data.data})
  }