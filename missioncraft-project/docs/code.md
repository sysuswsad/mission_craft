# 错误码

## API中使用的response code
- 200 正确处理
- 201 成功创建
- 400 请求错误
- 401 未授权(未token验证)
- 403 禁止操作（不能用别人的id取消、创建订单）
- 500 服务器错误，后端代码出错

## code GET
- 100 User {username} is already registered
- 101 Email {email} is already registered.
- 102 Sid {} is already registered.
- 103 Verification code is not correct
- 104 Verification code is out of time
## token POST
- 105 Incorrect username or email
- 106 Incorrect password
## code POST
- 107 Email format error
- 108 Email {email} is already registered.
## user PUT
- 109 User {username} is already registered.
## avatar GET
- 110 User avatar is not available
- 111 file is supposed to be jpg or png
## password POST
- 112 Old password wrong

## mission PUT
- 201 Should not cancel a mission already received

## order POST
- 301 Mission is closed
- 302 mission reached its max rcv num

## order PUT
- 303 The order has been confirmed
