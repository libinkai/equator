# 数据流实战

- 记录Docker、Kafka、Hadoop、Zookeeper、Flink等数据开发技术的学习过程。可以按照给出的学习资料学习，不用看我的，我的文字主要是实战记录，脉络框架也是参考其他人的。
- 本系列希望达到的目标：利用Docker搭建所需集群，使用Kafka模拟用户行为流数据，使用Flink进行处理，后续可能会引入推荐系统方面的知识。
- 前置知识
  - Java服务端开发知识
  - Linux知识

# Docker

> Docker可谓是不得不学的一门技术，有了它，可以更加快速地配置我们的各种环境，抹平了各平台的环境差异性。
>
> 推荐的学习资源：
>
> 哔哩哔哩的UP：遇见狂神说，[有视频教程](https://www.bilibili.com/video/BV1og4y1q7M4?from=search&seid=459300085567044738)，讲得比较通俗易懂。
>
> 微信读书上有的书：《每天5分钟玩转Docker容器技术》。

- [初体验](./docker/01-初体验/index.md)
- [镜像](./docker/02-镜像/index.md)
- [容器](./docker/03-容器/index.md)
- [网络](./docker/04-网络/index.md)
- [存储](./docker/05-存储/index.md)

------

> 实际上，容器的编排与集群部署往往使用K8S

- [编排](./docker/06-编排/index.md)
- [集群](./docker/07-集群/index.md)

# Zookeeper

> 集群节点之间的协调者。
>
> 视频教程主要有：[尚硅谷的视频](https://www.bilibili.com/video/BV1PW411r7iP?from=search&seid=5377547783698726294)

- [初体验（包含集群搭建）](./zookeeper/01-初体验/index.md)
- [使用教程](./zookeeper/02-使用教程/index.md)
- [原理](./zookeeper/03-原理/index.md)

# Kafka

> 一种消息队列，常常用于流处理的数据管道。

- [初体验（包含集群搭建）](./kafka/01-初体验/index.md)

# Hadoop

> 分布式系统基础框架，适合做批处理。
>
> 视频教程：[尚硅谷的视频](https://www.bilibili.com/video/BV1cW411r7c5)

# Flink

> 批流合一的数据处理框架。