<!--TOC-->

* [UI Design](#UI Design)
  * [注册页面UI](#注册页面UI)
  * [登录页面UI](#登录页面UI)
  * [主页面UI](#主页面UI)
  * [用户信息详情UI](#用户信息详情UI)
  * [新建任务UI](#新建任务UI)
  * [问卷设计UI](#问卷设计UI)
  * [支付UI](#支付UI)
  * [提现UI](#提现UI)



## UI Design

包括以下8个UI的设计（其他UI有待进一步设计）：

1. 注册页面UI
2. 登录页面UI
3. 主页面UI
4. 用户信息详情UI
5. 新建任务UI
6. 问卷设计UI
7. 支付UI
8. 提现UI

---

### 注册页面UI

注册页面包括头像、用户名（昵称）、邮箱、密码、号码等信息

* 设计图如下：

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/register.png>)

* 实际注册UI：

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/register1.png)

---

### 登录页面UI

* 登录UI设计：

  登录方式可分为以下几种：

  1. 用户名密码登录
  2. 邮箱验证登录
  3. 短信验证登录

  以下即为不同的登录方式的不同UI（邮箱验证登录和短信验证登录一样）

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/login.png)

* 实际登录UI：

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/login1.png)

---

### 主页面UI

* 主页面UI设计：

  主页面主要分成四部分：

  1. 左上角为用户基本信息
  2. 左下角为用户相关任务栏
  3. 右上角为功能栏，包括新建任务等
  4. 右下角为任务列表（占页面大部分）

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/mainpage.png>)

* 实际主页面UI：

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/mainpage1.png)

  * 左上角为用户基本信息
  * 左下角为用户相关任务栏
  * 右上角为功能栏，其中广场为展示现有任务
  * 右下角为发布任务按钮

  

  左边侧栏相关页面UI：

  * 任务发布历史UI：

    ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/published_history.png>)

  * 任务领取历史UI：

    ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/received_history.png>)

  * 消息通知UI：

    ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/notificationpage.png>)

  

---

### 用户信息详情UI

* 用户信息详情UI设计：

  用户信息包括：

  1. 头像
  2. 用户名
  3. 信誉积分
  4. 余额
  5. 邮箱
  6. 号码
  7. ...

  其中用户名、信誉积分、余额（可提现）是不可修改的，其他均可修改，需要修改密码时，弹框确定新密码

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/user_info.png)

* 实际用户信息详情UI：

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/user_info1.png)

---

### 新建任务UI

* 新建任务UI设计：

  任务类型可选，其中选择问卷设计（发布）跳转至问卷设计页面，其他任务共享此页面

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/new_mission.png>)

* 实际新建任务UI：

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/publish_other_mission.png)

  **其他任务详情（可在发布/领取历史中点击相关条目进行查看）：**

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/other_mission_detail.png>)

---

### 问卷设计UI

* 问卷设计UI：

  独立的任务UI，可以用户自行设计问卷题目等

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/survey_design.png>)

* 实际问卷设计UI：

  * 点击左边三个按钮选择题目类型并添加题目
  * 右侧为问卷详情，可对问题进行修改、删除和上下移位
  * 问卷下方可填写该问卷发布的信息设置（需点击灰色按钮‘问卷信息设置’才能填写）

  ![](https://github.com/penglsh/images/raw/master/sad_UI_design/publish_survey_mission.png)

  

  **问卷信息概览（仅发布者可见）：**

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/survey_design_scan.png>)

  **问卷填写页面：**

  ![]()

  **问卷结果统计页面（仅发布者可见）：**

  ![]()

---

### 支付UI

* 支付UI设计：

  发布任务时需支付酬金，可选支付方式

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/pay.png>)

* 实际支付UI设计：

  因为任务发布时会询问用户是否确认发布该任务，发布即自动支付，若无人领取该任务，则会返还金额

---

### 提现UI

* 提现UI：

  提现余额UI

  ![](<https://github.com/penglsh/images/raw/master/sad_UI_design/withdraw.png>)

* 实际提现UI：

  暂无

---

**注**：以上UI均未完善

