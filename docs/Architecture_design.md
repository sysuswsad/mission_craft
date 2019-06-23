# 软件架构文档（Software Architecture Document, SAD）

## 架构问题

## 可靠性

- 因素：当多人同时在线时，应用能正常运行。
- 动机：这是让用户有良好的体验的基础。
- 对于成功的优先级 ：高
- 困难或风险：中等

## 可用性

- 因素：用户等待时间不超过3秒。
- 动机：这是让用户有良好的体验的基础。
- 对于成功的优先级 ：高
- 困难或风险：中等

## 解决方案说明

Flask是一个web框架，而非web server，直接用Flask拉起的web服务仅限于开发环境使用，生产环境不够稳定，也无法承受大量请求的并发，在生茶环境下需要使用服务器软件来处理各种请求，如Gunicorn、 Nginx或Apache，而Gunicorn+Nginx的搭配，好处多多，一方面基于Nginx转发Gunicorn服务，在生产环境下能补充Gunicorn服务在某些情况下的不足，另一方面，如果做一个Web网站，除了服务外，还有很多静态文件需要被托管，这是Nginx的强项，也是Gunicorn不适合做的事情。所以，基于Flask开发的网站，部署时用Gunicorn和Nginx，是一个很好的选择。

Nginx功能强大，使用Nginx有诸多好处，但用Nginx转发Gunicorn服务，重点是解决“慢客户端行为”给服务器带来的性能降低问题；另外，在互联网上部署HTTP服务时，还要考虑的“快客户端响应”、SSL处理和高并发等问题，而这些问题在Nginx上一并能搞定，所以在Gunicorn服务之上加一层Nginx反向代理，是个一举多得的部署方案。


## 逻辑视图

![逻辑](https://github.com/sysuswsad/mission_craft/raw/master/docs/imgs/logic_layer.png)

## 物理视图

![部署](https://github.com/sysuswsad/mission_craft/raw/master/docs/imgs/physical_layer.png)