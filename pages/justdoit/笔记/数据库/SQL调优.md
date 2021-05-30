# 优化

## 优化响应时间

- 创建必要的索引
- 使用预编译查询
- 调整where子句的连接顺序
- 将多个SQL压缩到一个SQL执行
- 使用表的别名，这样就可以减少解析的时间并减少哪些友列名歧义引起的语法错误
- 在in和exists中通常情况下使用exists，因为in不走索引
- 在where字句中，如果索引列是计算或者函数的一部分，DBMS的优化器将不会使用索引而使用全表查询，函数属于计算的一种
- 避免出现隐式类型转换，当某一张表中的索引字段在作为where条件的时候，如果进行了隐式类型转换，则此索引字段将会不被识别，因为隐式类型转换也属于计算，所以此时DBMS会使用全表扫面
- 防止检索范围过宽：如果DBMS优化器认为检索范围过宽，那么将放弃索引查找而使用全表扫描。下面几种可能造成检索范围过宽的情况
  - 使用is not null或者不等于判断，可能造成优化器假设匹配的记录数太多
  - 使用like运算符的时候，“a%”将会使用索引，而“a%c”和“%a”则会使用全表扫描，因此“a%c”和“%a”不能被有效的评估匹配的数量

## 优化吞吐量

- 降低事务的隔离级别（牺牲数据一致性）
- 集群

# 数据分析

## 查看服务器状态

- `show global|session status [like 'Com%']`
  - `Com_select`、`Com_insert`、`Com_update`、`Com_delete`：Mysql层面的增删改查次数
  - `Innodb_rows_read`、`Innodb_rows_inserted`、`Innodb_rows_updated`、`Innodb_rows_deleted`：innodb引擎增删改查次数
  - `Connections`：尝试连接次数
  - `Uptime`：服务器运行时长
  - `Slow_queries`：慢SQL

## 查看索引使用情况

- `show global status like 'Handler_read%'`
  - Handler_read_first
  - Handler_read_key，如果索引正在工作，这个值代表一个行被索引值读的次数，如果值越低，表示索引得到的性能改善不高，因为索引不经常使用（这个值越高越好）
  - Handler_read_last
  - Handler_read_next，按照键顺序读下一行的请求数。如果你用范围约束或如果执行索引扫描来查询索引列，该值增加
  - Handler_read_prev，按照键顺序读前一行的请求数。该读方法主要用于优化ORDER BY ... DESC
  - Handler_read_rnd，根据固定位置读一行的请求数。如果你正执行大量查询并需要对结果进行排序该值较高。你可能使用了大量需要MySQL扫描整个表的查询或你的连接没有正确使用键。这个值较高，意味着运行效率低，应该建立索引来补救
  - Handler_read_rnd_next，Handler_read_rnd_next 的值高则意味着查询运行低效，并且应该建立索引补救。这个值的含义是在数据文件中读下一行的请求数。如果正进行大量的表扫描，Handler_read_rnd_next 的值较高，则通常说明表索引不正确或写入的查询没有利用索引

## 定位并查询慢查询SQL

- 用`--log-slow-queries[=file_name]`选项启动时，`mysqld `写一个包含所有执行时间超过 long_query_time 秒的 SQL 语句的日志
  文件
- 参数配置

```
show variables like '%query%'

关注
1. show_query_log 开关
2. show_query_log_file 文件路径
3. long_query_time 阈值

show status like '%slow_queries%' // 慢查询次数（本次会话），不记录DDL语句

set global xxxKey = xxxValue // 设置全局变量，如果要永久修改配置，需要修改my.cnf或者my.imi文件
```

- 日志格式

```
# Time: 150401 11:24:27
# User@Host: root[root] @ localhost [127.0.0.1]  Id:     7
# Query_time: 0.034002  Lock_time: 0.000000 Rows_sent: 3  Rows_examined: 3
use libu;
SET timestamp=1427858667;
select * from aaa;

分析如下:
(1) Time: 执行时间
(2) User@Host: 执行sql的主机信息
(3) Query_time: sql的执行信息,Lock_time: 锁定时间, Rows_sent: 发送(结果)行数, Rows_examined:扫描的行数
(4) timestamp: 执行时间
(5) select * from aaa; : 查询语句内容
```



# 使用explain等工具分析SQL

