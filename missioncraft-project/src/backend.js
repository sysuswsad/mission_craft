import axios from 'axios'
import Vue from 'vue'
import { Message } from 'element-ui'
import router from './router'

let $axios = axios.create({
  baseURL: 'http://127.0.0.1:5000/api/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Authorization,Origin, X-Requested-With, Content-Type, Accept',
    'Access-Control-Allow-Methods': 'GET,POST,PUT'
  }
})

// Request Interceptor
$axios.interceptors.request.use( config => {
  /*
  if (Vue.$cookies.isKey('u-token')) {
    config.headers.Authorization = `Bearer ${Vue.$cookies.get('u-token')}`
  }
  */
  return config
}, error => {
  Message.error({'message': '请求超时，请稍后重试'})
  return Promise.reject(error)
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(response => {
  return response
}, error => {
  switch (error.response.status) {
    case 401:
      Message.warning({message: '认证失效，请先登录'})
      router.replace({name: 'login'})
      break

    case 403:
      Message.error({message: '权限不足'})
      break

    case 404:
      Message.error({message: '资源错误'})
      break

    default:
      Message.error({message: '未知错误'})
      break
  }

  return Promise.reject(error)
})

export default {
  postRequest (url, params, config={}) {
    return $axios.post(url, params, config)
  },

  getRequest (url, params) {
    return $axios.get(url, params)
  },

  putRequest (url, params, config={}) {
    return $axios.put(url, params, config)
  }
}
