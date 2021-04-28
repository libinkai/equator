# 操作系统概览

## OS演进

- 无操作系统
- 批处理系统
- 分时系统

## 多道程序设计

> 多道程序设计使得操作系统可以一次处理多个任务

- 在计算机内存中同时存放多个内存
- 多道程序在计算机管理程序之下相互穿插运行

## 操作系统五大功能

> 作业的调度属于高级调度，进程的调度属于低级调度。作业就是从外存放到内存的一个过程，它可以包含一个或多进程

- 进程管理
- 作业管理
- 存储管理
- 文件管理
- 设备管理

## 操作系统的特性

- 并发性（并行与并发）
- 共享性（操作系统中的资源可供多个并发程序共同使用，分为互斥共享如打印机，以及非互斥共享如硬盘）
- 虚拟性（将一个物理实体转化为若干个逻辑实体，主要有**时分复用**，如虚拟处理器技术、虚拟设备技术；**空分复用**，如虚拟磁盘技术即逻辑分盘、虚拟内存技术）
- 异步性（在多道程序环境下，多个进程并发执行）

# 进程管理-进程实体

## 主存中的进程实体

> 进程控制块PCB是用于描述与控制程序运行的通用数据结构，PCB是常驻内存的，存放在系统专门开辟的PCB空间区域内

- 标识符：进程的唯一标识符
- 状态：进程的运行状态
- 优先级：程序调度优先级
- 程序计数器：进程即将被执行的下一条指令的地址
- 内存指针：程序代码、进程数据相关指针（可能有多个）
- 上下文指针：进程执行时处理器储存的数据
- IO状态信息：被进程IO操作所占用的文件列表
- 记账信息：进程使用处理器时长、时钟数总和

## 进程与线程

> 进程Process、线程Thread

- 进程是系统进行资源分配与调度的基本单位，线程是操作系统进行调度的最小单位
- 进程中的线程共享进程的资源

# 进程管理-进程状态模型

- 创建状态：已分配PCB，但未插入就绪队列
- 就绪状态：其它资源都准备好，只差CPU即可运行（通常在就绪队列中排队）
- 执行状态：进行获取CPU，其程序正在执行（单处理机中，在某个时刻只能有一个进程处于执行状态）
- 阻塞状态：进程由于某种原因（如其它资源没有就绪）而放弃CPU的状态，（通常在阻塞队列中排队）
- 终止状态：进程执行完毕

# 进程管理-进程同步

## 为什么需要进程间同步

- 生产者消费者问题（数据不一致，根本原因是生产者或者消费者的一系列存在不是原子性的）
- 哲学家进餐问题（死锁）

## 进程同步的原则

- 空闲让进：资源无占用，运行使用
- 忙则等待：资源被占用，请求进程等待
- 有限等待：
- 让权等待：等待时让出CPU

## 进程同步的方法

- 消息队列
- 共享储存
- 信号量

## 线程同步

> 线程共享进程的资源，进程内多线程需要同步

- 互斥锁
- 读写锁
- 自旋锁
- 条件变量

# 进程管理-Linux进程管理

## Linux进程的相关概念

### 进程的类型

- 前台进程（具有终端，可以和用户交互的进程）
- 后台进程（基本不与用户交互，没有占用终端，优先级一般比前台进程低，执行命令以`&`结尾）
- 守护进程（特殊的后台进程，一般在系统引导时启动，一直到系统关闭时终止，如`httpd、mysqld、sshd、crond`）

### 进程的标记

- 进程ID：`PID`，父子进程关系查看：`pstree`
  - ID为0的进程为`idle`进程，时系统创建的第一个进程
  - ID为1的进程为`init`进程，时0号进程的子进程，完成系统的初始化
- 进程的状态标记：进程状态查看命令`ps -aux`
  - R，Running，运行状态
  - S，Interruptible，睡眠状态
  - D，Uninterruptible，IO等待的睡眠状态
  - T，Stopped，暂停状态
  - Z，Dead或者Zombie，终止状态或者僵尸进程

