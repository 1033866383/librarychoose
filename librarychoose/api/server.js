import Vue from 'vue'
import Request from 'luch-request'
// 注意：如果用3.0以下版本，baseURL，请求和响应拦截有改动，需去对应版本readme文件查找。
import { proxy, proxyHttp, proxyPgApi } from './config.js'

const app = new Vue()
// request
const request = new Request()

request.setConfig((config) => { /* 设置全局配置 */
  config.baseURL = proxy

  config.header = {
    ...config.header,
	// a: 1
  }
  // config.custom = { auth: true }
  return config
})

request.interceptors.request.use((config, cancel) => { /* 请求之前拦截器 */
  const Token = uni.getStorageSync('lifeData').vuex_token ? uni.getStorageSync('lifeData').vuex_token : ''

  config.header = {
    ...config.header,
	Token
    // a: 3
  }
  // if (config.custom.auth) {
  //   config.header.token = 'token'
  // }
  /*
  if (!token) { // 如果token不存在，调用cancel 会取消本次请求，但是该函数的catch() 仍会执行
    cancel('token 不存在') // 接收一个参数，会传给catch((err) => {}) err.errMsg === 'token 不存在'
  }
  */
  return config
})

/**
 * 自定义验证器，如果返回true 则进入响应拦截器的响应成功函数(resolve)，否则进入响应拦截器的响应错误函数(reject)
 * @param { Number } statusCode - 请求响应体statusCode（只读）
 * @return { Boolean } 如果为true,则 resolve, 否则 reject
 */
request.validateStatus = (statusCode) => {
  return statusCode === 200
}

request.interceptors.response.use((response) => { /* 请求之后拦截器 */
  return response
}, (response) => { // 请求错误做点什么
  console.log(response)
  if (response.statusCode === 401) {
    app.$u.vuex('vuex_hasLogin', false)
    app.$u.vuex('vuex_token', undefined)
    app.$u.vuex('vuex_userInfo', undefined)
    app.$u.vuex('vuex_hasLogin', false)
    uni.navigateTo({
      url: '/pages/login/login/index',
    })
  }
  return response
})

// 测试用请求
const system = new Request()

export {
  request,
  system
}
