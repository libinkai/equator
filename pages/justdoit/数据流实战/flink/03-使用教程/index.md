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

```java
public class BaseTransformation {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // 加上这句代码可以实现顺序输出
        env.setParallelism(1);

        DataStreamSource<String> fileDataStreamSource = env.readTextFile("src/main/resources/data/sensordata.txt");

        DataStream<Integer> mapStream = fileDataStreamSource.map(String::length);


        DataStream<String> flatMapStream = fileDataStreamSource.flatMap(new FlatMapFunction<String, String>() {
            @Override
            public void flatMap(String line, Collector<String> collector) throws Exception {
                String[] fields = line.split(",");
                for (String field : fields) {
                    collector.collect(field);
                }
            }
        });

        SingleOutputStreamOperator<String> filterStream = fileDataStreamSource.filter((line) -> line.startsWith("sensor_1"));

        mapStream.print("map");
        flatMapStream.print("flatMap");
        filterStream.print("filter");

        env.execute();
    }
}
```

- keyBy，分组：DataStream->KeyedStream，逻辑地将一个流拆分为不相交的分区，每个分区包含具有相同key的元素，在内部以hash的方式实现。

### 滚动聚合

> 对KeyedStreamd的每一个支流做聚合

- sum
- min，保留一个字段；minBy，保留全部字段
- max；maxBy

### reduce聚合

> KeyedStreamd->DataStream，一个分组数据流的聚合操作，合并当前的元素和上次聚合的结果，产生一个新的结果。（更加一般化的聚合操作）

```java
public class ReduceAggregationTest {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // 加上这句代码可以实现顺序输出
        env.setParallelism(1);

        DataStreamSource<String> fileDataStreamSource = env.readTextFile("src/main/resources/data/sensordata.txt");

        // String数据包装为SensorReading
        DataStream<SensorReading> dataStream = fileDataStreamSource.map((line) -> {
            String[] fields = line.split(",");
            return new SensorReading(fields[0], Long.valueOf(fields[1]), Double.valueOf(fields[2]));
        });

        KeyedStream<SensorReading, Tuple> keyedStream = dataStream.keyBy("id");

        // reduce聚合，取最大的温度值以及最新的时间戳
        SingleOutputStreamOperator<SensorReading> reduceStream = keyedStream.reduce(new ReduceFunction<SensorReading>() {
            @Override
            public SensorReading reduce(SensorReading oldVal, SensorReading newVal) throws Exception {
                return new SensorReading(oldVal.getId(), newVal.getTimestamp(), Math.max(oldVal.getTemperature(), newVal.getTemperature()));
            }
        });

        reduceStream.print();

        env.execute();
    }
}
```

### 分流

> Split：DataStream->SplitStream，根据某些特征把一个DataStream拆分为多个或者多个DataStream。
>
> Select：SplitStream->DataStream，从一个SplitStream中获取一个或者多个DataStream。
>
> Split与Select两个操作是分流的一个流程

### connect合流

> DataStream，DataStream->ConnectStreams，连接两个保持他们类型的数据流，两个数据流被Connect之后，内部的数据和形式不变，两条流相互独立。需要通过CoMap或者CoFlatMap操作合并为真正的一条数据流。

### union合流

> DataStream->DataStream，连接多条数据类型一致的数据流

![数据流转换](./数据流转换.jpg)

## Sink

### Kafka

### Redis

### ES

### JDBC

## Flink数据类型

- Flink使用类型信息的概念来表示数据类型，为每个数据类型生成特定的序列化器、反序列化器以及比较器。
- Flink具有类型提取系统，分析函数的输入和返回类型，以自动获取类型信息。但是再lambda函数或者泛型类型场景下，需要程序显式地提供类型信息。
- 具体类型
  - Java、Scala的基础类型以及其包装类型
  - Java、Scala的元组类型Tuple（最大25元组）
  - Scala样例类（Scala Classes）、Java简单对象（POJO，需要有空参构造方法以及setter、getter方法）

## UDF函数类

## 数据重分区操作

# 窗口API

