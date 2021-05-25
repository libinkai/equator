# 概述

# 安装配置

## 单机

## 集群

### 创建自定义网络

```
docker network create --driver=bridge --subnet=172.18.0.0/16 --gateway=172.18.0.1 my-cluster-network
```

| 服务       | IP         | 端口（主机:容器） |
| ---------- | ---------- | ----------------- |
| zookeeper1 | 172.18.1.1 | 2181:2181         |
| zookeeper2 | 172.18.1.2 | 2182:2181         |
| zookeeper3 | 172.18.1.3 | 2183:2181         |
| kafka1     | 172.18.2.1 | 9092:9092         |
| kafka2     | 172.18.2.2 | 9093:9092         |
| kafka3     | 172.18.2.3 | 9094:9092         |

### 编写配置文件

> yml文件可以使用IDEA或者pycharm格式化一下，然后使用[网站](https://www.bejson.com/validators/yaml_editor/)校验一下

- 编写`docker-compose.yml`配置文件

```yml
version: '3'
services:
  zoo1:
    image: zookeeper:3.4
    restart: always
    hostname: zoo1
    container_name: zoo1
    ports:
      - 2181:2181
    volumes:
      - "/usr/workspace/volumes/zkcluster/zoo1/data:/data"
      - "/usr/workspace/volumes/zkcluster/zoo1/datalog:/datalog"
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888
    networks:
      my-cluster-network:
        ipv4_address: 172.18.1.1

  zoo2:
    image: zookeeper:3.4
    restart: always
    hostname: zoo2
    container_name: zoo2
    ports:
      - 2182:2181
    volumes:
      - "/usr/workspace/volumes/zkcluster/zoo2/data:/data"
      - "/usr/workspace/volumes/zkcluster/zoo2/datalog:/datalog"
    environment:
      ZOO_MY_ID: 2
      ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888
    networks:
      my-cluster-network:
        ipv4_address: 172.18.1.2

  zoo3:
    image: zookeeper:3.4
    restart: always
    hostname: zoo3
    container_name: zoo3
    ports:
      - 2183:2181
    volumes:
      - "/usr/workspace/volumes/zkcluster/zoo3/data:/data"
      - "/usr/workspace/volumes/zkcluster/zoo3/datalog:/datalog"
    environment:
      ZOO_MY_ID: 3
      ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888
    networks:
      my-cluster-network:
        ipv4_address: 172.18.1.3

  kafka1:
    image: wurstmeister/kafka:2.12-2.4.1
    restart: always
    hostname: kafka1
    container_name: kafka1
    privileged: true
    ports:
      - 9092:9092
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka1
      KAFKA_LISTENERS: PLAINTEXT://kafka1:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:9092
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_ZOOKEEPER_CONNECT: zoo1:2181,zoo2:2181,zoo3:2181
    volumes:
      - "/usr/workspace/volumes/kafkaCluster/kafka1/logs:/kafka"
    networks:
      my-cluster-network:
        ipv4_address: 172.18.2.1
    depends_on:
      - zoo1
      - zoo2
      - zoo3

  kafka2:
    image: wurstmeister/kafka:2.12-2.4.1
    restart: always
    hostname: kafka2
    container_name: kafka2
    privileged: true
    ports:
      - 9093:9092
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka2
      KAFKA_LISTENERS: PLAINTEXT://kafka2:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka2:9092
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_ZOOKEEPER_CONNECT: zoo1:2181,zoo2:2181,zoo3:2181
    volumes:
      - "/usr/workspace/volumes/kafkaCluster/kafka2/logs:/kafka"
    networks:
      my-cluster-network:
        ipv4_address: 172.18.2.2
    depends_on:
      - zoo1
      - zoo2
      - zoo3

  kafka3:
    image: wurstmeister/kafka:2.12-2.4.1
    restart: always
    hostname: kafka3
    container_name: kafka3
    privileged: true
    ports:
      - 9094:9092
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka3
      KAFKA_LISTENERS: PLAINTEXT://kafka3:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka3:9092
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_ZOOKEEPER_CONNECT: zoo1:2181,zoo2:2181,zoo3:2181
    volumes:
      - "/usr/workspace/volumes/kafkaCluster/kafka3/logs:/kafka"
    networks:
      my-cluster-network:
        ipv4_address: 172.18.2.3
    depends_on:
      - zoo1
      - zoo2
      - zoo3

networks:
  my-cluster-network:
    external:
      name: my-cluster-network
```

- 说明

```
- extra_hosts，添加主机名映射，将会在/etc/hosts创建记录
- external_links，容器互连
- 以上两个参数，在使用自定义网络之后，一般不再需要了。容器之间直接可以互连，也可以通过容器名称访问。

zookeeper端口说明：
	代码访问client的端口号： 2181
	leader和flower通信的端口号： 2888
	选举leader时通信的端口号： 3888
```

### 启动

- 启动docker compose：`docker-compose -f docker-compose.yml up -d`

![image-20210525222804044](image-20210525222804044.png)

### 测试

```
# 生产者生产数据
docker exec -it kafka1 bash

cd /opt/kafka_2.12-2.4.1/bin/

kafka-topics.sh --create --topic mytopic --replication-factor 3 --partitions 2 --zookeeper zoo1:2181

kafka-topics.sh --list --zookeeper zoo1:2181

kafka-console-producer.sh --broker-list kafka1:9092 --topic mytopic

# 消费者消费数据
docker exec -it kafka2 bash

cd /opt/kafka_2.12-2.4.1/bin

kafka-console-consumer.sh --bootstrap-server kafka1:9092 --topic mytopic --from-beginning
```

![image-20210525224147282](image-20210525224147282.png)

![image-20210525224250517](image-20210525224250517.png)

