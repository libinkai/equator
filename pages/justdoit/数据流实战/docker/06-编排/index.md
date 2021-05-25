# 编排

- 自动化可减少或取代对 IT 系统的人工操作，编排是指自动执行不同系统中多个步骤的流程或工作流。容器编排是指自动化地进行容器的部署、管理、扩展和联网。

# Docker Compose

## 安装

- [官网安装教程](https://docs.docker.com/compose/install/)

## 基本使用

1. 编写`docker file`文件（如果有必要的话）
2. 编写`docker-compose.yml`配置文件
3. `docker-compose up `启动项目

## 配置文件语法

- [菜鸟教程docker compose语法](https://www.runoob.com/docker/docker-compose.html)

```yaml
version: // compose版本
services:
	service1:
		image: // docker命令
		build:
		ports:
		depends_on: other_service // 声明依赖的服务，启动顺序
	service2:
[other_config]:
```

