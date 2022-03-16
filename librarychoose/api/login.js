import { request } from './server.js'

export const MobileLogin =
  function(params) {//手机号登录
    return request.post('/user/login',params)
    .then(data=>{return data.data})
  }

export const Register =
  function(params) {
    return request.post('/user/register',params)
    .then(data=>{return data.data})
  }
  
export const UserInfo = 
function() {
    return request.get('/user/userinfo')
    .then(data=>{return data.data})
}

export const AllUserInfo = 
function() {
    return request.get('/user/alluserinfo')
    .then(data=>{return data.data})
}

export const LowUserRole = 
function(id) {
    return request.post('/user/lowuserrole?id='+id)
    .then(data=>{return data.data})
}

export const SetUserRoleNormal = 
function(id) {
    return request.post('/user/setuserrolenormal?id='+id)
    .then(data=>{return data.data})
}
  
  