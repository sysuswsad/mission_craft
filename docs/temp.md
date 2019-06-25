# Weclome to ApiDoc
----
<!-- TOC -->
- [简介](#简介)    
- [用户接口](#用户接口)       
    - [获取邮箱验证码](#获取邮箱验证码)     
    - [用户注册](#用户注册)      
    - [用户登录](#用户登录)       
    - [得到个人信息](#得到个人信息)        
    - [修改个人信息](#修改个人信息)        
    - [修改密码](#修改密码)  
    - [上传头像](#上传头像)       
    - [得到头像](#得到头像)   
- [任务接口](#任务接口)
    - [得到任务信息](#得到任务信息)
    - [发布任务](#发布任务)
    - [取消任务](#取消或中断任务)
- [订单接口](#订单接口)        
    - [查询个人订单](#查询个人领取订单)
    - [创建个人订单](#创建个人订单)
    - [确认个人订单](#确认个人订单)
- [通知接口](#通知接口)
    - [查询通知信息](#获取通知)
    - [修改已读状态](#修改通知已读情况)

<!-- /TOC -->

## 简介

> 这是Mission Craft系统中使用的API接口文档，此文档在开发过程前后端交互中逐步完善。


---
---
## 用户接口
### 获取邮箱验证码

**请求地址**
```
/code/
```

**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
email|是|123@qq.com|用于接收验证码的邮箱|


**返回示例**
```json
{
    "staus" : 200,
    "message": "Generate and send token successfully"
}
```
---
### 用户注册

**请求地址**
```
/user/
```
**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
username|是|pj|用户名
sid|是|16340000|学号
email|是|9039989@qq.com|邮箱
password|是|123456|密码
code|是|1234|手机接收的验证码

**返回示例**
```json
{
    "staus" : 201,
    "message": "Register successfully"
}
```
----


### 用户登录

登录以获得token，使用token来验证用户信息。

**请求地址**

```
/token/
```

**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
username_or_email|是|pj或123@qq.com|用户昵称或注册的邮箱
password|是|123456|登录密码

**返回示例**
```json
{
    "staus" : 201,
    "data" : {
        "token" : 1234
    },
    "message": "Login successfully"
}
```

---
### 得到个人信息

**请求地址**
```
/user/
```
**HTTP方法**

GET

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录时所获得的token

**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "username" : "pj",
        "sid" : "16040000",
        "email" : "123@qq.com",
        "avatar" : "\..\..",
        "university" : "中山大学",
        "school": "数据院",
        "grade": "大三",
        "gender" : 0,
        "qq": "90379",
        "phone": "12321",
        "wechat" : "90379",
        "mission_pub_num": 10,
        "mission_fin_num": 10
    },
    "message": "Get user info successfully"
}
```

---
### 修改个人信息
**请求地址**
```
/user/
```

**HTTP方法**
PUT

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录所返回的token
username|否|pj|修改的用户名
university|否|大山中学|修改的学校
school|否|学院|修改的学院
grade|否|大三|修改的年级
gender|否|0|0为男,1为女
phone|否|+86 136012138485|电话号码
qq|否|90317|qq号
wechat|否|90325|微信号

**返回示例**
```json
{
    "staus" : 200,
    "message": "Update user info successfully"
}
```
---
### 修改密码
**请求地址**
```
/password/
```

**HTTP方法**
POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录所返回的token
username|是|pj|用户名
old_password|是|Pj123456|原密码
new_password|是|PJ123|新密码

**返回示例**
```json
{
    "staus" : 200,
    "message": "Change password successfully"
}
```
---
### 上传头像
**请求地址**
```
/avatar/
```

**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录所返回的token
image|是||上传头像文件(type=file),仅允许.jpg,.jpeg,.png类型

**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "avator" : "\..\.."
    },
    "message": "Get user avatar successfully"
}
```
---
### 得到头像

**请求地址**
```
/avatar/
```

**HTTP方法**

GET

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录所返回的token

**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "avator" : "www.domain.com/image/.."
    },
    "message": "change avatar successfully"
}
```

---
---

## 任务接口
### 得到任务信息
根据传递的参数获得所需的功能
- 任务广场所使用的API，返回待领取的任务。使用游标分页设计，返回特定条件下的任务清单
- 返回个人发布的任务，如果是问卷类型，则接收者为空(问卷为匿名)，否则带上接收者id和接收时间。只有发布快递类型的任务且被领取了，才返回领取者的个人信息
- 返回某个任务的具体信息，通过mission id查找

**请求地址**

```
/mission/
```
**HTTP方法**

GET 

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--
token|是|123|登录返回的token
create_time|否|2019-5-1 14:40:20|返回该时间前的任务
limit|否|10|最多返回条数
type|否|0或1|筛选返回类型，0-问卷、1-取快递、None全部
return_problems|否|0或1|1表示查询结果中需要返回问题信息
return_statistics|否|0或1|1表示查询结果中需要返回答案统计信息
bounty|否|10|筛选最低报酬
personal|否|0或1|0对应第一个功能，1对应第2个功能
mission_id|否|123|返回特定id对应的任务


**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "missions" : [
            {
            "mission_id": 10, 
            "create_time":"2019-5-1 14:40:20",
            "deadline": "2019-6-1 14:40:20",
            "title":"标题", 
            "description":"描述",
            "bounty":10,
            "max_num":10,
            "receiver_id":null,
            "rcv_num":5,
            "fin_num":2,
            "finish_time":"2019-5-10 14:40:20",
            "type":0, 
            "publisher_id":10, 
            "username":"pj",
            "avatar":"www.domain.com/imgage/..",
            "receiver_id":1,
            "receiver_name":'pj',
            "receviver_avatar": "www.domain/image/1.png",
            "recevier_qq": "12345648",
            "receiver_wechat": "13246790",
            "receiver_phone": "136976464",
            "receiver_other_way": "facebook: 1232213",
            "receiver_time":"2010-10-10 11:11:11",
            "problems":[
                { 'type': 0, 'question': '单选问题', 'choices': ['选项1', '选项2'], 'answer': [10,20]},
                { 'type': 1, 'question': '多选问题', 'choices': ['选项1', '选项2'], 'answer': [20,30] },
                { 'type': 2, 'question': '填空问题' , 'answer': ['answer1', 'answer2']}]
            },
            ...

        ],
        "unread_notification_num": 10 
    },   
    "message": "Get missions successfully"
}
```
---

### 发布任务
**请求地址**
```
/mission/
```
**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--
token|是|123|登录返回的token
type|是|类型|0表示问卷，1表示其他
deadline|否|2019-5-1 14:40:20|结束时间,如果是取快递，就不需要(默认为3天)
title|是|"标题1"|标题
descrption|是|"描述"|任务描述
qq|否|123|联系信息四个必有其一
phone|否|183|
wechat|否|ousx|
other_way|否|其它|
bounty|是|100|赏金
max_num|否|10|最大接收人,默认为1
problems|否|"problems":[<br/>                { 'type': 0, 'question': '单选问题', 'choices': ['选项1', '选项2'], 'answer': [10,20]},<br/>                { 'type': 1, 'question': '多选问题', 'choices': ['选项1', '选项2'], 'answer': [20,30] },<br/>                { 'type': 2, 'question': '填空问题' , 'answer': ['answer1', 'answer2']}]<br/>|以数组形式上传

**返回示例**

```json
{
    "staus" : 200,
    "mission_id": 123,
    "message": "Create mission successfully"
}
```
---
### 取消或中断任务
- 问卷
    - 发布者可以取消
- 取快递
    - 取消，如果没人接，发布者可以取消
    - 放弃，领取者主动放弃

**请求地址**
```
/mission/
```
**HTTP方法**

PUT

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录返回的token|
mission_id|是|123456|id


**返回示例**
```json
{
    "staus" : 200,
    "message": "ok"
}
```

---
---
## 订单接口
mission和order的区别是order是领取者领取的时候产生。问卷类型的mission可以有多个order,而取快递类型的mission只有一个order。再者，order有每个人领取任务的时间，而mission没有。
### 查询个人领取订单
若查看个人发布的任务，使用/mission API

**请求地址**
```
/order/
```
**HTTP方法**

GET

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录时所用的token


**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "orders" : [{
            "order_id" : 1,
            "receiver_id": 123,
            "publisher_id": 124,
            "order_state": 1,
            "publisher_confirm":1,
            "receiver_confirm": 1,
            "receive_time": "2019-6-1 14:40:20",
            "finish_time": "2019-6-1 14:40:20",
            'publisher_id' : 1,
            'mission_id': 1,
            'title': '标题',
            'type': 1
        },...
        ]
    },
    "message": "ok"
}
```
----

### 创建个人订单
用户接单，产生订单。

**请求地址**
```
/order/
```
**HTTP方法**

POST

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录时所用的token
mission_id|是|123|任务id
wechat|否|123456789|如果是快递任务需要4种临时联系方式之一
qq|否|123456789|如果是快递任务需要4种临时联系方式之一
phone|否|1369039959+|如果是快递任务需要4种临时联系方式之一
other_way|否|'facebook号:123465'|如果是快递任务需要4种临时联系方式之一

**返回示例**
```json
{
    "staus" : 200,
    "order_id":123,
    "message": "ok"
}
```
---
### 确认个人订单

- 填问卷者要确认
- 取快递发布者要确认
**请求地址**
```
/order/
```
**HTTP方法**

PUT

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--
token|是|123|登录时所用的token
order_id|是|123|订单id
answers|否|[<br/>        0,(单选选第一个)<br/>        [0,1],（多选选第一和第二个）<br/>        '填空题答案'（填空题答案）<br/>    ]|问卷类型提交必须有

**返回示例**
```json
{
    "staus" : 200,
    "message": "Confirm order successfully"
}
```

---
---
## 通知接口
- 问卷填完或者到了截止时间通知**发布者**
- 快递任务接单，通知**发布者**，给出接单人信息
- 快递发布者确定订单完成, 通知**接单人**,到账通知
- 到了任务截止时间，**通知**双方任务未完成
- 接收者放弃，通知**发布者**

### 获取通知
**请求地址**
```
/notification/
```
**HTTP方法**

GET

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录返回的token

**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "notifications" : [{
            "n_id" : 123,
            "mission_id": "",
            "message": "这个message是后台生成还是怎样",
            "time":"2019-6-1 14:40:20",
            "has_read": True
        }, ...
        ]
    },
    "message": "ok"
}
```
---
### 修改通知已读情况 
**请求地址**
```
/notification/
```
**HTTP方法**

PUT

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录返回的token
notification|是|[{"n_id":123,"has_read":True}]|一个列表

**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "notifications" : [{
            "n_id" : 123,
            "mission_id": 123456,
            "message": "这个message是后台生成",
            "create_time":"2019-6-1 14:40:20",
            "has_read": True
        }, ...
        ]
    },
    "message": "ok"
}
```
----

----
### 删除通知 
**请求地址**
```
/notification/
```
**HTTP方法**

DELETE

**请求参数**

参数名 | 是否必须 | 示例值 | 描述
--|--|--|--|
token|是|123|登录返回的token
notification|是|[{"n_id":123},...]|一个


**返回示例**
```json
{
    "staus" : 200,
    "data" : {
        "notification" : [{
            "n_id" : 123
        }, ...
        ]
    },
    "message": "ok"
}
```
----