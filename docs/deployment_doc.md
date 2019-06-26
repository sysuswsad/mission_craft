# 部署文档




## 部署流程

下载项目文件：

```bash
git clone https://github.com/sysuswsad/mission_craft.git
```



### 前端服务器部署流程

#### 环境配置

确保系统安装了npm，若没有，可通过以下链接下载安装：

[npm下载](https://www.npmjs.com/)

#### 安装前端服务器所需依赖包

进入文件 package.json 所在目录：

```bash
cd ~/mission_craft/missioncraft-project
```

安装依赖模块：

```bash
npm i
```



#### 运行前端服务器

进入项目：

```bash
cd ~/mission_craft/missioncraft-project 
```



运行服务器：

```bash
npm serve
```



### 后端服务器部署流程

#### 环境配置

确保系统安装了python3 和 pip3，若没有，可通过以下链接下载安装：

[Python下载](https://www.python.org/downloads/)

确保系统安装了SQLite3，若没有，可通过以下链接下载安装：

[SQLite3下载](https://www.sqlite.org/download.html)



#### 安装后端服务器所需依赖包

进入项目：

```bash
cd ~/mission_craft
```



安装依赖包：

```bash
pip install -r missioncraft-project/requirements.txt
```



#### 运行后端服务器

进入项目：

```bash
cd ~/mission_craft/missioncraft-project 
```



初始化数据库：

```bash
flask init-db
```



运行服务器：

```bash
flask run
```

