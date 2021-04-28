# Docker安装&配置

## 安装

- 查看linux版本

  ```shell
  cat /etc/redhat-releaseDocker
  ```

- 安装相关软件

  ```
  yum install -y yum-utils device-mapper- persistent-data lvm2
  ```

- 配置稳定的仓库

  ```
  yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  ```

- 安装docker

  ```
  yum install -y docker-ce docker-ce-cli containerd.io
  ```

## 加速

```shell
//登录阿里云，获取加速链接
/etc/docker/daemon.json

{
  "registry-mirrors": ["https://5whzerwg.mirror.aliyuncs.com"]
}
```

# Docker三要素

1. 镜像 image
2. 容器，镜像的实例
3. 仓库，存放镜像的地方

# Docker命令

## 帮助命令

- 查看版本

  ```shell
  docker version
  ```

- 查看个人信息描述

  ```shell
  docker info
  ```

- 查看帮助

  ```shell
  docker --help
  ```

## 镜像命令

### 列出本地主机上面的镜像

```shell
docker images
```

- 输出说明
  - REPOSITORY：镜像的仓库源
  - TAG：镜像的标签，同一个镜像源可以有不同的TAG，表示仓库源的不同版本，使用REPOSITORY:TAG来定义不同的镜像，默认为latest
  - IMAGE ID：镜像ID
  - CREATED：镜像创建的时间
  - SIZE：镜像大小
- OPTIONS
  - -a 列出所有的镜像（包含中间映像层），有的镜像包含很多层
  - -q只显示镜像ID
  - --digests显示镜像的摘要信息
  - --no-trunc显示位完整的镜像信息

### 搜索仓库中的镜像

```shell
docker search image_name
```

- OPTIONS
  - --no-trunc显示位完整的镜像信息
  - -s 列出收藏数不小于指定数目的镜像
  - --automated只列出automated build类型的镜像（自动构建）

### 将远程仓库的镜像拉取到本地

```shell
docker pull image_name:TAG
```

### 删除镜像

```shell
docker rmi -f image_id:TAG //强制删除

docker rmi -f image_id:TAG image_id:TAG //删除多个镜像

docker rmi -f $(docker images -qa) //全部删除
```

## 容器命令

### 新建并启动容器

```shell
docker run [OPTIONS] IMAGE [COMMAND][ARG...]
```

- OPTIONS说明
  - --name="name" 为容器指定一个名字
  - -d 后台运行容器，并返回容器ID（即启动守护进程）
  - -i 以交互式模式运行容器
  - -t 为容器重新分配一个伪终端 
  - -P 随机分配端口：随机分配外部端口
  - -p  指定映射端口 外部接口:内部接口
  - 

### 查看当前正在运行的容器

```shell
docker ps [OPTIONS]
```

- OPTIONS说明
  - -a 显示全部容器
  - -l 显示最近创建的容器
  - -n 显示最近n个创建的容器
  - -q 静默模式，只显示容器编号
  - --no-trunc 不截断输出

### 关闭容器

1. exit 停止退出
2. ctrl+P+Q 暂时离开，挂起

### 启动容器

```shell
docker start container_id
```

### 重启容器

```shell
docker restart container_id
```

### 停止容器

```shell
docker stop container_id //平滑停止

docker kill container_id //强制停止

```

### 删除已停止的容器

```shell
docker rm container_id

docker rm -f container_id //强制删除
```

删除多个容器

```shell
docker rm -f $(docker ps -a -q)
或者
docker ps -a -q | xargs docker rm
```

### 启动守护进程

```shell
docker run -d image
```

- 注意，docker容器后台运行，必须有一个前台进程，否则会自动退出。解决方法，将进程以前台进程的形式运行

### 查看容器日志

```shell
docker logs container_id [OPTIONS] 
```

- OPTIONS说明
  - -t加入时间戳
  - -f跟随最新的日志打印
  - --tail 数字 显示最后几条数据

### 查看容器内进程

> 可以把容器看做简易版的Linux环境（包括root权限，进程空间，用户进程，网络空间）以及运行在其中的应用

```shell
docker top container_id
```

### 查看容器内部细节

```shell
docker inspect container_id
```

### 进入正在运行的容器并以命令行进行交互

```shell
docker exec -it 容器ID bashShell //bashShell可以是一段shell程序，直接返回shell的执行结果，也可以是/bin/bash，表示进入终端再操作

docker attach 容器ID //重新进入，不会创建新的进程
```

### 从容器内拷贝文件到主机上面