## Linux相关命令

> `-`表示参数，`--`表示子命令

### ps

- -u 指定用户进程
- -a 显示所有进程
- -e 显示所有进程
- -f 显示UID，PPIP，C与STIME栏位
- --forest 查看进程树
- --sort 排序显示

### top

### kill

- -9 无条件停止

### C++编程

```
make xxx.cpp

time ./xxx  显示程序运行耗时
```

# 作业管理-进程调度

## 进程调度

> 进程调度指的是计算机通过决策决定哪个就绪进程可以获取CPU使用权

- 就绪队列的排队机制：将就绪进程按照一定的方式排成队列，以便调度程序可以最快地找到就绪进程
- 选择运行进程的委派机制：调度程序以一定的策略选择就绪进程，将CPU资源分配给它
- 新老进程的上下文切换机制：保存当前进程的上下文信息，装入被委派执行执行进程的运行上下文（抢占式调度与非抢占式调度）

## 进程调度算法

- 先来先服务调度
- 短进程优先调度
- 高优先级优先调度
- 时间片轮转调度

# 作业管理-死锁

## 死锁的必要条件

> 只要一个必要条件不满足即可破坏死锁

1. 互斥条件（进程对资源的使用是排他性的，某资源只能由一个进程使用，其它进程需要使用只能等待）
2. 请求保持条件（进程至少保持一个资源，又提出新的资源请求；新资源被占用，请求被阻塞；被阻塞的进程不释放自己保持的资源）
3. 不可剥夺条件（进程获得的资源在使用完毕之前无法剥夺，需要进程自己释放）
4. 环路等待条件（进程、资源环路等待链）

## 预防死锁的方法

> 互斥条件一般不可破坏

- 破坏**请求保持条件**，一次性请求所有资源

- 破坏**不可剥夺条件**，进程运行时资源可剥夺
- 破坏**环路等待条件**，资源线性排序，申请时必须按照需要递增申请

## 银行家算法

> 一个可操作著名的避免死锁的算法，以银行借贷分配策略为基础

- 可分配资源表
- 所需资源表
- 已分配资源表
- 还需分配资源表=所需资源表-已分配资源表

# 存储管理-内存分配与回收

## 内存分配过程

### 单一连续分配

- 将内存分为系统区与用户区，只适用于单任务系统

### 固定分区分配

- 将内存划分为固定大小的分区，每个分区只给一个进程使用

### 动态分区分配

- 数据结构
  - 空闲表数据结构
  - 空闲链数据结构（双向链表+节点需要记录可存储的容量）
- 分配算法
  - 首次适应算法
  - 循环适应算法（首次适应算法的改进，从上一次扫描点开始扫描而不是从头开始）
  - 最佳适应算法（空闲区链表按照容量大小升序排序）
  - 快速适应算法（多个空闲链，每个空闲链上的分区大小相同）

## 内存回收过程

- 回收区与空闲区接壤，合并
- 回收区与空闲区不接壤，创建新的节点加入道空闲链

# 存储管理-段页式存储管理

> 字块是相对于物理设备的概念，页面是相当于逻辑空间的概念

## 页式存储管理

- 特点
  - 将进程逻辑空间等分为若干个大小的页面
  - 相应的把物理内存空间划分为与页面等大的物理块
  - 以页面为单位把进程空间装进物理内存中分散的物理块
- 页面大小通常是512B~8K
- 会导致空间碎片
- 页表：记录将进程逻辑空间与物理空间的映射（页号|块号）
- 多级页表：解决页表过大问题
- 如果一段连续的逻辑分布在多个页面中，将大大降低执行效率

## 段式存储管理

- 特点
  - 将进程逻辑空间划分为若干段（非等分）
  - 段的长度由连续逻辑的长度决定

- 段表：记录将进程逻辑空间与物理空间的映射（段号|基址|段长）

## 段页式存储管理

