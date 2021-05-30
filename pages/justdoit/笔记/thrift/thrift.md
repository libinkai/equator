# 架构

## 架构图

- ![avatar](架构.png)

## Code generated

- constants.py: 包含声明的所有常量。
- ttypes.py: 声明的struct，实现了具体的序列化和反序列化。
- SERVICE_NAME.py: 对应service的描述文件，包含了：
  - Iface: service接口定义
  - Client: client的rpc调用桩


## Server

- Server创建Transport，输入、输出的Protocol，以及响应service的handler，监听到client的请求然后委托给processor处理。TServer是基类，构造函数的参数包括：
  1. processor, serverTransport
  2. processor, serverTransport, transportFactory, protocolFactory
  3. processor, serverTransport, inputTransportFactory, outputTransportFactory, inputProtocolFactory, outputProtocolFactory 
- TServer内部实际上需要3所列的参数，1和2参数会导致对应的参数使用默认值。
- TServer的子类包括：TSimpleServer, TThreadedServer, TThreadPoolServer, TForkingServer, THttpServer, TNonblockingServer, TProcessPoolServer。
- TServer的serve方法用于开始服务，接收client的请求。

### TSimpleServer 

- 单线程服务器端使用标准的阻塞式 I/O

### TThreadPoolServer 

- 多线程服务器端使用标准的阻塞式 I/O

### TNonblockingServer 

- 多线程服务器端使用非阻塞式 I/O


## Processor

- Processor对stream读写抽象，最终会调用用户编写的handler已响应对应的service。具体的Processor由compiler生成，用户需要实现service的实现类。


## Protocol

- Protocol用于对数据格式抽象，在rpc调用时序列化请求和响应。
- TProtocol的实现包括：TJSONProtocol，TSimpleJSONProtocol，TBinaryProtocol，TBinaryPotocolAccelerated，TCompactProtocol。
- Thrift 可以让用户选择客户端与服务端之间传输通信协议的类别，在传输协议上总体划分为文本 (text) 和二进制 (binary) 传输协议，为节约带宽，提高传输效率，一般情况下使用二进制类型的传输协议为多数，有时还会使用基于文本类型的协议

### TBinaryProtocol 

- 二进制编码格式进行数据传输

###  TCompactProtocol 

- 高效率的、密集的二进制编码格式进行数据传输

### TJSONProtocol 

- 使用 JSON 的数据编码协议进行数据传输

### TSimpleJSONProtocol 

-  只提供 JSON 只写的协议，适用于通过脚本语言解析

## Transport

- Transport网络读写（socket，http等）抽象，用于和其他thrift组件解耦。
- Transport的接口包括：open, close, read, write, flush, isOpen, readAll。
- Server端需要ServerTransport（对监听socket的一种抽象），用于接收客户端连接，接口包括：listen, accept, close。
- python中Transport的实现包括：TSocket, THttpServer, TSSLSocket, TTwisted, TZlibTransport，都是对某种协议或框架的实现。还有两个装饰器，用于为已有的Transport添加功能，TBufferedTransport（增加缓冲）和TFramedTransport（添加帧）。
- 在创建server时，传入的时Tranport的工厂，这些Factory包括：TTransportFactoryBase（没有任何修饰，直接返回），TBufferedTransportFactory（返回带缓冲的Transport）和TFramedTransportFactory（返回帧定位的Transport）

### TSocket 

- 使用阻塞式 I/O 进行传输，是最常见的模式

### TFramedTransport 

- 使用非阻塞方式，按块的大小进行传输，类似于 Java 中的 NIO

### TNonblockingTransport 

- 使用非阻塞方式，用于构建异步客户端


# 数据结构

## 基本类型

> thrift不支持无符号整形，因为很多目标语言不存在无符号整形（比如java）

- bool: 布尔类型，占一个字节
- byte: 有符号字节
- i16：16位有符号整型
- i32：32位有符号整型
- i64：64位有符号整型
- double：64位浮点数
- string：未知编码或者二进制的字符串

## 容器类型

> 容器中的元素类型可以是除service以外的任何合法的thrift类型，包括结构体和异常类型

