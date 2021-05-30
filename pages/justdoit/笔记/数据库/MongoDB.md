# MongoDB简介

## 概述

- MongoDB 是由C++语言编写的，是一个基于分布式文件存储的开源数据库系统
- MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象（BSON，Binary JSON ）
- 字段值可以包含其他文档，数组及文档数组

## 安装与启动

- 服务端mongod、客户端mongo

## 术语解析

| SQL术语/概念 | MongoDB术语/概念 | 解释/说明                           |
| ------------ | ---------------- | ----------------------------------- |
| database     | database         | 数据库                              |
| table        | collection       | 数据库表/集合                       |
| row          | document         | 数据记录行/文档                     |
| column       | field            | 数据字段/域                         |
| index        | index            | 索引                                |
| table joins  |                  | 表连接,MongoDB不支持                |
| primary key  | primary key      | 主键,MongoDB自动将_id字段设置为主键 |

### 数据库

#### 规则

- 一个MongoDB中可以建立多个数据库
- MongoDB的默认数据库为`db`，该数据库存储在data目录中
- MongoDB的单个实例可以容纳多个独立的数据库，每一个都有自己的集合和权限，不同的数据库也放置在不同的文件中

#### 专用数据库

- **admin**： 从权限的角度来看，这是"root"数据库。要是将一个用户添加到这个数据库，这个用户自动继承所有数据库的权限。一些特定的服务器端命令也只能从这个数据库运行，比如列出所有的数据库或者关闭服务器。
- **local:** 这个数据永远不会被复制，可以用来存储限于本地单台服务器的任意集合
- **config**: 当Mongo用于分片设置时，config数据库在内部使用，用于保存分片的相关信息

#### 常用命令

- `show dbs` 显示数据库列表
- `db` 显示当前所用数据库
- `use db_name` 切换数据库

### 文档

> 文档是一组键值(key-value)对(即 BSON)。MongoDB 的文档不需要设置相同的字段，并且相同的字段不需要相同的数据类型，这与关系型数据库有很大的区别，也是 MongoDB 非常突出的特点

#### 注意

- 文档中的键/值对是有序的
- 文档中的值不仅可以是在双引号里面的字符串，还可以是其他几种数据类型（甚至可以是整个嵌入的文档)
- MongoDB区分类型和大小写
- MongoDB的文档不能有重复的键
- 文档的键是字符串。除了少数例外情况，键可以使用任意UTF-8字符

#### 文档键命名规范

- 键不能含有\0 (空字符)。这个字符用来表示键的结尾
- .和$有特别的意义，只有在特定环境下才能使用
- 以下划线"_"开头的键是保留的（不是严格要求的）

### 集合

>集合就是 MongoDB 文档组，类似于 RDBMS 中的表格。集合存在于数据库中，集合没有固定的结构，这意味着你在对集合可以插入不同格式和类型的数据，但通常情况下我们插入集合的数据都会有一定的关联性

#### 集合命名规范

- 集合名不能是空字符串""
- 集合名不能含有\0字符（空字符)，这个字符表示集合名的结尾
- 集合名不能以"system."开头，这是为系统集合保留的前缀
- 用户创建的集合名字不能含有保留字符。有些驱动程序的确支持在集合名里面包含，这是因为某些系统生成的集合中包含该字符。除非你要访问这种系统创建的集合，否则千万不要在名字里出现$。　

# 数据库操作

## 创建

```
use DATABASE_NAME
// 如果数据库不存在，则创建数据库，否则切换到指定数据库
// MongoDB 中默认的数据库为 test，如果你没有创建新的数据库，集合将存放在 test 数据库中
// 空的db不会显示在 show dbs 的结果集中
```

## 删除

```
db.dropDatabase()
```

# 集合操作

## 创建

```
db.createCollection(name, options)
```

- options

>  在插入文档时，MongoDB 首先检查固定集合的 size 字段，然后检查 max 字段

| capped      | 布尔 | （可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。**当该值为 true 时，必须指定 size 参数。** |
| ----------- | ---- | ------------------------------------------------------------ |
| autoIndexId | 布尔 | （可选）如为 true，自动在 _id 字段创建索引。默认为 false。   |
| size        | 数值 | （可选）为固定集合指定一个最大值，以千字节计（KB）。**如果 capped 为 true，也需要指定该字段。** |
| max         | 数值 | （可选）指定固定集合中包含文档的最大数量。                   |

