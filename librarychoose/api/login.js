import { request } from './server.js'

export const MobileLogin =
  function(params) {//手机号登录
    return request.post('/status/200',params)
    .then(data=>{return data.data})
  }