- 分页可以有效提高内存利用率（虽然会导致页内碎片），分段可以更好的满足用户需求
- 原理
  - 先将逻辑空间按段式存储管理划分为若干段
  - 再把段内空间按页式储存管理等分为若干页
- 段页表（段号|段内页号|页内地址）

# 存储管理-虚拟内存

- 把程序使用内存划分、将部分暂时不使用的内存放置在辅存中

## 程序局部性原理

- CPU在访问存储器的时候，无论是存取指令还是存取数据，所访问的存储单元都趋于聚集在一个较小的连续区域
- 程序运行中，无需全部装入内存，如果访问页不在内存中，则发起缺页中断，进行页面置换

## 虚拟内存的置换算法

> 高速缓存与主存、主存与辅存的置换算法均为这些，可以说是置换算法的套路

- 先进先出 FIFO
- 最不经常使用算法 LFU
- 最近最少使用算法 LRU

# 存储管理-Linux存储管理

## Buddy内存管理算法（伙伴系统）

> 基于二进制特点，主要解决内存**外碎片**的问题，努力让内存分配与相邻内存合并能够快速执行（实际上是将内存外碎片问题转化为内存内碎片问题）

### 内存碎片

- 页内碎片：已经被分配出去的内存空间大于所需的内存空间，不能被利用的内存空间就是内部碎片
- 页外碎片：尚未分配出去，但是由于大小不合适无法分配给申请内存的进程的空闲块即页外碎片

### 算法原理

- 内存分配时，将每一块分配内存向上取整为2的幂大小，如申请`666k`，分配`1024k`
- 一片内存的伙伴是**相邻**的另一片等大的**连续**内存（伙伴是相互的）
- 申请时从小到大判断，分配时从大到小判断
- 回收时判断伙伴是否空闲，是则移出伙伴并合并（从小到大判断）

## Linux交换空间

- 交换空间Swap是磁盘的一个分区，在安装操作系统时配置
- Linux内存满的时候，会把一些内存交换到Swap空间
- 冷启动内存依赖
- 系统睡眠依赖
- 大进程内存依赖
- Swap空间与虚拟内存的区别：前者是操作系统的概念，后者是进程概念（角度不一样）

# 文件管理

## 文件的逻辑结构

### 逻辑结构的文件类型

- 有结构文件（主要有两部分：定长记录meta data和可变长记录data）
  - 文本文件
  - 文档
  - 媒体文件
- 无结构文件（流式文件，如`exe、dll、so`）
  - 二进制文件
  - 链接库

### 文件存储方式

- 顺序文件
  - 顺序文件指的是按顺序存放在存储介质中的文件
  - 顺序文件是所有逻辑文件中储存效率最高的
  - 可变长文件不适合顺序文件的储存
- 索引文件
  - 索引文件是为了解决可变长文件储存而发明的
  - 索引文件需要配合索引表实现储存操作

## 辅存的储存空间分配

### 连续分配

### 链接分配

> 链接分配可以将文件储存在离散的盘块中，需要额外的存储空间存储文件的盘块链接顺序

- 隐式链接：下一个链接指向储存在当前盘块中（随机访问效率低，可靠性不高）
- 显式链接：使用FAT（File Allocation Table）储存，不支持高效的直接存储（FAT表项过多），读取文件时需要把整个FAT加载进内存

### 索引分配（主流）

- 把文件所有盘块集中储存（索引），即每个文件拥有一个索引块，记录所有盘块信息
- 读取某个文件时，将文件索引读取进内存即可
- 支持直接访问盘块
- 储存大文件时有优势

### 存储空间管理

- 空闲表（序号|第一个空闲盘块号|空闲盘块数）
- 空闲链表（每个节点储存空闲盘块与空闲的数目）
- 位示图（盘块，磁道组成的二维表，通过布尔值标记是否）

## 目录管理

- 目录树（任何文件或者目录都有唯一的路径）

# 文件管理-Linux文件操作

## Linux目录

## Linux文件常用操作

## Linux文件类型

- 普通文件 `-`
- 目录文件 `d`
- 符号链接 `l`
- 设备文件 `b、c`
- 套接字 `s`
- FIFO `p`

