import axios from 'axios'
import $vue from './main.js'
import { Message } from 'element-ui'

let $axios = axios.create({
  // baseURL: 'http://qcloud.captainp.cn:5000/api/',
  // baseURL: 'http://127.0.0.1:5000/api/',
  baseURL: 'http://172.18.34.59:5000/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})

// Request Interceptor
$axios.interceptors.request.use(config => {
  if ($vue.$cookies.isKey('u-token')) {
    config.headers.Authorization = `Bearer ${$vue.$cookies.get('u-token')}`
  }
  return config
}, error => {
  Message.error({ 'message': '请求超时，请稍后重试' })
  return Promise.reject(error)
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(response => {
  return response
}, error => {
  console.log(error)
  switch (error.response.status) {
    case 401:
      Message.warning({ message: '认证失效，请先登录' })
      $vue.$router.replace({ name: 'login' })
      break

    case 403:
      Message.error({ message: '权限不足' })
      break

    case 404:
      Message.error({ message: '资源错误' })
      break

    default:
      Message.error({ message: '未知错误' })
      break
  }

  return Promise.reject(error)
})

export default {
  postRequest (url, params, config = {}) {
    return $axios.post(url, params, config)
  },

  getRequest (url) {
    return $axios.get(url)
  },

  putRequest (url, params, config = {}) {
    return $axios.put(url, params, config)
  }
}
