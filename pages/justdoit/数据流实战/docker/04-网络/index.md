# Docker网络

## 概述

- 网络定义了容器之间以及容器与外界之间如何通信的。

- 通过`docker network ls`可以查看网络列表

- 默认情况下，Docker会自动创建三个网络：none、host、bridge。

  ![image-20210523222506462](image-20210523222506462.png)

- 启动容器是通过`--network=network_type`参数指定使用的网络模式。
- 通过命令`docker network inspect network_type`查看网络详情。

## None网络

- 完全隔离的无网络状态，适用于安全性要求高的容器。

![image-20210523223334647](image-20210523223334647.png)

## Host 网络

- 共享主机的网络。

![image-20210523223612800](image-20210523223612800.png)

## Bridge 网络

- 默认的网络模式

![image-20210523224044472](image-20210523224044472.png)

![image-20210523223506783](image-20210523223506783.png)

- Docker会自动创建一个docker0的网卡，通过`veth pair`技术将容器的网卡与docker0进行连接。

##自定义网络