# 文件管理-Linux的文件系统

## 概述

- FAT （File Allocation Table），使用一张表保存盘块信息
- NTFS（New Technology File System），Windows、Linux均可识别
- EXT2/3/4（Extended File System），Linux文件系统

## Ext文件系统

- 结构为一个`Boot Sector`（启动扇区），若干个`Block Group`（块组，储存数据的实际位置）

### Inode

- 文件类型
- 文件权限
- 文件物理地址
- 文件长度
- 文件连接计数
- 文件存取时间
- 文件状态
- 访问计数
- 链接指针
- 文件名不是储存在文件的Inode上面的，而是储存在目录的Inode上（为了列出目录文件时不需要加载文件的Inode）

### Boot Sector

### Block Group

- Super Block：保存整个文件系统的meta data
- 文件系统描述
- Inode bitmap：记录已分配和未分配的Inode
- Block bitmap：记录已分配和未分配的Block
- Inode Table：存放文件Inode的地方，每一个文件，目录都有一个Inode，即索引节点
- Data Block：存放文件内容，每个Block都有唯一的编号，文件的Block记录在文件的Inode上面

### 命令

- `df -T` 查看磁盘挂载信息
- `dump2fs device_name` 查看文件系统的Inode信息
- inode是文件的唯一标记而不是文件名

# 设备管理

## 广义的IO设备

- 以CPU的视角来看，向CPU输入数据的设备是输入设备，CPU输出数据的设备是输出设备

### 按使用特性分类

- 储存设备
- 交互IO设备

### 信息交换单位分类

- 块设备：磁盘、SD卡
- 字符设备：打印机、Shell终端

### 按共享属性分类

### 按IO速率分类

## IO设备的缓冲区

- 缓冲区可以减少IO次数
- 专用缓冲区只适用于特定的IO进程，对内存消耗大
- 操作系统划出可供多个进程使用的公共缓冲区，称之为缓冲池

## SPOOLing技术

- 关于慢速字符设备如何与计算机主机交换信息的一种技术
- 利用高速共享设备将低速的独享设备模拟为高速的共享设备，逻辑上为每一个用户分配了一台高速共享设备（即把同步调用低速设备改为异步调用）
- 进程将数据输出到一个存储空间（输出井），SPOOLing进程负责输出井与低速设备之间的调度

# 线程同步-互斥量

- 互斥量（互斥锁），即处于两态之一的变量，具有解锁和加锁的语义

- 通过互斥量确保每次只有一个线程进入临界区，保证资源访问的串行性

- 操作系统提供的互斥量`pthread_mutex_t`

  ```
  // 定义
  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
  // 加锁
  pthread_mutex_lock(&mutex);
  // 解锁
  pthread_mutex_unlock(&mutex);
  ```

# 线程同步-自旋锁

- 自旋锁也是一种多线程同步的变量

- 使用自旋锁的线程会反复检查锁变量是否可用，自旋锁不会让出CPU而是处于忙等待的状态

- 自旋锁避免了进程或者线程上下文切换的开销，但是不适合在单核CPU下使用

- 操作系统提供的自旋锁`pthread_spinlock_t`

  ```
  // 定义
  pthread_spinlock_t spin_lock;
  // 初始化
  pthread_spin_init(&spin_lock,0);
  // 加锁
  pthread_spin_lock(&spin_lock);
  // 解锁
  pthread_spin_unlock(&spin_lock);
  ```

# 线程同步-读写锁

- 符合临界资源多读少写的情况

- 读写锁是一种特殊的自旋锁，允许多个读者同时访问临界资源，而写者间、读者与写者之间互斥

- 操作系统提供的读写锁

  ```
  // 定义
  pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;
  // 加读锁
  pthread_rwlock_rdlock(&rwlock);
  // 解读锁
  pthread_rwlock_unlock(&rwlock);
  // 加写锁
  pthread_rwlock_wrlock(&rwlock);
  // 解写锁
  pthread_rwlock_unlock(&rwlock);
  ```

