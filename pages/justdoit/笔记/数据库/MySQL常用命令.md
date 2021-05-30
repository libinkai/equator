# 连接

## 连接服务器

- `mysql -h$ip -P$port -u$user -p`

# 管理

## 参数的查看与设置

- 查看参数 `show variables like 'xxx'`
- 设置参数 `set [global|session] xxx_key=xxx_val`

## 查看进程信息

- `show processlist`

## 查看阻塞的进程ID

- `select blocking_pid from sys.schema_table_lock_waits`
- 杀死阻塞进程 `kill query pid`或`kill pid`

# 事务

# 锁

# 日志