- List\<t1\>：一系列t1类型的元素组成的有序列表，元素可以重复
- Set\<t1\>：一些t1类型的元素组成的无序集合，元素唯一不重复
- Map<t1,t2>：key/value对，key唯一

## 结构体与异常

- Thrift结构体在概念上同c语言的结构体类似，在面向对象语言中，thrift结构体将被转化为类

- 异常在语法和功能上类似于结构体，只是异常使用关键字exception而不是struct关键字来声明。但它在语义上不同于结构体—当定义一个RPC服务时，开发者可能需要声明一个远程方法抛出一个异常

- 结构体

  ```
  struct Tweet {
  1: required i32 userId;                  // a
  2: required string userName;             // b
  3: required string text;
  4: optional Location loc;                // c
  16: optional string language = "english" // d
  }
   
  struct Location {                            // e
  1: required double latitude;
  2: required double longitude;
  }
  
  a：每一个域都有一个唯一的正整数标识符
  b：每个域可以标识为required或者optional（也可以不注明）
  c：结构体可以包含其他结构体
  d：域可以有缺省值
  e：一个thrift中可以定义多个结构体，并存在引用关系
  ```

- 规范的struct定义中的每个域均会使用required或者optional关键字进行标识。如果required标识的域没有赋值，thrift将给予提示。如果optional标识的域没有赋值，该域将不会被序列化传输。如果某个optional标识域有缺省值而用户没有重新赋值，则该域的值一直为缺省值

## 服务

- Thrift中服务定义的方式和语法等同于面向对象语言中定义接口

- Thrift编译器会产生实现接口的client和server桩（桩代码即占位代码，粘合代码，残存代码, 指满足形式要求但没有实现实际功能的占坑/代理代码）

- IDL语法

  ```
  //“Twitter”与“{”之间需要有空格！！！
  service Twitter {
  // 方法定义方式类似于C语言中的方式，它有一个返回值，一系列参数和可选的异常
  // 列表. 注意，参数列表和异常列表定义方式与结构体中域定义方式一致.
  void ping();                                    // a
  bool postTweet(1:Tweet tweet);                  // b
  TweetSearchResult searchTweets(1:string query); // c
  // ”oneway”标识符表示client发出请求后不必等待回复（非阻塞）直接进行下面的操作，”oneway”方法的返回值必须是void
  oneway void zip();                          	// d
  }
  
  a：函数定义可以使用逗号或分号标识结束
  b：参数可以是基本类型或者结构体，参数只能是只读的（const），不可以作为返回值
  c：返回值可以是基本类型或者结构体
  d：返回值可以是void
  注意，函数中参数列表的定义方式与struct完全一样；Service支持继承，一个service可使用extends关键字继承另一个service。
  ```

# 语法

> Thrift 是对 IDL(Interface Definition Language) 描述性语言的一种具体实现

## 注释

> Thrift支持shell注释风格、C/C++语言中的单行或多行注释风格

```
# This is a valid comment.
 
/*
 
* This is a multi-line comment.
 
* Just like in C.
 
*/
 
// C++/Java style single-line comments work just as well.
```

## 命名空间

> Thrift中的命名空间同C++中的namespace和java中的package类似，它们均提供了一种组织（隔离）代码的方式。
>
> 因为每种语言均有自己的命名空间定义方式（如python中有module），thrift允许开发者针对特定语言定义namespace

```
namespace cpp com.example.project  // a 
namespace java com.example.project // b
```

## 文件包含

> Thrift允许文件包含，需要使用thrift文件名作为前缀访问被包含的对象

```
include "tweet.thrift" // 其它地方有tweet.thrift这样的一个文件（thrift文件名需要双引号包含，末尾没有逗号或者分号）
 
...
 
struct TweetSearchResult {
 
1: list<tweet.Tweet> tweets; // 使用thrift文件名作为前缀访问被包含的对象
 
}
```

## 常量

> Thrift允许用户定义常量，复杂的类型和结构体可以使用JSON形式表示

```
const i32 INT_CONST = 1234;    // a
 
const map<string,string> MAP_CONST = {"hello": "world", "goodnight": "moon"}
```

# 协议

