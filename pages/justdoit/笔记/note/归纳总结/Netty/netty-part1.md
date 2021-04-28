#  IO & NIO
## Blocking IO 

```

public class PlainEchoServer {
    public void serve(int port) throws IOException {
        final ServerSocket socket = new ServerSocket(port);              
        try {
            while (true) {
                final Socket clientSocket = socket.accept();             
                System.out.println("Accepted connection from " +
                        clientSocket);
                new Thread(new Runnable() {                              

                    @Override
                    public void run() {
                        try {
                            BufferedReader reader = new BufferedReader(
                                    new
                                            InputStreamReader(clientSocket.getInputStream()));
                            PrintWriter writer = new PrintWriter(clientSocket
                                    .getOutputStream(), true);
                            while (true) {                               
                                writer.println(reader.readLine());
                                writer.flush();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                            try {
                                clientSocket.close();
                            } catch (IOException ex) {
                                // ignore on close
                            }
                        }
                    }
                }).start();                                              
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```



*  缺点？

    一个请求一个线程

    ![](https://img2018.cnblogs.com/blog/1114580/201905/1114580-20190520201802320-1424612850.png)


* 老版本的tomcat使用此方式接受请求(tomcat7之前)

## NIO

```


public class PlainNioEchoServer {
    public void serve(int port) throws IOException {
        System.out.println("Listening for connections on port " + port);
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        ServerSocket ss = serverChannel.socket();
        InetSocketAddress address = new InetSocketAddress(port);
        ss.bind(address);                                                
        serverChannel.configureBlocking(false);
        Selector selector = Selector.open();
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);        
        while (true) {
            try {
                selector.select();                                       
            } catch (IOException ex) {
                ex.printStackTrace();
                // handle in a proper way
                break;
            }
            Set readyKeys = selector.selectedKeys();                     
            Iterator iterator = readyKeys.iterator();
            while (iterator.hasNext()) {
                SelectionKey key = (SelectionKey) iterator.next();
                iterator.remove();                                       
                try {
                    iif (key.isAcceptable()) {
                        ServerSocketChannel server = (ServerSocketChannel)key.channel();
                        SocketChannel Client = server.accept();
                        client.configureBlocking(false);
                        client.register(selector,SelectionKey.OP_READ|SelectionKey.OP_WRITE, ByteBuffer.allocate(100));                         
                    }
                    if (key.isReadable()) {                              
                        SocketChannel client = (SocketChannel) key.channel();
                        ByteBuffer output = (ByteBuffer) key.attachment();
                        client.read(output);                             
                    }
                    if (key.isWritable()) {                             
                        SocketChannel client = (SocketChannel) key.channel();
                        ByteBuffer output = (ByteBuffer) key.attachment();
                        output.flip();
                        client.write(output);                           
                        output.compact();
                    }
                } catch (IOException ex) {
                    key.cancel();
                    try {
                        key.channel().close();
                    } catch (IOException cex) {
                    }
                }
            }
        }
    }
}



```

![](https://img2018.cnblogs.com/blog/1114580/201905/1114580-20190520201928712-2106949489.png)


## NIO.2 (AIO 异步IO)

```
public class PlainNio2EchoServer {
    public void serve(int port) throws IOException {
        System.out.println("Listening for connections on port " + port);
        final AsynchronousServerSocketChannel serverChannel =
                AsynchronousServerSocketChannel.open();
                
        InetSocketAddress address = new InetSocketAddress(port);
        serverChannel.bind(address);                                    
        final CountDownLatch latch = new CountDownLatch(1);
        serverChannel.accept(null, new
                CompletionHandler<AsynchronousSocketChannel, Object>() {                

                    @Override
                    public void completed(final AsynchronousSocketChannel channel,
                                          Object attachment) {

                        serverChannel.accept(null, this);                       
                        ByteBuffer buffer = ByteBuffer.allocate(100);
                        channel.read(buffer, buffer,
                                new EchoCompletionHandler(channel));            
                        @Override
                        public void failed (Throwable throwable, Object attachment){
                            try {
                                serverChannel.close();                              
                            } catch (IOException e) {
                                // ingnore on close
                            } finally {
                                latch.countDown();
                            }
                        }
                    }); 
                    try{
                        latch.await();
                    } catch(InterruptedException e)
                    {
                        Thread.currentThread().interrupt();
                    }
                }
        private final class EchoCompletionHandler implements
                CompletionHandler<Integer, ByteBuffer> {
            private final AsynchronousSocketChannel channel;

            EchoCompletionHandler(AsynchronousSocketChannel channel) {
                this.channel = channel;
            }

            @Override
            public void completed(Integer result, ByteBuffer buffer) {
                buffer.flip();
                channel.write(buffer, buffer, new CompletionHandler<Integer,
                        ByteBuffer>() {


                    @Override
                    public void completed(Integer result, ByteBuffer buffer) {
                        if (buffer.hasRemaining()) {
                            channel.write(buffer, buffer, this);            
                        } else {
                            buffer.compact();
                            channel.read(buffer, buffer,
                                    EchoCompletionHandler.this);             
                        }
                    }

                    @Override
                    public void failed(Throwable exc, ByteBuffer attachment) {
                        try {
                            channel.close();
                        } catch (IOException e) {
                            // ingnore on close
                        }
                    }
                });
            }

            @Override
            public void failed(Throwable exc, ByteBuffer attachment) {
                try {
                    channel.close();
                } catch (IOException e) {
                    // ingnore on close
                }
            }
        }
    }

```

## 异步处理的两种方式 

* Futures

* Callback

## JDK NIO 的缺点

* 跨平台 

* ByteBuffer 易用性

* NIO epoll bug会导致 使用率 cpu 100%



# First Netty Application
```
public class EchoServer {
    private final int port;

    public EchoServer(int port) {
        this.port = port;
    }

    public void start() throws Exception {
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(group)                                              
                    .channel(NioServerSocketChannel.class)                     
                    .localAddress(new InetSocketAddress(port))                 
                    .childHandler(new ChannelInitializer<SocketChannel>() {    

                        @Override
                        public void initChannel(SocketChannel ch)
                                throws Exception {
                            ch.pipeline().addLast(
                                    new EchoServerHandler());                  
                        }
                    });
            ChannelFuture f = b.bind().sync(); 
            System.out.println(EchoServer.class.getName() + "started and listen on " + f.channel().localAddress());
            f.channel().closeFuture().sync(); 
        } finally { #9
            group.shutdownGracefully().sync(); 
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println(
                    ìUsage:ì + EchoServer.class.getSimpleName() +
                    ì < port > ì);
        }
        int port = Integer.parseInt(args[0]);
        new EchoServer(port).start();
    }
}
```

```
@Sharable
public class EchoServerHandler extends
        ChannelInboundHandlerAdapter {
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        System.out.println(ìServer received:ì + msg);
        ctx.write(msg);
    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) {
        ctx.writeAndFlush(Unpooled.EMPTY_BUFFER)
                .addListener(ChannelFutureListener.CLOSE);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStracktrace();
        ctx.close();
    }
}
```

* netty 重要的组件
    * Channel Handler
    * Buffers
    * Codec 编码器
    * Transports

* 事件驱动

![](https://img2018.cnblogs.com/blog/1114580/201905/1114580-20190520202335794-296348394.png)



# netty 开发实战开发应用

* brpc-java ： https://github.com/baidu/brpc-java


# TODO 

* next part ： channelHandler and Buffer