```
// 放在select语句之前，用于描述mysql如何进行查询操作，以及mysql获取到结果需要执行的行数（加上该关键字的语句并不会真正地去执行）
// 重点字段
1. type mysql找到需要方式行的方式
2. extra 当出现using filesort（mysql会对结果使用一个外部索引排序，而不是从表里按索引次序读到相关内容。可能在内存或者磁盘上进行排序。myslq无法利用索引进行排序的排序操作称其为文件排序）或者using temporary（mysql对查询结果排序时使用临时表，常见于orderby语句以及groupby语句）时表示myslq根本不使用索引，应进行优化
3. key 使用了哪一个键的索引
```

## id

> 查询的标识符，每个 SELECT 都会自动分配一个唯一的标识符

## select_type

> SELECT 查询的类型

- SIMPLE：简单表、表示此查询不包含 UNION 查询或子查询
- PRIMARY：表示此查询是最外层的查询
- UNION：表示此查询是 UNION 的第二或随后的查询
- UNION RESULT：UNION 的结果
- DEPENDENT UNION：UNION 中的第二个或后面的查询语句, 取决于外面的查询
- SUBQUERY：子查询中的第一个 SELECT
- DEPENDENT SUBQUERY：子查询中的第一个 SELECT, 取决于外面的查询. 即子查询依赖于外层查询的结果

## table

> 查询的是哪个表

## partitions

> 匹配的分区

## type !!!

> join类型

- `system`：表中只有一条数据. 这个类型是特殊的 `const` 类型，常量表
- `const`：针对**主键**或**唯一索引**的等值查询扫描，最多只返回一行数据。`const `查询速度非常快，因为它仅仅读取一次即可
- `eq_ref`：此类型通常出现在多表的 join 查询，表示对于前表的每一个结果，都只能匹配到后表的一行结果。 并且查询的比较操作通常是 `=`， 查询效率较高​
- `ref`：此类型通常出现在多表的 join 查询，针对于**非唯一或非主键索引**，或者是使用了 `最左前缀` 规则索引的查询
- `ref_or_null`：与 ref 类似，区别在于条件中包含对 NULL 的查询
- `range`：表示使用**索引范围查询**，通过索引字段范围获取表中部分数据记录。 这个类型通常出现在 =、 <>、 >、>=、<、<=、 IS NULL、<=>、BETWEEN、IN操作中。当 `type` 是 `range` 时, 那么 EXPLAIN 输出的 `ref` 字段为 NULL, 并且 `key_len` 字段是此次查询中使用到的索引的最长的那个.
- `index`：表示全索引扫描(full index scan)， 和 ALL 类型类似，只不过 ALL 类型是全表扫描，而 index 类型则仅仅扫描所有的索引, 而不扫描数据。所要查询的数据直接在索引树中就可以获取到，而不需要扫描数据。当是这种情况时, Extra 字段 会显示 `Using index`（索引覆盖）
- `index_merge`：索引合并优化
- `unique_subquery`：in的后面是一个查询主键字段的子查询
- `index_subquery`：与 unique_subquery 类似，区别在于 in 的后面是查询非唯一索引字段的子查询
- `ALL`：表示全表扫描， 这个类型的查询是性能最差的查询之一。通常来说我们的查询不应该出现 ALL 类型的查询，如一个查询是 ALL 类型查询, 那么一般来说可以对相应的字段添加索引来避免

## possible_keys

> 此次查询中可能选用的索引

## key !!!

> 此次查询中确切使用到的索引

## key_len

> 询优化器使用了索引的字节数. 这个字段可以评估组合索引是否完全被使用, 或只有最左部分字段被使用到

## ref

> 哪个字段或常数与 key 一起被使用，显示使用哪个列或常数与key一起从表中选择行

## rows

> 显示此查询一共扫描了多少行，这个是一个估计值

## filtered

> 表示此查询条件所过滤的数据的百分比

## Extra !!!

额外的信息

