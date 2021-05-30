# Java异常

> 异常类型回答了什么被抛出，异常堆栈跟踪回答了在哪里被抛出，异常信息回答了为什么被抛出

- Error与Exception的顶级父类：`Throwable`，二者都可以被抛出，但是Error不需要显式捕获处理。

## Error

> 程序无法处理的系统错误，编译器不做检查

- `NoClassDefFoundError`，找不到class定义
  - 类依赖的class或者jar不存在
  - 类文件存在，但是存在不同的域中
  - 大小写问题（`javac`编译时无视大小写，可能是编译出来的class文件就与想要的不一样）
- `StackOverflowError`
- `OutOfMemoryError`

## Exception

> 程序可以处理的异常，捕获之后可能恢复。checked exception用来指示一种调用方能够直接处理的异常情况。而runtime exception则用来指示一种调用方本身无法处理或恢复的程序错误

- `RuntimeException`，不可预知的，程序应当自行避免，如数组越界、空指针异常，运行时异常可以在编译时被忽略
  - `NullPointerException`，空指针异常
  - `ClassCastException`，类型强转异常
  - `IllegalArgumentException`，传递非法参数异常
  - `IndexOutOfBoundsException`，越界异常
  - `NumberFormatException`，数字格式异常，String转Number
- `CheckedException`，可预知的，编译器校验的异常，必须编码上做好`try-catch`处理，如IO异常，这些异常在编译时不能被简单地忽略
  - `ClassNotFoundException`，找不到指定的类
  - `IOException`，IO操作异常

- 写代码过程中标红的那种，是TM的语法错误！

## 异常处理机制

1. 抛出异常：创建异常对象，交由运行时系统处理

2. 捕获异常：寻找合适的异常处理器处理异常，否则终止运行

3. 机制

   ```java
   try{
   
   } catch(Exception e){
   
   } finally{
   	// finally块中的语句会在catch语句return之前执行
   }
   ```

4. 原则
   1. 不要粗化异常
   2. 不要捕获自己不希望捕获的异常
   3. 不要生吞异常（捕获而不处理）
   4. 尽早抛出，延迟处理

## 自定义异常处理框架

- 定义一个顶级异常`AppException`继承自`RuntimeException`
- 定义不同的业务子异常，继承自`AppException`
- 子异常转义为顶级异常向前端抛出

## 性能

> `try catch`语句比`if`语句慢

- `try catch`影响JVM的优化
- 异常对象实例需要保存栈快照等信息

# IO机制

## BIO

> java.io或者java.net下的类

- InputStream、OutputStream
- Reader、Writer

## NIO

> 构建多路复用的、同步非阻塞IO操作

### Channels

- FileChannel，避免了两次用户态与内核态的切换
- DatagramChannel
- SocketChannel
- ServerSocketChannel

### Buffers

- Byte、Char、Double、Float、Int、Long、Short、MappedByteBuffer（内存映射文件）

### Selectors

#### IO多路复用

- select单个进程能够打开的最大连接数由（机器字长*32）决定，极其有限；FD剧增后由于其线性遍历，性能会下降；通过内核拷贝将消息传递到用户空间
- poll，链表实现，没有最大连接数限制；FD剧增后由于其线性遍历，性能会下降；通过内核拷贝将消息传递到用户空间
- epoll，有限的最大连接数，但是上界很高；基于回调实现，活跃的socket才主动callback，性能较好。通过内核和用户空间共享一块内存来实现，性能较高

## AIO

> Asynchronous IO，基于事件与回调机制

### 加工处理结果

- 基于回调：实现CompletionHandler接口，调用时触发回调函数
- 返回Future：通过isDone查看是否准备好，通过get获取处理结果

# 集合框架

- 客户化排序优先级高于自然排序

## HashMap

> JDK8以前：数组+链表，JDK8以后：数据+链表+红黑树（TREEIFY_THRESHOLD）

- JDK8以前，数组元素为`entry`，JDK8以后，数组元素为`Node`
- `TREEIFY_THRESHOLD`树化阈值，值为8；`UNTREEIFY_THRESHOLD`逆树化阈值，值为6
- `允许插入NULL`

### 初始化

| initialCapacity | HashMap 初始容量                                             |
| --------------- | ------------------------------------------------------------ |
| loadFactor      | 负载因子                                                     |
| threshold       | 当前 HashMap 所能容纳键值对数量的最大值，超过这个值，则需扩容，threshold = capacity * loadFactor |

### put方法

1. 如果`hashmap`没有被初始化过，则初始化，`resize()`具有初始化与扩容的功能
2. 对Key求hash值，计算下标
3. 如果没有哈希碰撞，直接放入桶中
4. 如果碰撞了，以链表方式链接到后面
5. 如果链表长度超过阈值8，把链表转化为红黑树
6. 如果树节点少于阈值6，将红黑树转换为链表
7. 如果节点已经存在（key相等），替换旧值
8. 如果桶满了（容量（默认16）*加载因子（默认0.75）），就需要resize（扩容2倍后重排）