# 线程同步-条件变量

- 条件变量允许线程睡眠，直到满足某种条件

- 当满足条件时，可以向该线程发送信号，通知唤醒

- 配合互斥量，优雅解决生产者消费者问题

- 操作系统提供的条件变量`pthread_cond_t`

  ```
  // 定义条件变量与互斥量
  pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
  // 等待条件满足
  pthread_cond_wait(&cond,&mutex);
  // 等待被唤醒 
  pthread_cond_signal(&cond);
  ```

- 步骤
  - 加锁保护条件变量
  - 等待条件满足被唤醒
  - 访问临界资源
  - 通知

# 进程同步-创建进程

> fork系统调用

- fork创建的进程状态与父进程完全一样，创建之后系统为子进程分配新的资源
- fork一次调用，两次返回，分别返回子进程id与0，通过判断返回值可以进入两次条件分支

# 进程同步-共享内存

- 由于操作系统的管理，进程间的内存空间是相互独立的，进程是默认不能访问进程空间以外的内存的

- 可以通过共享内存实现进程间的通信，也是传输数据的最快方式

- 操作步骤

  - 申请共享内存
  - 连接到进程空间
  - 使用共享内存
  - 脱离进程空间与删除

- 实例（共享内存为提供同步机制，需要自己管理）

  ```
  #ifndef __COMMON_H__
  #define __COMMON_H__
  
  #define TEXT_LEN 2048
  
  // 共享内存的数据结构
  struct ShmEntry{
      // 是否可以读取共享内存，用于进程间同步
      bool can_read;
      // 共享内存信息
      char msg[2048]; 
  };
  
  #endif
  
  #include "common.h"
  
  #include <sys/shm.h>
  #include <stdlib.h>
  #include <unistd.h>
  #include <stdio.h>
  #include <string.h>
  
  #include <iostream>
  
  int main()
  {
      // 共享内存的结构体
      struct ShmEntry *entry;
  
      // 1. 申请共享内存
      int shmid = shmget((key_t)1111, sizeof(struct ShmEntry), 0666|IPC_CREAT);
      if (shmid == -1){
          std::cout << "Create share memory error!" << std::endl;
          return -1;
      }
  
      // 2. 连接到当前进程空间/使用共享内存
      entry = (ShmEntry*)shmat(shmid, 0, 0);
      entry->can_read = 0;
      while (true){
          if (entry->can_read == 1){
              std::cout << "Received message: " << entry->msg << std::endl;
              entry->can_read = 0;
          }else{
              std::cout << "Entry can not read. Sleep 1s." << std::endl;
              sleep(1);
          }
      }
      // 3. 脱离进程空间
      shmdt(entry);
  
      // 4. 删除共享内存 
      shmctl(shmid, IPC_RMID, 0);
  
      return 0;
  }
  
  #include "common.h"
  
  #include <sys/shm.h>
  #include <stdlib.h>
  #include <unistd.h>
  #include <stdio.h>
  #include <string.h>
  
  #include <iostream>
  
  int main()
  {
      struct ShmEntry *entry;
  
      // 1. 申请共享内存
      int shmid = shmget((key_t)1111, sizeof(struct ShmEntry), 0666|IPC_CREAT);
      if (shmid == -1){
          std::cout << "Create share memory error!" << std::endl;
          return -1;
      }
  
      // 2. 连接到当前进程空间/使用共享内存
      entry = (ShmEntry*)shmat(shmid, 0, 0);
      entry->can_read = 0;
      char buffer[TEXT_LEN];
      while (true){
          if (entry->can_read == 0){
              std::cout << "Input message>>> ";
              fgets(buffer, TEXT_LEN, stdin);
              strncpy(entry->msg, buffer, TEXT_LEN);
              std::cout << "Send message: " << entry->msg << std::endl;
              entry->can_read = 1;
          }
      }
      // 3. 脱离进程空间
      shmdt(entry);
  
      // 4. 删除共享内存 
      shmctl(shmid, IPC_RMID, 0);
  
      return 0;
  }
  
  ```

