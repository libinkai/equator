# 经典的IO模式

## 阻塞与非阻塞

- 阻塞：读操作阻塞直到数据就绪，写操作阻塞直到缓冲区可写
- 非阻塞：数据未就绪、缓冲区满直接返回

## 同步与异步

- 同步：数据就绪之后，自己去读

- 异步：数据就绪之后直接读好再回调给应用程序

## Netty支持的IO

- Netty仅仅支持NIO，BIO已经过期废弃，AIO在Linux上不完善、性能不必NIO高太多

# Reactor

> Reactor是一种开发模式，核心流程为注册感兴趣的事件->扫描是否有感兴趣的事件发生->事件发生之后做相应的处理

- BIO -> Thread-Per-Connection
- NIO -> Reactor
- AIO -> Proactor

## 角色关心的事件

- client~SocketChannel OP_OPEN、OP_WRITE、OP_READ
- server~ServerSocketChannel OP_ACCEPT
- server~SocketChannel OP_WRITE、OP_READ