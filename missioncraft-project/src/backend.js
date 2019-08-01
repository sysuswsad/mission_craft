import axios from 'axios'
import $vue from './main.js'
import { Message } from 'element-ui'
const baseURL = 'http://172.18.35.89:5000'

let $axios = axios.create({
  // baseURL: 'http://qcloud.captainp.cn:5000/api/',
  //baseURL: 'http://127.0.0.1:5000/api/',
  baseURL: 'http://172.18.35.89:5000/api/',
  // baseURL: 'http://172.18.34.59:5000/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  }
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
  console.log(`error keys: ${Object.keys(error)}`)
  console.log(`error.response keys: ${Object.keys(error.response)}`)
  console.log(`error.response.data keys: ${Object.keys(error.response.data)}`)
  console.log(error.response.data.message)
  if (error.response.status === 400) {
    switch (parseInt(error.response.data.message)) {
      case 100:
        Message.warning('该用户名已被注册')
        break

      case 101:
        Message.warning('该邮箱已被注册')
        break

      case 102:
        Message.warning('该学号已注册')
        break

      case 103:
        Message.error('验证码错误')
        break

      case 104:
        Message.error('验证码已过期')
        break

      case 105:
        // 登录时用户名或邮箱错误，在input中处理
        break

      case 106:
        // 登录时密码错误，在input中处理
        break

      case 109:
        // 修改用户名时，新的用户名已存在，在input中处理
        break

      case 110:
        Message.error('上传头像错误')
        break

      case 111:
        Message.error('头像文件必须是.jpg或.png格式文件')
        break

      case 112:
        // 修改密码时，原密码输入错误，在input中处理
        break

      case 201:
        Message.error('您不能取消已被他人接受的任务')
        break

      case 301:
        Message.error('任务已关闭')
        break

      case 302:
        Message.error('任务以达到其最大接受数，不能再接受该任务了')
        break

      case 303:
        Message.warning('该任务已经确认')
        break

      case 304:
        Message.error('您已领取该任务，不能重复领取')
        break

      case 305:
        Message.error('不可领取自己发布的任务')
        break

      default:
        console.log(`msg: ${error.response.data.message}`)
        break
    }
  } else if (error.response.status === 401) {
    Message.error('认证失效，请先登录')
  } else if (error.response.status === 403) {
    Message.error('错误，非法操作')
  } else {
    Message.error('错误')
  }

  return Promise.reject(error)
})

export default {
  baseURL,
  postRequest (url, params, config = {}) {
    return $axios.post(url, params, config)
  },

  getRequest (url, config = {}) {
    return $axios.get(url, config)
  },

  putRequest (url, params, config = {}) {
    return $axios.put(url, params, config)
  },

  deleteRequest (url, config = {}) {
    return $axios.delete(url, config)
  }
}
