const isDev = process.env.NODE_ENV === 'development'; // 判断当前开发环境

// 开发环境可以用devserver进行proxy代理，线上环境用真实接口地址
// 注意：proxy devserver跨域只适用于h5,其他环境需完整路径才能正常发起请求。

export const proxy = isDev ? 'http://httpbin.org' : 'http://httpbin.org'