### get方法

1. 计算哈希值，获取数组中对应的第一个元素（链表头或者树根）~定位桶`(n - 1)& hash`
2. 如果第一个元素不是目标，按照树或者链表的方式获取节点
3. 返回节点

### hash方法

1. `h=hashCode`，获取`int`类型的`hashCode`（`hashCode`范围过大，需要映射）
2. `hash=h^(h>>>16)`，将高16位与低16位混合，让高位数据与低位数据进行异或，以此加大低位信息的随机性，变相的让高位数据参与到计算中
3. `(n-1)&hash` 取数组大小的位（等效于取模），`HashMap`数组大小都是`2^n`
4. 需要将高位数据移位到低位进行异或运算，因为有些数据计算出的哈希值差异主要在高位，而 HashMap 里的哈希寻址是忽略容量以上的高位的，那么这种处理就可以有效避免类似情况下的哈希碰撞。

### resize方法

> HashMap 按当前桶数组长度的2倍进行扩容，阈值也变为原来的2倍

1. 创建新数组
2. 重新散列 `rehashing`

### 减少碰撞

1. 扰动函数：促使元素位置分布均匀，减少碰撞几率
2. 使用final对象，并采用合适的equals与`hashCode`方法

### 并发

- 包装成为线程安全的`synchronizedMap`，基于mutex

  ```
  Map map = new HashMap();
  Map safeMap = Collections.synchronizedMap(map);
  ```

## HashTable

- 线程安全，锁住整个对象
- **不允许插入NULL**

## ConcurrentHashMap

> 锁的细粒度化

- 早期：通过分段锁Segment实现，数组+链表（默认16个段）
- JDK8：CAS+synchronized使锁更细化，数组+链表+红黑树，只锁住数组的每个元素（链表的头部或者树根）
- **不允许插入NULL**
- Hashtable和ConcurrentHashMap是线程安全的，在设计时，默认使用场景是多线程下。如果允许value为空，则用户调用get(key)方法后返回null不能判断是否存在对应的key-null键值对，需要额外使用containsKey来进行判断，在多线程场景下需要用户手动进行加锁。为了减少用户使用的负担，以及避免由于误使用带来严重的后果，同时也考虑到key/value为空也没有太大的意义，所以就禁止key/value为空

### put方法

1. 判断Node数组是否初始化，没有则进行初始化
2. 通过hash定位数组的索引坐标，检查是否有Node节点，如果没有则CAS添加（头节点），添加失败则进入下一次循环
3. 如果检查到内部正在扩容，则辅助其扩容
4. 如果头节点不等于NULL，则使用synchronized锁住头节点（包括链表头部以及树根），进行链表或者树的添加节点存在
5. 判断链表长度，判断是否进行树化

### size方法

- 通过重试机制（RETRIES_BEFORE_LOCK指定重试次数为2）来试图获得可靠值。如果判断到没有变化则直接返回（通过对比Segment.modCount），否则获取锁进行操作

# JUC

> java.util.concurrent，提供了并发编程的解决方案

## CAS

> java.util.concurrent.atomic包的基础

## AQS

> java.util.concurrent.locks包以及Semophore、ReentrantLock等类的基础

## 分类

### 线程执行器

> executor

### 锁

> locks

### 原子变量类

> atomic

### 并发工具类

> tools

- 闭锁 CountDownLatch：让主线程等待一组事件发生之后继续执行；事件指的是CountDownLatch 里面的countDown方法
- 栅栏 CyclicBarrier：阻塞当前线程，等待其它线程；
  - 等待其它线程，且会阻塞自己当前线程，所有线程必须同时到达栅栏位置之后才可以继续执行
  - 所有线程到达栅栏之后，可以触发另外一个预设的线程
- 信号量 Semaphore：控制某个资源可被同时访问的线程个数
- 交换器 Exchanger：两个线程到达同步点之后，相互交换数据，需要交换的数据作为参数传入`Exchanger的exchange方法`

### 阻塞队列

> collections

- BlockingQueue：提供可阻塞的入队与出队操作
  - add 添加失败则抛出异常
  - offer 添加失败则返回NULL，poll取出元素，可以超时
  - put 添加失败则自旋，take 阻塞取出元素

- ArrayBlockingQueue，数组实现的有界阻塞队列
- LinkedBlockingQueue，链表实现的有界/无界（默认大小Integer.MAX_VALUE）阻塞队列
- PriorityBlockingQueue，一个支持优先级排序的无界阻塞队列
- DealyQueue支持延时获取的优先级阻塞队列，元素必须实现delay接口
- SynchronousQueue，不储存元素
- LinkedTransferQueue：链表实现的无界阻塞队列（SynchronousQueue+LinkedBlockingQueue）
- LinkedBlockingDeque：链表实现的双向无界阻塞队列