```shell
docker cp container_id:container_source_path target_path
```

### 提交容器副本使之成为一个新的镜像

```shell
docker commit -m "提交的描述信息" -a="作者信息" container_id 目标镜像名:TAG
```



# Docker镜像

> 镜像是一种轻量级的，可执行的独立软件包，用来打包软件运行环境和基于运行环境开发的软件，它包含某个软件所需要的所有内容，包括代码，运行时库，环境变量和配置文件

## UnionFileSystem

- Union File System 联合文件系统，分层的，轻量级高性能的文件系统，它支持对文件系统的修改作为一次提交来一层一层地叠加，同时将不同目录挂载到一个虚拟文件系统下面。UnionFileSystem是Docker镜像的基础
- docker里面的镜像一般比普通的安装包大，这是因为该镜像中包含了基础环境
- 联合文件系统的好处：共享资源

## 镜像加载原理

- Boot File System，主要包含bootloader与kernel，bootloader主要用于加载kernel

# 容器数据卷

> Docker容器产生的数据，如果不通过docker commit生成新的镜像，使得数据成为镜像的一部分保存下来，那么当容器删除之后，其数据也会随机消失

## 容器数据卷的作用

1. 容器的持久化
2. 容器间继承+共享数据

## 数据卷添加

### 直接命令添加

- 添加数据卷

```shell
docker run -it -v /宿主机绝对路径:/容器内路径 镜像名
//目录会自动创建
//即宿主机与容器共用一块硬盘
//容器退出之后，宿主机对数据卷的修改仍然对容器可见
```

- 查看数据卷是否挂载成功

```shell
docker inspect container_id

查看 Volumes
```

- 权限限制 root only

```shell
docker run -it -v /宿主机绝对路径:/容器内路径:ro 镜像名

//在container里面只能读数据卷里面的数据
```

### DockerFile添加

## 数据卷容器

> 命名的容器挂载数据卷，其它容器通过挂载这个父容器实现数据共享，挂载数据卷的容器，称之为数据卷容器

```shell
docker run -it --name xxx --volumes-from parent_container parent_image
//继承的容器之间数据共享

//容器之间配置信息的传递，数据卷的生命周期一致持续到没有容器使用它为止
```

# DockerFile

> DockerFile是用来构建Docker镜像的构建文件，是由一系列命令和参数构成的脚本

- 三部曲：code、build、run

  ```shell
  docker build -f docker_file_path -t image:TAG

  //当dockerFile文件名为DockerFile时，[-f docker_file_path]可以省略，默认在当前目录下构建DockerFile文件
  //image:TAG为目标镜像名，TAG默认为latest
  ```

  

## DockerFile构建过程

### 基础语法

1. 每条保留字指令必须都为大写字母而且其后面必须至少带有一个参数
2. 指令按照从上到下顺序执行
3. \#表示注释
4. 每条指令都会创建一个新的镜像层并对镜像进行提交

### 执行流程

1. docker从基础镜像运行一个容器
2. 执行一条指令并对容器进行修改
3. 执行类似于commit的操作提交一个新的镜像层
4. docker再基于刚提交的镜像运行一个新的容器
5. 执行dockerfile中下一条指令直到所有指令执行完毕

### 保留字指令

#### FROM

- 声明基础镜像（当前镜像基于哪个镜像）

#### MAINTAINER

- 镜像维护者的信息（姓名和邮箱）

#### RUN

- 容器构建时需要运行的命令

#### EXPOSE

- 当前容器对外暴露的端口

#### WORKDIR

- 指定创建容器过后，终端默认登录的工作目录（落脚点）

#### ENV

- 用来构建镜像过程中设置环境变量

#### ADD

- 拷贝+解压，会自动处理URL与解压缩
- ADD 构建源目录 容器目标目录

#### COPY

- 拷贝

#### VOLUME

- 容器数据卷，用于数据保存和持久化工作

#### CMD

- 容器启动命令

```shell
1. CMD <shell风格命令>
2. CMD <可执行文件，参数1，参数2>

//命令格式
shell格式：RUN yum -y install vim
或者
字符串数组 ：RUN ["curl","-s","http://ip.cn"]
```

- dockerFile中可以用许多CMD命令，但是只有最后一个生效，CMD会被docker run之后的参数替换

#### ENTRYPOINT

- 类似于CMD，但是ENTRYPOINT不会被docker run命令之后的参数替换，其会把参数追加到命令后面

#### ONBUILD

- 父镜像在被子继承之后父镜像的onbuild被触发（回调函数），在构建过程中触发