# 进程同步- Unix域套接字

- 用于同一主机间进程的进程间通信，提供了类似于网络套接字类似的功能，如可靠性传输

- 实例

  ```
  #include <stdio.h>
  #include <sys/types.h>
  #include <sys/socket.h>
  #include <sys/un.h>
  #include <strings.h>
  #include <string.h>
  #include <netinet/in.h>
  #include <stdlib.h>
  #include <unistd.h>
  
  #include <iostream>
  
  // 域套接字
  #define SOCKET_PATH "./domainsocket"
  #define MSG_SIZE 2048
  
  int main()
  {
      int socket_fd, accept_fd;
  	int ret = 0;
  	socklen_t addr_len;
  	char msg[MSG_SIZE];
  	struct sockaddr_un server_addr;
  
      // 1. 创建域套接字
  	socket_fd = socket(PF_UNIX,SOCK_STREAM,0);
  	if(-1 == socket_fd){
  		std::cout << "Socket create failed!" << std::endl;
  		return -1;
  	}
      // 移除已有域套接字路径
  	remove(SOCKET_PATH);
      // 内存区域置0
  	bzero(&server_addr,sizeof(server_addr));
  	server_addr.sun_family = PF_UNIX;
  	strcpy(server_addr.sun_path, SOCKET_PATH);
  
      // 2. 绑定域套接字
      std::cout << "Binding socket..." << std::endl;
  	ret = bind(socket_fd,(sockaddr *)&server_addr,sizeof(server_addr));
  
  	if(0 > ret){
  		std::cout << "Bind socket failed." << std::endl;
  		return -1;
  	}
  	
      // 3. 监听套接字
      std::cout << "Listening socket..." << std::endl;
  	ret = listen(socket_fd, 10);
  	if(-1 == ret){
  		std::cout << "Listen failed" << std::endl;
  		return -1;
  	}
      std::cout << "Waiting for new requests." << std::endl;
      accept_fd = accept(socket_fd, NULL, NULL);
      
      bzero(msg,MSG_SIZE);
  
      while(true){
          // 4. 接收&处理信息
          recv(accept_fd, msg, MSG_SIZE, 0);
          std::cout << "Received message from remote: " << msg <<std::endl;
      }
  
      close(accept_fd);
  	close(socket_fd);
  	return 0;
  }
  
  
  #include <stdio.h>
  #include <sys/types.h>
  #include <sys/socket.h>
  #include <sys/un.h>
  #include <strings.h>
  #include <string.h>
  #include <netinet/in.h>
  #include <stdlib.h>
  #include <unistd.h>
  
  #include <iostream>
  
  #define SOCKET_PATH "./domainsocket"
  #define MSG_SIZE 2048
  
  int main()
  {
      int socket_fd;
  	int ret = 0;
  	char msg[MSG_SIZE];
  	struct sockaddr_un server_addr;
  
      // 1. 创建域套接字
  	socket_fd = socket(PF_UNIX, SOCK_STREAM, 0);
  	if(-1 == socket_fd){
  		std::cout << "Socket create failed!" << std::endl;
  		return -1;
  	}
      
      // 内存区域置0
  	bzero(&server_addr,sizeof(server_addr));
  	server_addr.sun_family = PF_UNIX;
  	strcpy(server_addr.sun_path, SOCKET_PATH);
  
      // 2. 连接域套接字
  	ret = connect(socket_fd, (sockaddr *)&server_addr, sizeof(server_addr));
  
  	if(-1 == ret){
  		std::cout << "Connect socket failed" << std::endl;
  		return -1;
  	}
  
  	while(true){
          std::cout << "Input message>>> ";
          fgets(msg, MSG_SIZE, stdin);
  		// 3. 发送信息
  		ret = send(socket_fd, msg, MSG_SIZE, 0);
  	}
  
  	close(socket_fd);
  	return 0;
  }
  ```