- Using filesort：当 Extra 中有 `Using filesort` 时, 表示 MySQL 需额外的排序操作, 不能通过索引顺序达到排序效果. 一般有 `Using filesort`, 都建议优化去掉, 因为这样的查询 CPU 资源消耗大
- Using index："**覆盖索引**扫描"，表示查询在索引树中就可查找所需数据，不用扫描表数据文件，往往说明性能不错
- Using temporary：查询有使用临时表，一般出现于排序，分组和多表 join 的情况，查询效率不高，建议优化
- Using index condition，会先条件过滤索引，过滤完索引后找到所有符合索引条件的数据行，随后用 WHERE 子句中的其他条件去过滤这些数据行。因为MySQL的架构原因，分成了server层和引擎层，才有所谓的“下推”的说法。所以ICP其实就是实现了index filter技术，将原来的在server层进行的table filter中可以进行index filter的部分，在引擎层面使用index filter进行处理，不再需要回表进行table filter（**索引下推**）

# MYSQL索引

- MyISAM 存储引擎的表的数据和索引是自动分开存储的，各自是独立的一个文件；InnoDB存储引擎的表的数据和索引是存储在同一个表空间里面，但可以有多个文件组成。MySQL 中索引的存储类型目前只有两种（BTREE 和 HASH），具体和表的存储引擎相关：MyISAM 和 InnoDB 存储引擎都只支持 BTREE 索引；MEMORY/HEAP 存储引擎可以支持 HASH
  和 BTREE 索引

# 存在索引但是没有使用

- `show index from table_name`，查看一个表上的索引

- 如果 MySQL 估计使用索引比全表扫描更慢，则不使用索引
- 如果使用 MEMORY/HEAP 表并且 where 条件中不使用“=”进行索引列，那么不会用到索引。heap 表只有在“=”的条件下才会使用索引
- 用 or分割开的条件，如果 or前的条件中的列有索引，而后面的列中没有索引，那么涉及到的索引都不会被用到
- 如果列类型是字符串，那么一定记得在 where 条件中把字符常量值用引号引起来，否则的话即便这个列上有索引，MySQL 也不会用到的，因为，MySQL 默认把输入的常量值进行转换以后才进行检索
- 如果如果 like 后面跟的是一个列的名字，那么索引也不会被使用

# 常见优化方法

## 定期分析表和检查表

- `ANALYZE [LOCAL | NO_WRITE_TO_BINLOG] TABLE tbl_name [, tbl_name] ...`，分析和存储表的关键字分布，分析的结果将可以使得系统得到准确的统计信息，使得 SQL 能够生成正确的执行计划
- `CHECK TABLE tbl_name [, tbl_name] ... [option] ... option = {QUICK | FAST | MEDIUM | EXTENDED
  | CHANGED}`，检查一个或多个表是否有错误

## 定期优化表

> 如果已经删除了表的一大部分，或者如果已经对含有可变长度行的表（含有 VARCHAR、BLOB 或 TEXT 列的表）进行了很多更改，则应使用 OPTIMIZE TABLE 命令来进行表优化。这个命令可以将表中的空间碎片进行合并，并且可以消除由于删除或者更新造成的空间浪费，但
> OPTIMIZE TABLE 命令只对 MyISAM、BDB 和 InnoDB 表起作用

- `OPTIMIZE [LOCAL | NO_WRITE_TO_BINLOG] TABLE tbl_name [, tbl_name] ...`

## 常用的SQL优化

### 大批量导入数据

- 因为 InnoDB 类型的表是按照主键的顺序保存的，所以将导入的数据按照主键的顺序排列，可以有效地提高导入数据的效率
- 在导入数据前执行 SET UNIQUE_CHECKS=0，关闭唯一性校验，在导入结束后执行SET UNIQUE_CHECKS=1，恢复唯一性校验，可以提高导入的效率

### 优化插入语句

- 如果同时从同一客户插入很多行，尽量使用多个值表的 INSERT 语句，这种方式将大大缩减客户端与数据库之间的连接、关闭等消耗，使得效率比分开执行的单个 INSERT 语句快
- 如果从不同客户插入很多行，能通过使用 INSERT DELAYED 语句得到更高的速度。DELAYED 的含义是让 INSERT 语句马上执行，其实数据都被放在内存的队列中，并没有真正写入磁盘，这比每条语句分别插入要快的多；LOW_PRIORITY 刚好相反，在所有其他用户对表的读写完后才进行插入

### 优化GROUP BY语句

- 默认情况下，MySQL 对所有 GROUP BY col1，col2....的字段进行排序。这与在查询中指定ORDER BY col1，col2...类似。因此，如果显式包括一个包含相同的列的 ORDER BY 子句，则对 MySQL 的实际执行性能没有什么影响。如果查询包括 GROUP BY 但用户想要避免排序结果的消耗，则可以指定 ORDER BY NULL禁止排序

