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

- 对外的输出操作都需要使用Sink完成，`stream.addSink(new SinkFunction(xxx))`，Flink提供了一些连接器，其余的需要用户自定义
- Kafka等消息队列可以作为source来源或者sink的目的地，HDFS、Redis等一般只作为sink目的地。

### Kafka

- 使用Kafka作为数据管道的两端，Flink进行ETL操作

### Redis

### ES

### JDBC

- 继承RichSinkFunction

## Flink数据类型

- Flink使用类型信息的概念来表示数据类型，为每个数据类型生成特定的序列化器、反序列化器以及比较器。
- Flink具有类型提取系统，分析函数的输入和返回类型，以自动获取类型信息。但是再lambda函数或者泛型类型场景下，需要程序显式地提供类型信息。
- 具体类型
  - Java、Scala的基础类型以及其包装类型
  - Java、Scala的元组类型Tuple（最大25元组）
  - Scala样例类（Scala Classes）、Java简单对象（POJO，需要有空参构造方法以及setter、getter方法）

## UDF函数类

### 函数类

- Flink暴露了所有UDF函数的接口（实现方式为接口或者抽象类），如MapFunction、FilterFunction。

### 匿名函数

- lambda表达式

### 富函数

- DataStream API提供的函数类接口，所有的Flink的函数类都有其Rich版本。其可以获取运行环境的上下文（`getRuntimeContext`，获取子任务编号、上下文、状态等信息），并拥有一些生命周期方法（`open`、`close`），可以实现更加复杂的功能。如RichMapFunction、RichFilterFunction。

## 数据重分区操作

- forward，传播到下一个分区
- keyBy，哈希重分区
- broadcast，广播到所有下游
- shuffle，随机传播到下游
- reblance，轮询传播
- rescale，分组轮询
- global，将全部数据汇总到下游第一个分区
- partitionCustom，自定义重分区分区器

# 窗口API

## 基本概念

> 窗口（window）就是将无限流切割为有限流的一种方式，其将无限流数据分发到有限大小的桶（bucket）中进行分析。

## 窗口的类型

### 时间窗口（Time Window）

> 按照时间开窗

#### 滚动时间窗口（Tumbling）

- 将数据依据固定的窗口长度进行切分，时间对齐，窗口长度（`window_size`）固定，没有重叠。

#### 滑动时间窗口（Sliding）

- 滚动窗口的广义形式，由固定的窗口长度（`window_size`）和滑动间隔（`window_slide`）组成，可以有重叠（一条数据最多属于`window_size/window_slide`个窗口）
-  可以通过偏移量控制窗口起始位置。

#### 会话窗口

- 一段时间`timeout`没有接收到新数据就会生成新的窗口，时间不对齐

### 计数窗口（Count Window）

> 按照数据条数开窗

#### 滚动计数窗口

#### 滑动计数窗口

## 窗口分配器

- 使用window方法定义一个窗口，基于这个window去做一些聚合操作。或者使用timeWindow或者countWindow方法直接定义时间窗口与计数窗口。
- 开窗的前提是处理keyedStream，否则使用windowAll方法，需要将所有数据发送到下游同一个算子，类似于global的传播方式。

## 窗口增量聚合

> 每条数据到来就进行计算，保持一个简单的状态，如ReduceFunction，AggregationFunction。

- ReduceFunction即reduce聚合
- AggregationFunction<IN,ACC,OUT>，ACC表示累加器

## 窗口全窗口聚合

> 先把窗口所有的数据收集起来再处理，计算时遍历所有数据处理，如ProcessFunction、WindowFunction。 统计平均数、中位数等场景下需要用到。更加灵活，可操作性更强。

- WindowFunction<IN,OUT,KEY,W>

## 其它可选API

# 时间语义

- Event Time：事件创建的时间
- Ingestion Time：数据进入Flink的时间
- Processing Time：执行操作算子的本地系统时间，与机器相关

![image-20210627205306914](image-20210627205306914.png)

- 一般来说，EventTime更为重要，其代表了事件的实际发生时间，可以从日志数据时间戳中提取。 （EventTime使用更大的时间延迟来换取相对更加准确的计算结果）
- 时间语义的设置在环境中进行设置

# WaterMark

## 乱序数据带来的问题

- 当Flink以EventTime模式处理数据时，其根据数据的时间戳来处理基于时间的算子，由于网络、分布式等原因，会导致乱序数据的产生。

## WaterMark基本原理

> 由于Flink延迟较低，迟到数据的延迟也不高，数据比较集中

- 可以这样处理乱序事件：窗口应该关闭的时候，不立即触发窗口的关闭而是等待一段事件，等迟到的数据来了之后关闭，一般结合window使用。WaterMark让程序自己平衡延迟和结果正确性，它的设置需要一定的经验。
- WaterMark是一条特殊的带有时间戳的数据记录，时间戳必须单调递增以确保任务的事件时间时钟在向前推进而不是后退。

## WaterMark在任务间的传递

- WaterMark是一条特殊的数据，从上游传递到下游，采取广播的方式。
- 算子作为下游接收WaterMark时，保留每个上游任务最新的的WaterMark即分区水位线，算子选取做小的WM作为自己的事件时钟。

## WaterMark的使用

- 基本流程：环境中设置时间语义，提取数据的时间戳，生成WaterMark。`assignTimestampAndWatermarks`方法，`BoundedOutOfOrdernessTimestampExtractor`时间戳抽取类。`AscendingTimestampExtractor`用来处理正常排序的升序数据。
- WaterMark可以间断性生成（WM生成很多），周期性生成（适合数据量大的情况）

## 设定原则

- 经验值
- WM设置延迟时间太长，结果产出可能很慢，解决方法是到达水位线前输出一个近似的结果。VM设置延迟时间太短，可能收到错误的结果，可以通过Flink的迟到数据处理机制纠正结果。

# 状态

- 由一个任务维护，并且用来计算某个结果的所有数据，都属于这个任务的状态。可以认为是一个本地变量，可以被任务的业务逻辑访问。
- Flink会进行状态管理，保证状态一致性，故障处理以及高效存储访问。
- 可以在富函数类的close生命周期方法中清理状态资源。

## 算子状态

> Operator State，算子状态的作用范围限定为算子任务

- 算子状态是对于同一个子任务共享的，不能由相同或者不同算子的另一个子任务访问。

### 数据结构

- 列表状态 List State
- 联合列表状态 Union List State
- 广播状态 Broadcast State

## 键控状态

> Keyed State，根据输入数据流中定义的键key来维护和访问

- 键控状态根据数据流中定义的键来维护和访问的。Flink为每个key维护一个状态实例，并将具有相同键的所有数据都分到同一个算子任务中，该任务维护和处理这个key对应的状态。
- 当任务处理一条数据时，其自动将状态的访问范围限定为当前数据的key。

### 数据结构

- Value State
- List State
- Map State
- Reducing State & Aggregation State

## 状态后端

- 状态的存储，访问以及维护由一个可插入的组件决定，该组件就是状态后端（State Backend）。其主要负责：本地状态管理，将检查点（CheckPoint）状态写入远程存储。

### 类型

- MemoryStateBackend：内存级别的状态后端，状态保存在TaskManager的JVM堆上，检查点状态存储在JobManager的JVM堆上。快速但是不稳定。
- FsStateBacked：将检查点写入远程持久的文件系统（HDFS）上，本地存储仍然保存在本地。

- RocksDBStateBackend：将所有状态序列化后写入本地RocksDB中存储。（适合需要消耗大量内存的任务）