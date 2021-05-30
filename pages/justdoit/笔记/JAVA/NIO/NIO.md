# 缓冲区

## Buffer

### 使用缓冲区的好处

- Buffer类是一个抽象类，有7个直接抽象子类。除了boolean，每一种基本数据类型都有与之对应的之类：ByteBuffer、CharBuffer、DoubleBuffer、FloatBuffer、IntBuffer、LongBuffer、ShortBuffer。

### Buffer的四个核心属性

#### capacity 

- capacity 容量，表示缓冲区的大小（最多可以存放多少数据），不可以修改

####  limit 

- 限制，代表第一个不应该读取或者写入元素的index，即缓冲区中limit后面的空间[limit,capacity-1]不可以读写。limit的主要在反复从缓冲区中存取数据时使用，用于限制读的范围。

#### position

- 位置，代表下一个要读写元素的index
- 写模式下，limit=capacity，表示最多可写数据。读模式下，limit表示最多读取数据，此时被设置为写模式下的position值

####  mark

- 标记，标记一个position，默认为-1
- mark()方法在缓冲区的位置设置标记，记录此时position的值
- reset()方法将缓冲区position重置为该索引

#### 四者的一些关系

- 大小：0 <= mark <= position <= limit <= capacity
- 剩余空间=limit-position，可以通过remaining()方法

###  创建Buffer子类的对象

- Buffer的7个直接子类也是抽象类，不可以直接实例化。可以通过某一子类将对应类型的数组包装进缓冲区。
- 每一个Buffer的直接子类都有一个静态方法wrap()用于将数组放入缓冲区中，以构建不同数据类型的缓冲区
- 以ByteBuffer为例
  - public static ByteBuffer wrap(byte[] array)

    ```java
    byte[] bytes = "hello".getBytes();
    ByteBuffer byteBuffer1 = ByteBuffer.wrap(bytes);
    System.out.println(byteBuffer1.capacity());//5
    System.out.println(byteBuffer1.limit());//5
    System.out.println(byteBuffer1.position());//0
    ```

  - public static ByteBuffer wrap(byte[] array, int offset, int length)，在上一个方法的基础上可以指定偏移量和长度，这个offset也就是包装后ByteBuffer的position，而length是limit-position的大小，可以得出limit=length+position=length+offset

    ```
    ByteBuffer byteBuffer2 = ByteBuffer.wrap(bytes,0,3);
    System.out.println(byteBuffer2.capacity());//5
    System.out.println(byteBuffer2.limit());//3
    System.out.println(byteBuffer2.position());//0
    ```


### Buffer重要方法

- capacity()、position()、limit()返回对应的属性值
- position(int newPosition)、limit(int newLimit)设置新的属性值
- mark()标记当前position、reset()将position恢复到上一次mark的地方
- isReadOnly()判断是否只读缓冲区
- remaining()返回缓冲区剩余空间，hasRemaining()判断缓冲区是否有剩余空间

#### clear()

- 将缓冲区还原到初始状态：将position设置为0，将limit设置为capacity，清除mark（设置为-1）
- 缓冲区里面的数据并没有真正被清除，只是指针被还原，数据处于被遗忘的状态

#### flip()

- 对缓冲区进行翻转：将limit设置为position，将position设置为0.如果有标记，则清除标记。通俗地说，就是将缓冲区转换为读数据模式。

#### rewind()

- 重绕缓冲区，将position设置为0并丢弃mark。使缓冲区可以重复读写


## ByteBuffer

### 直接缓冲区

通过前面方式创建的缓冲区为非直接缓冲区，通过非直接缓冲区存取数据，需要通过中间缓冲区进行数据拷贝。通过allocateDirect()可以创建之间缓冲区，直接对硬盘进行数据的传输。使用allocateDirect()方法创建的缓冲区为直接缓冲区（DirectByteBuffer），使用allocate()方法创建的缓冲区为非直接缓冲区（HeapByteBuffer）。

### slice()

创建新的缓冲区，其内容是调用此方法的缓冲区的共享子序列，新缓冲区的内容从此缓冲区的当前位置开始

### asXXXBuffer()创建缓冲区视图

### duplicate()复制缓冲区

### extendSize() 缓冲区扩容

### compact()压缩缓冲区



# 通道

