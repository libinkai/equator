# 大数据技术

## 大数据基本理念

- 基本理念：分而治之。通过分布式的存储与计算方案，平摊了存储与计算的压力。
- 分布式计算方案
  - 消息传递接口 MPI：多进程多节点数据通信解决方案，但是比较复杂，使用成本较高。
  - 映射规约模型 MapReduce：一种简单的分布式计算编程模型，Map就是分，Reduce就是治。

## 大数据相关技术生态

### Hadoop

| 技术         | 备注          |
| ------------ | ------------- |
| HDFS         | 分布式存储    |
| HBase        | 数据库        |
| Yarn         | 资源调度      |
| Zookeeper    | 协调管理      |
| Sqoop        | 数据管道      |
| Hive         | SQL on Hadoop |
| Spark        | 内存计算      |
| Flink、Kafka | 流处理        |

### Spark

- 比原生MapReduce更加友好；基于内存计算，速度更快。

| 技术            | 备注                   |
| --------------- | ---------------------- |
| Spark核心       |                        |
| Spark SQL       |                        |
| Spark Streaming | 流处理，基于mini-batch |
| MLLib           |                        |
| GraphX          |                        |

### Kafka

- Kafka作为消息队列一般作为不同系统之间的数据管道，其也有原生的流处理框架。

### Flink

- 第三代流处理技术（第一代是Storm，第二代是Spark Streaming）

- 优点
  - 支持多种时间语义，可以处理乱序到达数据
  - Exactly-Once保障
  - 毫秒级延迟
  - 简单易用的API
  - 易于拓展，生态丰富

## 大数据处理平台

### Lambda架构

- 为了保证实时性与准确性，同时采用批处理以及流处理对源数据进行处理

### Kappa架构

- 舍弃批处理层，批流合一

## 流处理基础

### 延迟与吞吐

- 延迟 Latency，表示一个时间被系统处理的总时间。分为平均延迟以及分位延迟。
- 吞吐 Throughout，表示一个系统最多可以处理多少时间。

- 延迟高，吞吐量一般就比较小。

### 窗口与时间

- 窗口
  - 滚动窗口 Tumbling Window，定长，窗口之间不包含重复数据。
  - 滑动窗口 Sliding Window，定长，窗口之间包含重复数据。
  - 会话窗口 Session Window 不定长，使用会话间隔（Window Gap）划分事件

- 时间语义
  - Event Time 事件实际发生的时间
  - Processing Time 事件被流处理引擎处理的时间

- Watermark
  - 控制数据接收的最长等待时间
- 状态与检查点
  - 计算分为有状态计算与无状态计算
  - 检查点主要是保存状态数据

- 数据一致性保障
  - At-Most-Once，可能丢数据
  - At-Least-Once，可能重复处理数据
  - Exactly-Once，不重不漏数据

# 安装配置

## 单节点

```yml
version: "2.1"
services:
  jobmanager:
    image: flink:1.9.2-scala_2.12
    hostname: jobmanager
    container_name: jobmanager
    expose:
      - "6123"
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager

  taskmanager1:
    image: flink:1.9.2-scala_2.12
    hostname: taskmanager1
    container_name: taskmanager1
    expose:
      - "6121"
      - "6122"
    depends_on:
      - jobmanager
    command: taskmanager
    links:
      - "jobmanager:jobmanager"
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
```

## 集群

```

```