## 删除

```
db.collection_name.drop()
```

# 文档操作

## 插入

```
db.collection_name.insert(document)

插入文档你也可以使用 db.col.save(document) 命令。如果不指定 _id 字段 save() 方法类似于 insert() 方法。如果指定 _id 字段，则会更新该 _id 的数据
```

## 更新

### update

```
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```

- **query** : update的查询条件，类似sql update查询内where后面的
- **update** : update的对象和一些更新的操作符（如\$,inc...）等，也可以理解为sql update查询内set后面的
- **upsert** : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入
- **multi** : 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新
- **writeConcern** :可选，抛出异常的级别。

### save

```
db.collection.save(
   <document>,
   {
     writeConcern: <document>
   }
)
```

- **document** : 文档数据
- **writeConcern** :可选，抛出异常的级别。

## 删除

```
db.collection.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
```

- **query** :（可选）删除的文档的条件
- **justOne** : （可选）如果设为 true 或 1，则只删除一个文档，如果不设置该参数，或使用默认值 false，则删除所有匹配条件的文档
- **writeConcern** :（可选）抛出异常的级别

```
// 删除所有数据
db.col.remove({})
```

## 查询

```
db.collection.find(query, projection)
```

- **query** ：可选，使用查询操作符指定查询条件
- **projection** ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）

```
db.collection.findOne(query, projection) 
// 只查询一条数据
```

### 条件操作符

- (>) 大于 - $gt
- (<) 小于 - $lt
- (>=) 大于等于 - $gte
- (<= ) 小于等于 - $lte

# $type操作符

> $type操作符是基于BSON类型来检索集合中匹配的数据类型，并返回结果

# Limit

> 如果你需要在MongoDB中读取指定数量的数据记录，可以使用MongoDB的Limit方法，limit()方法接受一个数字参数，该参数指定从MongoDB中读取的记录条数

````
db.COLLECTION_NAME.find().limit(NUMBER)
````

# Skip

> 使用skip()方法来跳过指定数量的数据，skip方法同样接受一个数字参数作为跳过的记录条数

```
db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)
```

# 排序

```
// 使用 1 和 -1 来指定排序的方式，其中 1 为升序排列，而 -1 是用于降序排列
db.COLLECTION_NAME.find().sort({KEY:1})
```

# 索引

## 创建

```
// 语法中 Key 值为你要创建的索引字段，1 为指定按升序创建索引，如果你想按降序来创建索引指定为 -1 即可
db.collection.createIndex(keys, options)

// 也可以创建复合索引
```

| background         | Boolean       | 建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引，即增加 "background" 可选参数。 "background" 默认值为**false** |
| ------------------ | ------------- | ------------------------------------------------------------ |
| unique             | Boolean       | 建立的索引是否唯一。指定为true创建唯一索引。默认值为**false** |
| name               | string        | 索引的名称。如果未指定，MongoDB的通过连接索引的字段名和排序顺序生成一个索引名称 |
| dropDups           | Boolean       | 3.0+版本已废弃。在建立唯一索引时是否删除重复记录,指定 true 创建唯一索引。默认值为 **false** |
| sparse             | Boolean       | 对文档中不存在的字段数据不启用索引；这个参数需要特别注意，如果设置为true的话，在索引字段中不会查询出不包含对应字段的文档.。默认值为 **false** |
| expireAfterSeconds | integer       | 指定一个以秒为单位的数值，完成 TTL设定，设定集合的生存时间。 |
| v                  | index version | 索引的版本号。默认的索引版本取决于mongod创建索引时运行的版本 |
| weights            | document      | 索引权重值，数值在 1 到 99,999 之间，表示该索引相对于其他索引字段的得分权重 |
| default_language   | string        | 对于文本索引，该参数决定了停用词及词干和词器的规则的列表。 默认为英语 |
| language_override  | string        | 对于文本索引，该参数指定了包含在文档中的字段名，语言覆盖默认的language，默认值为 language. |

# 聚合

> MongoDB中聚合(aggregate)主要用于处理数据(诸如统计平均值,求和等)，并返回计算后的数据结果。有点类似sql语句中的聚合函数

```
db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)
```

# 复制

# 分片

# 备份与恢复

