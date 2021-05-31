# 命令

> 命令行中使用Kafka，一般用于测试

## Topic

### 查看

- 查看主题列表，`kafka-topics.sh --list --zookeeper zoo1:2181`

### 增加

- 创建主题，`kafka-topics.sh --create --topic mytopic --replication-factor 3 --partitions 2 --zookeeper zoo1:2181`
- `partitions`必须小于等于broker的数量，`replication-factor`与broker的数量没有必然的关系

### 删除

- 删除主题，`kafka-topics.sh --delete --topic mytopic --zookeeper zoo1:2181`

### 查看主题元数据

- 查看主题数据，`kafka-topics.sh --describe --topic mytopic --zookeeper zoo1:2181`

![image-20210526213158686](image-20210526213158686.png)

![image-20210526213556752](image-20210526213556752.png)

## Producer

### 生产数据

- `kafka-console-producer.sh --broker-list kafka1:9092 --topic mytopic`

![image-20210526221101536](image-20210526221101536.png)

## Consumer

### 消费数据

- ~~kafka-console-consumer.sh --zookeeper zoo1:2181 --topic mytopic --from-beginning~~ ，已过时。0.9版本之后，Kafka消费者不使用zookeeper保存数据。

- `kafka-console-consumer.sh --bootstrap-server kafka1:9092 --topic mytopic --from-beginning`。
  - `--from-beginning`，从头开始消费

![image-20210526221213352](image-20210526221213352.png)

# API

> 代码中使用Kafka

## Producer API

### 消息发送流程

- 消息提交到线程共享变量RecordAccumulator（相当于缓冲队列），Sender线程不断地从RecordAccumulator中拉取消息发送到Kafka broker。
- 消息流向：Producer->Interceptors->Serializer->Partitioner->RecordAccumulator->Sender->Topic
- 参数配置
  - `batch.size`，发送数据的批次大小
  - `linger.ms`，攒batch的最长等待时间

### 异步发送API

```java
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

@Slf4j
public class MyProducerWithPartitioner {
    public static void main(String[] args) {
        // 创建Kafka配置信息
        Properties conf = new Properties();
        conf.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka1:9092;kafka2:9093;kafka3:9094");
        conf.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        conf.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        // 添加自定义分区器
        conf.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, "com.equator.kafkalearning.partitioner.MyPartitioner");
        KafkaProducer<String, String> producer = new KafkaProducer<>(conf);
        for (int i = 0; i < 8; i++) {
            producer.send(new ProducerRecord<>("mytopic", "MyProducerWithPartitionerMsg" + i), (recordMetadata, e) -> {
                log.info("recordMetadata: partition: {}, offset: {}", recordMetadata.partition(), recordMetadata.offset(), e);
            });
        }
        producer.close();
    }
}
```

### 同步发送API

- 设置一个分区，使用同步发送可以保证全局有序，但是意义不大
- 同步发送依赖于Future

```java
public class MySyncProducer {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        // 创建Kafka配置信息
        Properties conf = new Properties();
        conf.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka1:9092;kafka2:9093;kafka3:9094");
        conf.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        conf.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        KafkaProducer<String, String> producer = new KafkaProducer<>(conf);
        for (int i = 0; i < 8; i++) {
            Future<RecordMetadata> future = producer.send(new ProducerRecord<>("mytopic", "MyProducerWithCallbackMsg" + i));
            RecordMetadata recordMetadata = future.get();
            log.info("recordMetadata: partition: {}, offset: {}", recordMetadata.partition(), recordMetadata.offset());
        }
        producer.close();
    }
}
```

## Consumer API

### 自动提交offset

### 手动提交offset

### 自定义存储offset

## 自定义Interceptor

### 拦截器原理

### 拦截器案例