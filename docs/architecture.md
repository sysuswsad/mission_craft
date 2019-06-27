# 架构设计、详细设计（BCE方法）到应用程序框架映射指南
## 逻辑架构
逻辑架构由四层模型（表示层、业务层、服务层、持久化层）构成

### 表示层
用户端使用 Web 作为表示层，提供任务信息管理子系统、问卷系统、用户管理系统、订单管理子系统、通知系统

### 业务层
服务器充当业务层的角色，为表示层的各个子系统提供相应的服务模块，翻译用户的输入并依照用户的输入调用服务

### 服务层
从各种数据访问对象检索和创建模型，更新各个存储库的值，执行特定于应用程序的逻辑和操作等。

### 持久化层
SQLite3 提供了数据的持久化服务

## 框架目录设计
### 前端

```bash
.                                   //前端开发的源码
├── App.vue                         //应用的最外层结构
├── assets                          //图片等静态资源
│   ├── flask-logo.png
│   ├── logo.png
│   ├── python-logo.png
│   └── vue-logo.png
├── backend.js                      //与后端接口
├── components                      //前端组件
│   ├── HelloWorld.vue
│   ├── SideBar.vue
│   ├── TimeSlider.vue
│   └── TopMenu.vue
├── filters.js
├── main.js
├── router.js                       //前端路由
├── store.js                        //应用的全局数据状态管理
├── theme
│   └── element
│       ├── alert.css
│       ├── aside.css
│       ├── autocomplete.css
│       ├── badge.css
│       ├── base.css
│       ├── breadcrumb-item.css
│       ├── breadcrumb.css
│       ├── button-group.css
│       ├── button.css
│       ├── calendar.css
│       ├── card.css
│       ├── carousel-item.css
│       ├── carousel.css
│       ├── cascader.css
│       ├── checkbox-button.css
│       ├── checkbox-group.css
│       ├── checkbox.css
│       ├── col.css
│       ├── collapse-item.css
│       ├── collapse.css
│       ├── color-picker.css
│       ├── container.css
│       ├── date-picker.css
│       ├── dialog.css
│       ├── display.css
│       ├── divider.css
│       ├── dropdown-item.css
│       ├── dropdown-menu.css
│       ├── dropdown.css
│       ├── fonts
│       │   ├── element-icons.ttf
│       │   └── element-icons.woff
│       ├── footer.css
│       ├── form-item.css
│       ├── form.css
│       ├── header.css
│       ├── icon.css
│       ├── image.css
│       ├── index.css
│       ├── input-number.css
│       ├── input.css
│       ├── link.css
│       ├── loading.css
│       ├── main.css
│       ├── menu-item-group.css
│       ├── menu-item.css
│       ├── menu.css
│       ├── message-box.css
│       ├── message.css
│       ├── notification.css
│       ├── option-group.css
│       ├── option.css
│       ├── pagination.css
│       ├── popover.css
│       ├── popper.css
│       ├── progress.css
│       ├── radio-button.css
│       ├── radio-group.css
│       ├── radio.css
│       ├── rate.css
│       ├── reset.css
│       ├── row.css
│       ├── scrollbar.css
│       ├── select-dropdown.css
│       ├── select.css
│       ├── slider.css
│       ├── spinner.css
│       ├── step.css
│       ├── steps.css
│       ├── submenu.css
│       ├── switch.css
│       ├── tab-pane.css
│       ├── table-column.css
│       ├── table.css
│       ├── tabs.css
│       ├── tag.css
│       ├── time-picker.css
│       ├── time-select.css
│       ├── timeline-item.css
│       ├── timeline.css
│       ├── tooltip.css
│       ├── transfer.css
│       ├── tree.css
│       └── upload.css
└── views
    ├── AnswerQuestionnairePage.vue
    ├── Api.vue
    ├── Home.vue
    ├── LoginPage.vue
    ├── MessagePage.vue
    ├── PublishMissionPage.vue
    ├── PublishedPage.vue
    ├── QuestionnairePage.vue
    ├── ReceivedPage.vue
    ├── RegisterPage.vue
    ├── SquarePage.vue
    ├── StatisticPage.vue
    └── UserInfoPage.vue
```



### 后端  

```bash
.
├── __init__.py
├── api                     //与前端接口
│   ├── __init__.py
│   ├── mission.py          //任务api
│   ├── notification.py     //通知api
│   ├── order.py            //订单api
│   └── user.py             //用户api
├── auth.py                 //身份认证组件
├── currency.py				//货币系统组件
├── db.py                   //数据库交互组件
├── email.py                //发送邮件验证码组件
├── response_code.py		//状态码组件
├── schema.sql              //数据库创建sql文件
├── static              	//静态文件夹存储用户头像
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 2.png
│   ├── 3.jpg
│   └── logo.png
├── statistics.py			//问卷统计组件
└── verification.py         //邮箱真实性验证组件
```


## ECB
- **Boundary 对象**：表示参与者与系统之间进行的交互以及信息交流  
- **Controller 对象**：一个用例具有的事件流的控制行为
  - Boundary 发生的用户事件消息，皆是 Controller 的方法。
  - 以下都是不正确的交互：
    - UI 有箭头指向模型
    - 模型有箭头指向控制器。或控制器有除创建之外的箭头指向界面
    - 无论安卓或web，控制器都设计为多用户，即控制器不包含状态变量
  - 不能考虑多线程，使用多线程更新界面。要使用回调函数（消息）机制完成异步操作。  

- **Entity 对象**：表示数据库中存储的信息及相关行为
  - 从 Domain Model 获取属性
  - 如果模型之间存在关联，请将关系转化为合适的实现（关联属性）
  - 将 Controller 消息转化为方法

## 映射指南：
项目框架基本上是经典的三层架构，前端UI和业务逻辑是Vue.js，后端接受请求并返回数据是JSON数据类型，数据库是SQLite3。逻辑图对应目录结构是UI层（Vue.js）对应目录front-end（前端），中间Domain层主要对应目录back-end，处理请求并返回数据的逻辑是在user.py、mission.py、order.py、notification.py中，db.py主要是对数据库的管理。最后，数据库存在于db.sqlite3中，非常典型的三层架构。ECB的对应则是Boundary对应UI层（前端），Controller对应Domain（后端），Entity对应Technical Services（数据库）。
