# 确保云服务器可以相互通信

# 主库

```
use db; # 选择数据库
flush tables with read lock; # 加锁
mysqldump -uroot -p123456 >/data/db.sql; # 导出结构与数据
```

# 从库

```
change master to master_host='172.17.0.17',
master_user='slave',
master_password='slave.server1',
master_log_file='mysql-bin.000001',
master_log_pos='154'
```