### 优化ORDER BY语句

- 在某些情况中，MySQL 可以使用一个索引来满足 ORDER BY 子句，而不需要额外的排序。WHERE 条件和 ORDER BY 使用相同的索引，并且 ORDER BY 的顺序和索引顺序相同，并且ORDER BY 的字段都是升序或者都是降序
- 在以下几种情况下则不使用索引
  - order by 的字段混合 ASC 和 DESC
  - 用于查询行的关键字与 ORDER BY 中所使用的不相同
  - 对不同的关键字使用 ORDER BY

### 优化嵌套查询

> 有些情况下，子查询可以被更有效率的连接（JOIN）替代

- 连接（JOIN）之所以更有效率一些，是因为 MySQL 不需要在内存中创建临时表来完成这个逻辑上的需要两个步骤的查询工作

### 优化OR语句

- 对于含有 OR 的查询子句，如果要利用索引，则 OR 之间的每个条件列都必须用到索引；如果没有索引，则应该考虑增加索引
-  MySQL 在处理含有 OR字句的查询时，实际是对 OR 的各个字段分别查询后的结果进行了 UNION

### 使用SQL提示

- SQL 提示（SQL HINT）是优化数据库的一个重要手段，简单来说就是在 SQL 语句中加入一些人为的提示来达到优化操作的目的
- `USE INDEX`，在查询语句中表名的后面，添加 USE INDEX 来提供希望 MySQL 去参考的索引列表，就可以让 MySQL 不再考虑其他可用的索引
- `IGNORE INDEX`，如果用户只是单纯地想让 MySQL 忽略一个或者多个索引，则可以使用 IGNORE INDEX 作为 HINT
- `FORCE INDEX`，为强制 MySQL 使用一个特定的索引，可在查询中使用 FORCE INDEX 作为 HINT，当使用 FORCE INDEX 进行提示时，即便使用索引的效率不是最高，MySQL 还是选择使用了索引，这是 MySQL 留给用户的一个自行选择执行计划的权力

# 优化数据库对象

## 优化表的数据类型

- 在 MySQL 中，可以使用函数 PROCEDURE ANALYSE()对当前应用的表进行分析，该函数可以对数据表中列的数据类型提出优化建议，用户可以根据应用的实际情况酌情考虑是否实施优化

## 通过拆分表提高访问效率

- 垂直拆分，即把主码和一些列放到一个表，然后把主码和另外的列放
  到另一个表中
- 水平拆分，即根据一列或多列数据的值把数据行放到两个独立的表中（即同等地位）

## 逆规范化

- 增加冗余列：指在多个表中具有相同的列，它常用来在查询时避免连接操作
- 增加派生列：指增加的列来自其他表中的数据，由其他表中的数据经过计算生成。增加的派生列其作用是在查询时减少连接操作，避免使用集函数
- 重新组表：指如果许多用户需要查看两个表连接出来的结果数据，则把这两个表重新组成一个表来减少连接而提高性能

- 分割表

## 使用中间表提高查询效率

# 实战之`Using FileSort`优化

- 优化方法：建立联合索引

```mysql
select * from t_father_comments where album_id = 40 and status = 1 order by create_time

# 只对 album_id、create_time分别建立索引，索引走album_id，出现filesort

# 对album_id、create_time建立联合索引，索引走联合索引，不出现filesort
```

# 说说你的SQL调优思路

- 首先我们可以通过慢查询日志定位慢SQL，由于最近的调优时我使用的是测试数据库，数据量少，所以我是直接在NAVICAT软件使用explain关键字对SQL语句进行了分析。主要有两种情况，第一种是在设计数据库的时候我使用了外键，由于我的外键命名不规范，使用`fk_uid_1`格式的命名，而由于数据库会对外键建立索引，也就导致了索引命名的不规范，漏掉了不少的索引，我一一添加回去。第二种是我优化了ORDERBY子句，我在用户评论、用户反馈等接口需要返回按时间排序的列表，如果只对where子句中的字段A与ORDERBY子句字段B分别建立索引，会在explain语句返回结果中的extra字段说明使用了`file sort`，所以我根据**最左前缀匹配原则**，对where子句中的字段A以及ORDERBY的字段B建立了联合索引AB，避免了file sort。