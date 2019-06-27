# Axios 封装使用

## 前言

在当前Web开发中，为了更高效率的开发和更好的用户体验，采用前后端分离是一种主流的做法。在进行[项目](https://github.com/sysuswsad/mission_craft)的开发中，我们也采用了这样的架构设计方式。在该项目中，前端使用了 Vue 作为开发框架，而为了与后端进行交互，前端使用基于 promise 的 HTTP 客户端 [axios](https://github.com/axios/axios) 来处理网络请求，访问 API 。

为了统一使用形式，并处理各种网络异常错误，做出恰当的动作（如向用户展示友好的错误提示），前端对 axios 进行了简单的封装。



## 创建 axios 实例

使用自定义参数创建用于全局的 axios 实例，项目中例子如下：

```javascript
let $axios = axios.create({
  baseURL: 'http://127.0.0.1:5000/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  }
})
```

header 中的 `Content-Type` 字段值为 `application/json` 是因为在前后端分离的架构设计下，我们项目基本上是通过 json 文件来交互；`Access-Control-Allow-Origin` 字段是为了处理跨域问题，此处不表。



## 使用拦截器

axios 提供了对 request 和 response 的拦截器（*Interceptor*），在两者被 `then` 或 `catch` 处理之前，拦截器可以将拦截它们并做一定的修改或携带的信息做出相应的动作。

- Request 拦截

  常见的对 request 的拦截做法是添加 header 的信息，项目中使用如下：

  ```javascript
  // Request Interceptor
  $axios.interceptors.request.use(config => {
    if ($vue.$cookies.isKey('u-token')) {
      config.headers.Authorization = `Bearer ${$vue.$cookies.get('u-token')}`
    }
    return config
  }, error => {
    Message.error('请求失败')
    return Promise.reject(error)
  })
  ```

  上述代码检查当前 cookie 信息，为每个请求的头部加上用户的 token 信息，以便后端进行用户认证与权限确认。

  

- Response 拦截

  常见的对 response 的拦截做法是当请求返回了错误时拦截错误并首先进行一些可能的统一处理（如提示信息）。例子如下：

  ```javascript
  $axios.interceptors.response.use(response => {
    return response
  }, error => {
    // console.log something
    if (error.response.status === 400) {
      Message.error(error.response.data.message)
    } else if (error.response.status === 401) {
      Message.error('认证失效，请先登录')
    } else if (error.response.status === 403) {
      Message.error('错误，非法操作')
    } else {
      // other actions
      Message.error('错误')
    }
    
  return Promise.reject(error)
  })
  ```
  
  上述代码通过对 error 应答中的错误状态码进行判断，并向用户展示对应的信息。发生错误的最后返回 rejected 状态的 promise 以便在请求处做进一步处理。



## 统一请求接口

将发送 http 请求的 axios method 进一步封装成方法，并暴露给外部：

```javascript
export default {
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
```

项目中使用到的 http 请求有 post、get、put 和 delete，故封装上述四种方法。

使用例子如下（`backend.js` 中即为封装的 axios 代码）：

```javascript
import $backend from './backend'

$backend.postRequest('login/',{
  username_or_email: this.info.username,
  password: this.info.password
}).then(response => {
  // do something with response
}).catch(error => {
  // handle error
})
```

例子中，将用户输入的用户名与密码作为 post body 中的数据（例子中为明文）发送到后端作为登录凭证。

■