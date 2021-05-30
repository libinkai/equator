# Servlet规范

## 架构图

![Servlet与Tomcat1](.\Servlet与Tomcat1.jpg)

## Servlet接口

```java
public interface Servlet {
    void init(ServletConfig config) throws ServletException;
    
    ServletConfig getServletConfig();
    
    void service(ServletRequest req, ServletResponse res）throws ServletException, IOException;
    
    String getServletInfo();
    
    void destroy();
}
```

- 虽然 Servlet 规范并不在乎通信协议是什么，但是大多数的 Servlet 都是在 HTTP 环境中处理的，因此 Servet 规范还提供了 HttpServlet 来继承 GenericServlet，并且加入了 HTTP 特性。这样我们通过继承**HttpServlet **类来实现自己的 Servlet，只需要重写两个方法：doGet 和 doPost
- Servlet 规范里定义了**ServletContext**这个接口来对应一个 Web 应用。Web 应用部署好后，Servlet 容器在启动时会加载 Web 应用，并**为每个 Web 应用创建唯一的 ServletContext 对象**。你可以把 ServletContext 看成是一个全局对象，一个 Web 应用可能有多个 Servlet，这些 Servlet 可以通过全局的 ServletContext 来共享数据，这些数据包括 Web 应用的初始化参数、Web 应用目录下的文件资源等。由于 ServletContext 持有所有 Servlet 实例，你还可以通过它来实现 Servlet 请求的转发
- Servlet 规范提供了两种扩展机制：**Filter**和**Listener**

# Tomcat

- 处理 Socket 连接，负责网络字节流与 Request 和 Response 对象的转化：**连接器（Connector）**
- 加载和管理 Servlet，以及具体处理 Request 请求：**容器（Container）**
- Tomcat 为了实现支持多种 I/O 模型和应用层协议，一个容器可能对接多个连接器，就好比一个房间有多个门。但是单独的连接器或者容器都不能对外提供服务，需要把它们组装起来才能工作，组装后这个整体叫作 Service 组件。Service 本身没有做什么重要的事情，只是在连接器和容器外面多包了一层，把它们组装在一起。Tomcat 内可能有多个 Service，这样的设计也是出于灵活性的考虑。通过在 Tomcat 中配置多个 Service，可以实现通过不同的端口号来访问同一台机器上部署的不同应用

![Tomcat架构](./Tomcat架构.jpg)

## 目录结构

```
/bin：存放 Windows 或 Linux 平台上启动和关闭 Tomcat 的脚本文件
/conf：存放 Tomcat 的各种全局配置文件，其中最重要的是 server.xml
/lib：存放 Tomcat 以及所有 Web 应用都可以访问的 JAR 文件
/logs：存放 Tomcat 执行时产生的日志文件
/work：存放 JSP 编译后产生的 Class 文件
/webapps：Tomcat 的 Web 应用目录，默认情况下把 Web 应用放在这个目录下
```

## 日志

- `catalina.***.log`

主要是记录 Tomcat 启动过程的信息，在这个文件可以看到启动的**JVM **参数以及操作系统等日志信息

- `catalina.out`

catalina.out 是 Tomcat 的标准输出（stdout）和标准错误（stderr），这是在 Tomcat 的启动脚本里指定的，如果没有修改的话 stdout 和 stderr 会重定向到这里

- `localhost.**.log`

主要记录 Web 应用在初始化过程中遇到的未处理的**异常**，会被 Tomcat 捕获而输出这个日志文件。

- `localhost_access_log.**.txt`

存放访问 Tomcat 的**请求日志**，包括 IP 地址以及请求的路径、时间、请求协议以及状态码等信息。

- `manager.***.log/host-manager.***.log`

存放 Tomcat 自带的 manager 项目的日志信息。

## IO模型

- NIO：非阻塞 I/O，采用 Java NIO 类库实现
- NIO2：异步 I/O，采用 JDK 7 最新的 NIO2 类库实现
- APR：采用 Apache 可移植运行库实现，是 C/C++ 编写的本地库

## 应用层协议

- HTTP/1.1：这是大部分 Web 应用采用的访问协议
- AJP：用于和 Web 服务器集成（如 Apache）
- HTTP/2：HTTP 2.0 大幅度的提升了 Web 性能