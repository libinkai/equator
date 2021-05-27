# 工作流程

- 消息分区内有序

![img](log_anatomy.png)

- topic是逻辑上的概念，partition是物理上的概念，每个partition对应一个log文件，该log文件存储的是producer生产的消息，每条消息都会有offset。消费者消费数据时，会记录自己消费的offset。

# 文件存储

- 为了避免log文件过大导致消息定位困难，Kafka采取分片与索引机制：一个topic下有多个partition，一个partition下有多个segment。

```
*.log		文件
*.index 	索引
*.log与*.index命名规则是当前segment的第一条消息的offset
查找数据时，先通过二分查找方法查找index文件，再查找log文件。此外，log文件中每条消息大小相同，可以通过计算快速定位到对应的数据。
*.log保存的是序列化后的消息
*.index保存的是(offset,起始偏移量)
```

# 生产者

## 分区策略

### 分区的原因

1. 提高并发度，以partition为单位进行读写，分散读写压力
2. 便于集群拓展，一个topic下partition的数量可以根据实际情况调整

### 分区的原则

- 生产者生产的消息会被封装为`ProducerRecord`对象
  - topic [required]
  - partition
  - timestamp
  - key
  - value [required]
  - headers

- partition选择流程
  - 指定了partition，发送到指定的partition
  - 没有指定partition，但是指定了key，`partition=hash(key)%num_partition`
  - partition与key均没指定，进行轮询（round-robin）。

## 生产者ISR

### 数据可靠性

- 为保证数据的可靠性，topic下的partition收到producer生产的消息后，需要返回ack信息。如果producer没有接收到ack信息，则会重新发送消息。
- 使用副本机制保证数据可靠性有两种策略
  - 半数以上follower完成同步，认为写成功。延迟较低，为了容忍n台节点的故障，需要2n+1个副本。
  - 全部follower完成同步，认为写成功。延迟较高，为了容忍n台节点的故障，需要n+1个副本。
  - Kafka需要全部follower完成同步后才认为写入成功，发送ack消息。原因是半数机制会导致大量的数据冗余，而网络延迟对Kafka影响不大。

### ISR机制

- ISR机制避免数据同步过程中，由于某个follower节点宕机无法完成同步导致leader等待时间过长。ISR（in-sync replica set），即与leader保持同步的follower集合。ISR是动态的，follower超过`replica.lag.time.max.ms`时间未完成数据同步，则会被踢出ISR。leader宕机时，从ISR中选举新的Leader。
- ISR选择follower的条件
  - 同步消息条数（0.9之后版本废弃该条件，因为生产者是批量发送数据的，当batch_size大于消息条数差值时，会导致节点频繁进出ISR）
  - 同步消息耗时

## 生产者ACK机制

- 不同的消息重要性可能不一样，Kafka提供不同的ack策略。`acks`参数配置ack策略。
- `ack=0`，producer不等待broker的ack消息，有可能丢失数据。
- `ack=1`，leader成功落盘后返回ack消息。follower数据同步成功之前，leader宕机，有可能丢失数据。
- `ack=-1|all`，producer等待leader与全部follower成功落盘后才返回的ack。follower数据同步成功后，broker发送ack之前，leader宕机，会导致数据重复（producer没有收到ack消息会重新发送数据）。极端情况下，ISR没有其它可用节点，仍可能丢失数据。

## 数据一致性问题

> 当leader与众多follower之间的消息offset不一致时，该如何解决一致性问题？

![image-20210527214111877](image-20210527214111877.png)

- 高水位与低水位
  - LEO（Log End Offset），每个副本最后一个offset。
  - HW（High Watermark），ISR所有副本中最小的LEO。
  - HW之前的消息才对consumer可见，保险起见的数据对齐方案。

- 故障恢复
  - follower故障：follower故障被踢出ISR，恢复后，该follower会舍弃HW后的数据，并向leader进行数据同步直到LEO大于等于HW，重新加入ISR。
  - leader故障，选择新的leader后，其余follower会将HW后的数据丢弃，从新leader同步数据。
  - 水位机制只能保证副本之间的数据一致性（消费者角度的数据一致性），而不是保证不重复不遗漏数据。

## ExactlyOnce

- ack策略设置为-1，可以（基本）保证数据不丢失，即At Least Once
- ack策略设置为0，保证消息只被生产者发送一次，即At Most Once
- 既不丢失数据也不重复数据，即Exactly Once。0.11版本后的Kafka引入幂等性特性间接实现Exactly Once，即在broker去重。`Exactly Once=幂等性+At Least Once`
- `enable.idempotentence`设置为true开启幂等性特性，Producer会被分配一个PID，发送到同一个partition的消息有一个Sequence Number，Broker使用(PID,Partition,Sequence Number)三元组缓存去重。
- Producer重启后PID会变化。幂等性无法支持跨分区，跨会话的Exactly Once。

# 消费者

## 消费方式

## 分区分配策略

## offset保存机制

## 消费者组

# 高效读写

# Zookeeper与Kafka

# Ranger分区

# 事务



