# 流处理API

## Environment

- **createExecutionEnvironment**，返回本地执行环境，需要在调用时指定默认的并行度。

- **createRemoteEnvironment**，返回远程执行环境，需要指定JobManager的IP以及端口号，并指定要在集群种运行的Jar包。
- 以上两种方法不太通用，可以使用**getExecutionEnvironment**，根据提交任务的方式返回本地的或者集群的运行环境，为最常用的执行环境创建方式。

```java
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
或者
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
```

## Source

### 从集合中读取数据

### 从文件中读取数据

### 从消息队列读取数据（Kafka）

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

Properties conf = new Properties();
conf.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka1:9092;kafka2:9093;kafka3:9094");

DataStreamSource<String> dataStreamSource = env.addSource(new FlinkKafkaConsumer<>("sensor_topic", new SimpleStringSchema(), conf));

dataStreamSource.print("sensor");

env.execute();
```

### 自定义消息源

- 实现自定义SourceFunction

```java
public class SensorDataSource implements SourceFunction<SensorReading> {

    /**
     * 标记位控制数据的产生
     */
    private boolean isRunning = true;

    @Override
    public void run(SourceContext<SensorReading> sourceContext) throws Exception {
        Random random = new Random();

        int sensorNum = 10;
        // 随机生成初始化温度
        Map<String, Double> temperatureMap = new HashMap<>(sensorNum);
        for (int i = 0; i < sensorNum; i++) {
            // 服从正态分布的温度
            temperatureMap.put("sensor_" + (i + 1), 60 + random.nextGaussian() * 20);
        }
        // 在循环中源源不断地生成数据
        while (isRunning) {
            for (String sensorId : temperatureMap.keySet()) {
                // 在原温度基础上随机波动
                Double temperature = temperatureMap.get(sensorId) + random.nextGaussian();
                temperatureMap.put(sensorId, temperature);
                sourceContext.collect(new SensorReading(sensorId, System.currentTimeMillis(), temperature));
            }
            // 控制输出频率
            Thread.sleep(2000);
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
    }
}
```

- 使用数据

```java
public class SourceFunctionTest {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // 自定义SourceFunction
        DataStreamSource<SensorReading> dataStreamSource = env.addSource(new SensorDataSource());

        dataStreamSource.print("sensor");

        env.execute();
    }
}
```

## Transform

### 基本转换操作

- map，一对一转换
- flatMap，一对一或者一对多转换
- filter，过滤
- keyBy，分组：DataStream->KeyedStream，逻辑地将一个流拆分为不相交的分区，每个分区包含具有相同key的元素，在内部以hash的方式实现。

### 滚动聚合

### reduce聚合

### 分流

### connect合流

### Union合流

## Sink

### Kafka

### Redis

### ES

### JDBC

## Flink数据类型

## UDF函数类

## 数据重分区操作

# 窗口API

