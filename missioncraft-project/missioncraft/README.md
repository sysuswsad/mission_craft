
## 启动服务器：

For Linux and Mac:
```
export FLASK_APP=missioncraft
export FLASK_ENV=development
flask run
```
For Windows cmd, use set instead of export:
```
set FLASK_APP=missioncraft
set FLASK_ENV=development 
flask run
```
For Windows PowerShell, use $env: instead of export:
```
$env:FLASK_APP = "missioncraft"
$env:FLASK_ENV = "development"
flask run
```


## 初始化数据库：
```
flask init-db
```

## 浏览器访问:  
```
http://127.0.0.1:5000/auth/register
http://127.0.0.1:5000/auth/login
```


